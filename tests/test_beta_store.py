from __future__ import annotations

from random import Random

import pytest

from agent.autonomy.confidence import (
    PRIOR_ALPHA,
    PRIOR_BETA,
    REVERT_WEIGHT,
    BetaStore,
    Bucket,
)

CONTEXT = Bucket(
    sender="claire@nexustalent.example", intent="recruiter follow-up", action="email.create_draft"
)
INTENT_LEVEL = Bucket(intent="recruiter follow-up", action="email.create_draft")
ACTION_LEVEL = Bucket(action="email.create_draft")

# What one observation is worth, and what a confirmation is worth on top of it. The plan's
# worked example: one approval turns Beta(1, 3) into Beta(2, 3), a mean of 0.40.
ONE_APPROVAL = pytest.approx(0.4)


def test_the_prior_is_distrustful_at_every_level():
    store = BetaStore()
    for bucket in (CONTEXT, INTENT_LEVEL, ACTION_LEVEL, Bucket()):
        posterior = store.posterior(bucket)
        assert (posterior.alpha, posterior.beta) == (PRIOR_ALPHA, PRIOR_BETA)
        assert posterior.mean == pytest.approx(0.25)
        assert posterior.evidence == 0
        assert posterior.level == "", "nothing has been counted, so no level answered"


def test_a_bucket_with_no_history_resolves_through_backoff_to_global_counts():
    store = BetaStore()
    store.record(
        Bucket(sender="news@engweekly.example", intent="newsletter", action="email.apply_label"),
        approved=False,
    )
    unseen = Bucket(
        sender="nobody@nowhere.example", intent="receipt", action="email.create_draft"
    )
    posterior = store.posterior(unseen)
    assert posterior.level == "global"
    assert posterior.mean < 0.25, "the only history there is is a rejection"
    assert posterior.evidence == 1


def test_the_most_specific_level_with_counts_answers():
    store = BetaStore()
    store.record(CONTEXT, approved=True)
    other_sender = Bucket(
        sender="dana@othertalent.example",
        intent="recruiter follow-up",
        action="email.create_draft",
    )
    assert store.posterior(other_sender).level == "intent+action"
    assert store.posterior(other_sender).mean == ONE_APPROVAL


def test_an_observation_counts_at_every_level_of_its_chain():
    store = BetaStore()
    store.record(CONTEXT, approved=True)

    assert len(store.counts) == 4, "the context, its intent, its action and the mailbox"
    assert store.posterior(CONTEXT).level == "sender+intent+action"
    assert store.posterior(CONTEXT).mean == ONE_APPROVAL
    assert store.posterior(ACTION_LEVEL).mean == ONE_APPROVAL
    assert store.posterior(Bucket()).mean == ONE_APPROVAL
    assert store.contexts() == (CONTEXT,)


def test_a_bucket_missing_part_of_its_key_never_reads_a_level_it_cannot_be_keyed_by():
    """A mail with no intent cannot be counted at, or read from, the intent level."""
    store = BetaStore()
    store.record(ACTION_LEVEL, approved=True)
    assert store.posterior(ACTION_LEVEL).level == "action"
    assert [level[0] for level in Bucket(action="email.archive").levels()] == [
        "action",
        "global",
    ]
    assert "intent+action" not in [level[0] for level in Bucket(sender="a@b.example").levels()]


def test_a_revert_is_a_weight_the_callers_decide_on():
    store = BetaStore()
    store.record(CONTEXT, approved=False, weight=REVERT_WEIGHT)
    assert store.posterior(CONTEXT).beta == PRIOR_BETA + REVERT_WEIGHT
    assert store.posterior(CONTEXT).mean < 0.25


def test_a_draw_is_a_sample_of_the_posterior_and_repeats_with_its_seed():
    store = BetaStore()
    drawn = _draws(store, seed=7)
    assert all(0.0 <= value <= 1.0 for value in drawn)
    assert store.draw(CONTEXT, Random(7)) == store.draw(CONTEXT, Random(7))  # noqa: S311

    store.record(CONTEXT, approved=True)
    assert sum(_draws(store, seed=11)) / 50 > sum(drawn) / 50


def _draws(store: BetaStore, *, seed: int) -> list[float]:
    rng = Random(seed)  # noqa: S311 - a seeded generator is the point: it has to replay
    return [store.draw(CONTEXT, rng) for _ in range(50)]


def test_contexts_are_reported_most_evidential_first():
    store = BetaStore()
    store.record(ACTION_LEVEL, approved=True)
    store.record(CONTEXT, approved=True)
    store.record(CONTEXT, approved=True)

    assert store.contexts() == (CONTEXT,)
    assert Bucket() in store.observed(), "the level every observation pooled into"
    assert store.posterior(store.observed()[0]).evidence == 3
