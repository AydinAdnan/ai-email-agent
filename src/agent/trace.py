from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import IO, Any

from agent.state import STATE_SCHEMA_VERSION, TRACE_KEYS, digest_of

SCHEMA_VERSION = STATE_SCHEMA_VERSION
MAX_STRING = 160
MAX_ITEMS = 32
MAX_DEPTH = 4
# A trace line carries a label, a tool call, an id - not a sentence. Mail text a tool
# composed into a short field is prose, and prose is digested.
# ponytail: a body cut under this cap would still pass; the real guard is that no schema
# field holds one, and this is the second line instead of the only one.
MAX_WORDS = 8

# A key naming mail text, a credential, or a map of PII tokens is replaced by a digest of
# its name and value, nested records included. Substrings on purpose ("draft_body",
# "sender_address"); the short words that would match half the schema are matched whole.
_REFUSED_KEY = re.compile(
    r"body|text|snippet|subject|quote|raw|secret|password|token|credential"
    r"|api[_-]?key|apikey|auth|cookie|sender|recipient|address",
    re.IGNORECASE,
)
_REFUSED_KEY_EXACT = frozenset({"to", "from", "cc", "bcc", "content", "payload"})
# A value that carries a secret anyway, whether or not its key confessed to it.
_SECRET = re.compile(
    r"secret|token_map|api[_-]?key|password|bearer\s|sk-[A-Za-z0-9-]{8}"
    r"|-----BEGIN|AKIA[0-9A-Z]{8}",
    re.IGNORECASE,
)
_ADDRESS = re.compile(r"(?P<local>[\w.+-]+)@(?P<domain>[\w-]+(?:\.[\w-]+)+)")


class TraceError(RuntimeError):
    """The trace could not be written where it was asked to go."""


@dataclass
class TraceSink:
    """Append-only JSONL trace, one line per decision, flushed as it is written."""

    path: Path
    max_chars: int = MAX_STRING
    lines: int = field(init=False, default=0)
    _handle: IO[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._handle = self.path.open("a", encoding="utf-8")
        except OSError as error:
            raise TraceError(f"cannot write a trace to {self.path}: {error}") from error
        self._emit({"schema_version": SCHEMA_VERSION, "event": "open"})

    def write(
        self,
        event: str,
        state: Mapping[str, Any],
        *,
        at: datetime | None = None,
    ) -> dict[str, Any]:
        """Record one decision and return the line that was written."""
        payload: dict[str, Any] = {"event": event}
        if at is not None:
            payload["at"] = at.isoformat()
        for key in TRACE_KEYS:
            if key in state:
                payload[key] = _safe(key, state[key], self.max_chars, depth=0)
        self._emit(payload)
        return payload

    def close(self) -> None:
        """Close the file. Safe to call twice, which an except-block may do."""
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> TraceSink:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _emit(self, payload: Mapping[str, Any]) -> None:
        try:
            line = json.dumps(payload, default=str)
        except (TypeError, ValueError) as error:  # a value the scrubber could not reach
            raise TraceError(f"cannot serialise a trace line for {self.path}: {error}") from error
        if self._handle.closed:
            raise TraceError(f"the trace at {self.path} is already closed")
        self._handle.write(line + "\n")
        self._handle.flush()
        self.lines += 1


def _refused(key: str) -> bool:
    return bool(_REFUSED_KEY.search(key)) or key.lower() in _REFUSED_KEY_EXACT


def _safe(key: str, value: Any, max_chars: int, *, depth: int) -> Any:
    """A nested record: its keys are scrubbed too, since a caller chose them."""
    if _refused(key):
        return _redacted(value)
    return _bounded(value, max_chars, depth=depth)


def _bounded(value: Any, max_chars: int, *, depth: int) -> Any:
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return _redacted(value) if _too_much(value, max_chars) else _scrub(value)
    if depth >= MAX_DEPTH:
        return _redacted(value)
    if isinstance(value, Mapping):
        return {
            _scrub_key(str(name)): _safe(str(name), item, max_chars, depth=depth + 1)
            for name, item in list(value.items())[:MAX_ITEMS]
        }
    if isinstance(value, list | tuple | set):
        return [_bounded(item, max_chars, depth=depth + 1) for item in list(value)[:MAX_ITEMS]]
    return _redacted(value)


def _scrub_key(name: str) -> str:
    """A refused key's name is itself replaced, so `token_map` cannot reach the file."""
    return _redacted(name) if _refused(name) or _SECRET.search(name) else name


def _too_much(text: str, max_chars: int) -> bool:
    return (
        len(text) > max_chars
        or len(text.split()) > MAX_WORDS
        or "\n" in text
        or bool(_SECRET.search(text))
    )


def _scrub(text: str) -> str:
    """Keep the domain, drop the person: a local part becomes a digest."""
    scrubbed = _ADDRESS.sub(lambda m: f"{digest_of(m['local'])}@{m['domain']}", text)
    return _SECRET.sub(lambda m: digest_of(m.group(0)), scrubbed)


def _redacted(value: Any) -> str:
    """A stand-in a trace can carry: the digest, the size, and what kind of thing it was."""
    payload = value if isinstance(value, str) else _fingerprint(value)
    return f"{digest_of(payload)} ({len(payload)} chars, {type(value).__name__})"


def _fingerprint(value: Any) -> str:
    try:
        return json.dumps(value, default=str, sort_keys=True)
    except (TypeError, ValueError):
        return repr(value)
