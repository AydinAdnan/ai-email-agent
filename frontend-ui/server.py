"""Serve the calibration page.

    uv run python frontend-ui/server.py

Standard library only, loopback only, one session at a time: this is a window onto a
calibration run, not a service. The run itself is the same one `wajo sim run` drives, so
everything the page shows came from the pipeline rather than from the page.
"""
from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from agent.ui.session import Session

ROOT = Path(__file__).resolve().parent
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}

# The page owns one run. A second browser tab seeing the first one's session is the honest
# behaviour for a calibration window: there is one inbox and one person answering it.
SESSION: Session | None = None


def set_session(session: Session | None) -> None:
    """Point the server at a session, which is what the tests and the page both need."""
    global SESSION
    SESSION = session


class Handler(BaseHTTPRequestHandler):
    """The page, its assets, and the four calls it makes back."""

    server_version = "wajo-ui"

    def do_GET(self) -> None:
        path, _, query = self.path.partition("?")
        if path in ASSETS:
            self._file(*ASSETS[path])
            return
        if path == "/api/poll":
            self._json(self._poll(query))
            return
        if path == "/api/state":
            self._json(self._state())
            return
        self._json({"error": f"no such path: {path}"}, status=404)

    def do_POST(self) -> None:
        body = self._body()
        if self.path == "/api/start":
            self._start(body)
            return
        if self.path == "/api/reply":
            self._reply(body)
            return
        if self.path == "/api/stop":
            self._stop()
            return
        self._json({"error": f"no such path: {self.path}"}, status=404)

    # ---------------------------------------------------------------- the four calls

    def _start(self, body: dict[str, Any]) -> None:
        """Begin a run from the form the page sent."""
        if SESSION is not None and not SESSION.done:
            self._json({"error": "a session is already running; stop it first"}, status=409)
            return
        session = Session(
            fixture=body.get("fixture") or None,
            lane=str(body.get("lane") or "calibration"),
            seed=int(body.get("seed") or 7),
            store_path=body.get("store") or None,
            provider=str(body.get("provider") or "rules"),
        )
        try:
            session.start()
        # A fixture that will not load, a lane that is sealed, a provider with no key: each
        # is a reason the page can show, and none of them should be a stack trace.
        except Exception as error:  # noqa: BLE001
            self._json({"error": f"{type(error).__name__}: {error}"}, status=400)
            return
        set_session(session)
        self._json({"started": True, **session.state()})

    def _reply(self, body: dict[str, Any]) -> None:
        if SESSION is None:
            self._json({"error": "no session has been started"}, status=409)
            return
        try:
            SESSION.reply(str(body.get("text") or ""))
        except RuntimeError as refusal:
            self._json({"error": str(refusal)}, status=409)
            return
        self._json({"sent": True, **SESSION.state()})

    def _stop(self) -> None:
        if SESSION is None:
            self._json({"error": "no session has been started"}, status=409)
            return
        SESSION.stop()
        self._json({"stopped": True, **SESSION.state()})

    def _poll(self, query: str) -> dict[str, Any]:
        since = 0
        for part in query.split("&"):
            name, _, value = part.partition("=")
            if name == "since" and value.isdigit():
                since = int(value)
        if SESSION is None:
            return {"blocks": [], "state": {"waiting": False, "done": False, "count": 0}}
        return {
            "blocks": [block.as_json() for block in SESSION.since(since)],
            "state": SESSION.state(),
        }

    def _state(self) -> dict[str, Any]:
        if SESSION is None:
            return {"error": "no session has been started"}
        return SESSION.state()

    # ---------------------------------------------------------------- plumbing

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _file(self, name: str, content_type: str) -> None:
        path = ROOT / name
        if not path.exists():
            self._json({"error": f"missing asset: {name}"}, status=404)
            return
        payload = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        """Silence the per-request log: the page polls, and the terminal stays readable."""
        return None


def serve(host: str = "127.0.0.1", port: int = 8730) -> ThreadingHTTPServer:
    """Start the server, ready to be run by the caller."""
    return ThreadingHTTPServer((host, port), Handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="serve the WAJO calibration page")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8730)
    parser.add_argument("--open", action="store_true", help="open the page in a browser")
    args = parser.parse_args(argv)

    server = serve(args.host, args.port)
    url = f"http://{args.host}:{server.server_port}/"
    print(f"serving {url} (ctrl-c to stop)")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
