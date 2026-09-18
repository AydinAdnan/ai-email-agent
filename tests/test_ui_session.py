from __future__ import annotations

import importlib.util
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from agent.safety.floor import Route
from agent.ui.session import Session, classify

REPO = Path(__file__).parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "stream_12.jsonl"
RECRUITER = "WAJO-0008"
RECRUITER_SENDER = "claire@nexustalent.synthetic.example"


def wait_until(session: Session, *, what: str, seconds: float = 20.0) -> None:
    """Poll a session the way the page does, so a slow line fails as one readable error."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if what == "waiting" and session.waiting:
            return
        if what == "done" and session.done:
            return
        time.sleep(0.02)
    raise AssertionError(f"the session never became {what}; error={session.error!r}")


def test_blocks_are_classified_for_the_page():
    assert classify("[  1/12] WAJO-0001") == "mail"
    assert classify("  [waiting] approval required: nothing goes out") == "wait"
    assert classify("        reply for WAJO-0008: 'yes'") == "reply"
    assert classify("run summary") == "summary"
    assert classify("        stored clm-1: silently archive future mail") == "note"
    assert classify("fixture: tests/fixtures/stream_12.jsonl") == "meta"


def test_the_summary_section_is_one_block_however_it_is_written(tmp_path):
    """The run writes the summary a line at a time; the page has to read it as one thing."""
    session = Session(fixture=FIXTURE, store_path=tmp_path / "prefs.jsonl")
    session.add("run summary")
    session.add("    PROCEED_SILENTLY         3")
    session.add("    seed=7 replay_digest=b88755e7")
    session.add("session ended: 1 rule(s) in force")
    assert [block.kind for block in session.since(0)] == ["summary", "summary", "summary", "note"]


def test_a_session_shows_the_mail_and_takes_a_line(tmp_path):
    session = Session(fixture=FIXTURE, seed=7, store_path=tmp_path / "prefs.jsonl")
    session.start()

    wait_until(session, what="waiting")
    blocks = session.since(0)
    assert any(block.kind == "mail" for block in blocks)
    assert session.case_id, "the page has to know which decision is waiting"

    # The line a person would type at an ask-first case, and the confirmation after it.
    session.reply(f"ignore mail from {RECRUITER_SENDER} from now on")
    wait_until(session, what="waiting", seconds=20)
    session.reply("yes")

    deadline = time.monotonic() + 20
    while time.monotonic() < deadline and not session.store.claims:
        time.sleep(0.02)
    assert [claim.scope.sender for claim in session.store.claims] == [RECRUITER_SENDER]

    session.stop()
    wait_until(session, what="done")
    state = session.state()
    assert state["claims"], state
    assert state["learner"]["updates"] >= 1
    assert state["posteriors"], "the page shows what the calibration moved"
    assert (tmp_path / "prefs.jsonl").exists()
    assert any(block.startswith("reply for ") for block in [b.text.lstrip() for b in session.since(0)])


def test_every_card_can_be_labeled_with_the_route_it_got(tmp_path):
    """The four states are the colours on the page, so each card needs the route it took."""
    session = Session(fixture=FIXTURE, seed=7, store_path=tmp_path / "prefs.jsonl")
    session.start()
    wait_until(session, what="waiting")

    state = session.state()
    assert state["routes_by_case"][session.case_id] in set(Route)
    # The waiting case is the ask-first one, so a rule the user states can quieten it - which
    # is what decides whether the page offers a quietening choice or only escalation.
    assert state["quietenable"] is True
    assert state["confirming"] is False

    session.reply(f"ignore mail from {RECRUITER_SENDER} from now on")
    wait_until(session, what="waiting", seconds=20)
    assert session.state()["confirming"] is True, "the run is asking about the rule it echoed"
    session.reply("yes")
    session.stop()
    wait_until(session, what="done")
    assert session.state()["confirming"] is False


def test_an_escalation_says_no_rule_can_quieten_it(tmp_path):
    """A choice the page must not offer: nothing the user says takes this one off the screen."""
    session = Session(fixture=FIXTURE, seed=7, store_path=tmp_path / "prefs.jsonl")
    session.start()

    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if session.waiting:
            if not session.quietenable:
                break
            session.reply("yes")
        time.sleep(0.02)
    assert session.waiting and session.quietenable is False
    assert any("no rule quietens this one" in block.text for block in session.since(0))

    session.stop()
    wait_until(session, what="done")


def test_a_line_is_refused_when_nothing_waits():
    session = Session(fixture=FIXTURE, seed=7, store_path=None)
    with pytest.raises(RuntimeError, match="nothing is waiting"):
        session.reply("ignore everything")


def _server(tmp_path: Path) -> tuple[Any, str]:
    """The real handler on a free port, imported the way the entry point runs it."""
    spec = importlib.util.spec_from_file_location(
        "wajo_ui_server", REPO / "frontend-ui" / "server.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.set_session(None)
    server = module.serve("127.0.0.1", 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}"


def _call(url: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """One call to the page's server: a body makes it a POST, no body a GET."""
    request = urllib.request.Request(  # noqa: S310 - the page's own server, on loopback
        url + path,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=20) as answer:  # noqa: S310 - loopback
        return json.loads(answer.read().decode("utf-8"))


def test_the_page_is_served_and_can_drive_a_session(tmp_path):
    server, url = _server(tmp_path)
    try:
        with urllib.request.urlopen(url + "/", timeout=20) as answer:  # noqa: S310 - loopback
            page = answer.read().decode("utf-8")
        assert "WAJO" in page and "/app.js" in page

        started = _call(
            url,
            "/api/start",
            {
                "fixture": str(FIXTURE),
                "lane": "calibration",
                "seed": 7,
                "store": str(tmp_path / "prefs.jsonl"),
                "provider": "rules",
            },
        )
        assert started["started"] is True

        deadline = time.monotonic() + 20
        polled = {"blocks": [], "state": {"waiting": False, "done": False}}
        while time.monotonic() < deadline and not polled["state"]["waiting"]:
            polled = _call(url, "/api/poll?since=0")
            time.sleep(0.05)
        assert polled["state"]["waiting"], polled
        assert any(block["kind"] == "mail" for block in polled["blocks"])

        assert _call(url, "/api/stop", {})["stopped"] is True
        # Stopping closes the input; the run notices on its next read rather than instantly.
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline and not _call(url, "/api/state")["done"]:
            time.sleep(0.05)
        assert _call(url, "/api/state")["done"] is True

        with pytest.raises(urllib.error.HTTPError) as refused:
            _call(url, "/api/reply", {"text": "ignore everything"})
        assert refused.value.code == 409
    finally:
        server.shutdown()
        server.server_close()
