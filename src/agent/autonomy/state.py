"""Freezing what a run learned, so the next one starts where it stopped.

Three things carry across a session: the per-context Beta counts, the arms the user refused
outright, and the cutoffs those readings adapted. All three are learned state - a fresh
``Learner`` would ask again for what the user already answered - and the sealed lane is
scored against exactly this payload, so it is written as plain JSON a reader can check
rather than a pickle they have to trust.

Event ids are kept with it. A resumed ask or a replayed lane delivering the same approval
twice still counts once after a freeze, which is the same idempotency the uncounted run has.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from agent.autonomy.bandit import Learner
from agent.autonomy.confidence import BetaStore
from agent.autonomy.router import Cutoffs, Router, ThresholdStore
from agent.memory.claims import ClaimScope

# Bumped when the payload's shape changes. A version this module does not know is refused
# rather than read: a learner restored from a different shape is a wrong answer, not a
# degraded one, and it would go on to decide what the agent does with real mail.
FREEZE_VERSION = 1


def freeze(learner: Learner, router: Router) -> dict[str, Any]:
    """Everything a run earned, as a JSON-serializable payload."""
    return {
        "version": FREEZE_VERSION,
        "learner": {
            "counts": [
                {"level": list(level), "approved": counted[0], "rejected": counted[1]}
                for level, counted in learner.store.counts.items()
            ],
            "blocks": [
                {
                    "claim": name,
                    "action": action,
                    "scope": {
                        "sender": scope.sender,
                        "domain": scope.domain,
                        "intent": scope.intent,
                    },
                }
                for name, (scope, action) in learner.blocks.items()
            ],
            "seen": sorted(learner.seen),
            "applied": learner.applied,
            "ignored": learner.ignored,
        },
        "router": {
            "cutoffs": [
                {"level": list(level), "silent": cutoffs.silent, "notify": cutoffs.notify}
                for level, cutoffs in router.thresholds.cutoffs.items()
            ],
            "adapted": sorted(router.adapted),
            "routings": router.routings,
        },
    }


def thaw(payload: Mapping[str, Any]) -> tuple[Learner, Router]:
    """Rebuild the learner and the router a payload was frozen from.

    Every field is read defensively and named in the failure: a corrupted freeze should say
    which entry is wrong, not raise a bare KeyError three frames down.
    """
    version = payload.get("version")
    if version != FREEZE_VERSION:
        raise ValueError(
            f"frozen state version {version!r} is not the {FREEZE_VERSION} this build reads"
        )
    learner_blob = _section(payload, "learner")
    router_blob = _section(payload, "router")

    learner = Learner(BetaStore())
    for entry in _entries(learner_blob, "counts"):
        level = tuple(_strings(entry, "level"))
        try:
            learner.store.counts[level] = [
                float(entry["approved"]),
                float(entry["rejected"]),
            ]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"frozen count for level {level!r} is malformed: {error}") from error

    for entry in _entries(learner_blob, "blocks"):
        scope = _section(entry, "scope")
        learner.blocks[str(entry.get("claim", ""))] = (
            ClaimScope(
                sender=scope.get("sender"),
                domain=scope.get("domain"),
                intent=scope.get("intent"),
            ),
            str(entry.get("action", "")),
        )

    learner.seen = {str(item) for item in learner_blob.get("seen") or ()}
    learner.applied = int(learner_blob.get("applied", 0))
    learner.ignored = int(learner_blob.get("ignored", 0))

    thresholds = ThresholdStore()
    for entry in _entries(router_blob, "cutoffs"):
        level = tuple(_strings(entry, "level"))
        try:
            thresholds.cutoffs[level] = Cutoffs(
                silent=float(entry["silent"]), notify=float(entry["notify"])
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"frozen cutoffs for level {level!r} are malformed: {error}") from error

    router = Router(learner, thresholds=thresholds)
    router.adapted = {str(item) for item in router_blob.get("adapted") or ()}
    router.routings = int(router_blob.get("routings", 0))
    return learner, router


def save(path: Path | str, learner: Learner, router: Router) -> Path:
    """Write the frozen state, naming the file in the failure rather than raising blind."""
    target = Path(path)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(freeze(learner, router), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except OSError as error:
        raise ValueError(f"cannot write frozen state to {target}: {error}") from error
    return target


def load(path: Path | str) -> tuple[Learner, Router]:
    """Read a frozen state back, or say what about it could not be read."""
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(f"cannot read frozen state {source}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"frozen state {source} is not JSON: {error}") from error
    if not isinstance(payload, Mapping):
        raise ValueError(f"frozen state {source} is not an object")
    return thaw(payload)


def _section(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    found = payload.get(key)
    if not isinstance(found, Mapping):
        raise ValueError(f"frozen state has no {key!r} section")
    return found


def _entries(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    found = payload.get(key)
    if found is None:
        found = []
    if not isinstance(found, list):
        raise ValueError(f"frozen {key!r} has to be a list")
    for entry in found:
        if not isinstance(entry, Mapping):
            raise ValueError(f"every frozen {key!r} entry has to be an object, got {entry!r}")
    return list(found)


def _strings(entry: Mapping[str, Any], key: str) -> list[str]:
    found = entry.get(key)
    if not isinstance(found, list) or not all(isinstance(item, str) for item in found):
        raise ValueError(f"frozen entry's {key!r} has to be a list of strings, got {found!r}")
    return list(found)


__all__ = ["FREEZE_VERSION", "freeze", "load", "save", "thaw"]
