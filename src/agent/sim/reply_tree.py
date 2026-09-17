"""Bounded reply-tree reconstruction (Phase 3.4).

Thread history arrives flat and noisy: parents may be missing, ids may repeat, and
a malformed thread can point back at itself. The traversal is therefore iterative
with an explicit stack, keeps a visited set, expands in a deterministic order, and
stops at a depth and node cap. Bounded work on untrusted input, same rules as the
floor: no recursion, no unbounded walk.
"""
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC

from agent.events import Message

DEFAULT_MAX_DEPTH = 5
DEFAULT_MAX_NODES = 200


@dataclass(frozen=True)
class ReplyTree:
    """A reconstructed thread: its roots, plus every message's children by parent id.

    A thread can have more than one root, because a missing parent link leaves its
    child detached rather than nested. ``roots`` holds them all in expansion order
    (``root`` is the one a caller asked for, or the earliest), so the walk covers
    every message the caps allowed and no branch is dropped just because it hangs
    off a second root. ``truncated`` records that a cap stopped the walk, and
    ``orphan_ids`` names messages whose parent is not in the thread at all.
    """

    root: Message
    roots: tuple[Message, ...]
    children_of: Mapping[str, tuple[Message, ...]]
    node_count: int
    max_depth_reached: int
    truncated: bool
    orphan_ids: tuple[str, ...]

    def branch(self, message_id: str) -> tuple[Message, ...]:
        """The direct replies to one message, in expansion order."""
        return self.children_of.get(message_id, ())

    def walk(self) -> tuple[Message, ...]:
        """Depth-first order over the reconstructed thread, asked-for root first."""
        ordered: list[Message] = []
        stack: list[Message] = list(reversed(self.roots))
        while stack:
            message = stack.pop()
            ordered.append(message)
            stack.extend(reversed(self.branch(message.message_id)))
        return tuple(ordered)


def _order_key(message: Message) -> tuple[int, float, str]:
    """A total order over messages: dated first, then undated, then by id.

    Thread history often carries no timestamp while the arriving message does, and
    comparing a missing stamp against an aware one would raise, so an unknown time
    becomes a leading flag rather than a ``datetime.min`` that cannot be compared.
    """
    stamp = message.sent_at
    if stamp is None:
        return (1, 0.0, message.message_id)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=UTC)
    return (0, stamp.timestamp(), message.message_id)


def build_reply_tree(
    messages: Sequence[Message] | Iterable[Message],
    *,
    root_id: str | None = None,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_nodes: int = DEFAULT_MAX_NODES,
) -> ReplyTree:
    """Reconstruct the reply tree for a thread, bounded by depth and node caps.

    Iterative DFS: a work stack of ``(message, depth)`` pairs, a visited set so a
    cycle or a duplicated id is walked once, children sorted by timestamp then id so
    two runs reconstruct the same tree.
    """
    if max_depth < 0:
        raise ValueError("max_depth must not be negative")
    if max_nodes < 1:
        raise ValueError("max_nodes must be positive")

    thread = list(messages)
    if not thread:
        raise ValueError("cannot build a reply tree from an empty thread")

    by_id: dict[str, Message] = {}
    for message in thread:
        by_id.setdefault(message.message_id, message)

    children: dict[str, list[Message]] = {}
    orphan_ids: list[str] = []
    for message in by_id.values():
        parent_id = message.parent_message_id
        if parent_id is None or parent_id not in by_id:
            if parent_id is not None:
                orphan_ids.append(message.message_id)
            continue
        children.setdefault(parent_id, []).append(message)

    for bucket in children.values():
        bucket.sort(key=_order_key)

    roots = _ordered_roots(by_id, root_id)

    visited: set[str] = set()
    resolved: dict[str, tuple[Message, ...]] = {}
    stack: list[tuple[Message, int]] = [(root, 0) for root in reversed(roots)]
    node_count = 0
    max_depth_reached = 0
    truncated = False

    while stack:
        message, depth = stack.pop()
        if message.message_id in visited:
            continue
        if node_count >= max_nodes:
            truncated = True
            break
        if depth > max_depth:
            truncated = True
            continue

        visited.add(message.message_id)
        node_count += 1
        max_depth_reached = max(max_depth_reached, depth)

        branch = tuple(child for child in children.get(message.message_id, ()))
        resolved[message.message_id] = tuple(
            child for child in branch if child.message_id not in visited
        )
        for child in reversed(branch):
            stack.append((child, depth + 1))

    return ReplyTree(
        root=roots[0],
        roots=tuple(roots),
        children_of=resolved,
        node_count=node_count,
        max_depth_reached=max_depth_reached,
        truncated=truncated,
        orphan_ids=tuple(sorted(orphan_ids)),
    )


def _ordered_roots(by_id: Mapping[str, Message], root_id: str | None) -> list[Message]:
    """Every thread root, asked-for first, the rest in a deterministic order.

    A root is a message with no parent, or one whose parent is not in the thread.
    Preferring an explicit ``root_id`` covers the thread's own declaration; the
    fallback is the earliest root, and a thread where every message has a parent
    inside it is a cycle, so the earliest message starts the walk and the visited
    set bounds it.
    """
    detached = [
        message
        for message in by_id.values()
        if message.parent_message_id is None or message.parent_message_id not in by_id
    ]
    if not detached:
        detached = list(by_id.values())

    ordered = sorted(detached, key=_order_key)
    if root_id is None:
        return ordered
    if root_id not in by_id:
        raise KeyError(root_id)

    chosen = by_id[root_id]
    return [chosen, *(message for message in ordered if message.message_id != root_id)]


__all__ = [
    "DEFAULT_MAX_DEPTH",
    "DEFAULT_MAX_NODES",
    "ReplyTree",
    "build_reply_tree",
]
