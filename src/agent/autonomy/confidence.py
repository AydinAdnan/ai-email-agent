from __future__ import annotations

from dataclasses import dataclass
from random import Random

# The prior is distrustful on purpose: Beta(1, 3) is a mean of 0.25, so a bucket nobody
# has said anything about routes the cautious way until the user has actually said
# otherwise, more than once.
PRIOR_ALPHA = 1.0
PRIOR_BETA = 3.0

# A revert is the user undoing work the agent did, so it counts as three rejections: a
# mistake they had to clean up says more than a silence they did not have to break.
REVERT_WEIGHT = 3.0

LEVEL_CONTEXT = "sender+intent+action"
LEVEL_INTENT = "intent+action"
LEVEL_ACTION = "action"
LEVEL_GLOBAL = "global"


@dataclass(frozen=True)
class Bucket:
    """The context a posterior is kept for: the mail's shape, and the work proposed."""

    sender: str = ""
    intent: str = ""
    action: str = ""

    def levels(self) -> tuple[tuple[str, ...], ...]:
        """This bucket and every level it backs off to, most specific first.

        A level is only in the chain when the bucket names what that level is keyed on:
        a mail with no intent cannot be read at ``intent+action``, because that level would
        be counting a different question.
        """
        levels: list[tuple[str, ...]] = []
        if self.sender and self.intent and self.action:
            levels.append((LEVEL_CONTEXT, self.sender, self.intent, self.action))
        if self.intent and self.action:
            levels.append((LEVEL_INTENT, self.intent, self.action))
        if self.action:
            levels.append((LEVEL_ACTION, self.action))
        levels.append((LEVEL_GLOBAL,))
        return tuple(levels)

    def describe(self) -> str:
        """The bucket in one line, for a run summary or a trace."""
        named = [part for part in (self.sender, self.intent, self.action) if part]
        return " + ".join(named) or LEVEL_GLOBAL


@dataclass(frozen=True)
class Posterior:
    """One estimate: the counts the store holds, with the prior folded in."""

    alpha: float
    beta: float
    # Which level of the chain answered. Empty when nothing anywhere has counts.
    level: str = ""

    @property
    def mean(self) -> float:
        """The probability the user approves of this, before any sampling."""
        return self.alpha / (self.alpha + self.beta)

    @property
    def evidence(self) -> float:
        """How much has been counted at the answering level, in units of feedback."""
        return max((self.alpha - PRIOR_ALPHA) + (self.beta - PRIOR_BETA), 0.0)

    def describe(self) -> str:
        where = self.level or "no history"
        return f"mean {self.mean:.2f} ({where}, alpha={self.alpha:g} beta={self.beta:g})"


class BetaStore:
    """Per-context Beta posteriors, resolved through a backoff chain.

    Every level starts at Beta(1, 3). An observation is counted at every level of the chain
    it belongs to, so one approval about one sender is also evidence about that intent and
    about the mailbox as a whole. A level with no counts of its own is skipped rather than
    read as the prior, which is what makes a cold context resolve to the coarse counts
    instead of starting from nothing: only a bucket nothing anywhere has touched is the
    prior itself.
    """

    def __init__(self) -> None:
        self.counts: dict[tuple[str, ...], list[float]] = {}

    def posterior(self, bucket: Bucket) -> Posterior:
        """What is believed about this bucket, through the chain when it has no history."""
        for level in bucket.levels():
            counted = self.counts.get(level)
            if counted is not None and (counted[0] or counted[1]):
                return Posterior(
                    alpha=PRIOR_ALPHA + counted[0],
                    beta=PRIOR_BETA + counted[1],
                    level=level[0],
                )
        return Posterior(alpha=PRIOR_ALPHA, beta=PRIOR_BETA)

    def record(self, bucket: Bucket, *, approved: bool, weight: float = 1.0) -> None:
        """Count one observation, at every level of the bucket's chain."""
        for level in bucket.levels():
            counted = self.counts.setdefault(level, [0.0, 0.0])
            counted[0 if approved else 1] += weight

    def draw(self, bucket: Bucket, rng: Random) -> float:
        """One Thompson sample: the number an arm is compared with."""
        posterior = self.posterior(bucket)
        return rng.betavariate(posterior.alpha, posterior.beta)

    def observed(self) -> tuple[Bucket, ...]:
        """Every level anything has been counted about, most evidential first."""
        found = [
            (_bucket_from(level), counted[0] + counted[1])
            for level, counted in self.counts.items()
            if counted[0] or counted[1]
        ]
        return tuple(bucket for bucket, _ in sorted(found, key=lambda item: -item[1]))

    def contexts(self) -> tuple[Bucket, ...]:
        """The most specific contexts counted about, most evidential first.

        This is what a run reports: the coarse levels are the same observations pooled, so
        listing them separately would read as more history than the user actually gave.
        """
        return tuple(
            bucket for bucket in self.observed() if bucket.sender and bucket.intent
        )


def _bucket_from(level: tuple[str, ...]) -> Bucket:
    """The bucket a stored level key stands for, for reporting."""
    if level[0] == LEVEL_CONTEXT:
        return Bucket(sender=level[1], intent=level[2], action=level[3])
    if level[0] == LEVEL_INTENT:
        return Bucket(intent=level[1], action=level[2])
    if level[0] == LEVEL_ACTION:
        return Bucket(action=level[1])
    return Bucket()


__all__ = [
    "LEVEL_ACTION",
    "LEVEL_CONTEXT",
    "LEVEL_GLOBAL",
    "LEVEL_INTENT",
    "PRIOR_ALPHA",
    "PRIOR_BETA",
    "REVERT_WEIGHT",
    "BetaStore",
    "Bucket",
    "Posterior",
]
