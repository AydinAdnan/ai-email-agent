# analysis.md — how the agent actually did

two full sandbox runs plus the gated eval in three route configurations. every number below comes
out of a real run against the real models. two numbers came out of a console and not a file, and
they're marked where they appear.

sources:

| evidence | what it is | where |
|---|---|---|
| run a | 15 arrivals, seed 8, 14 kept (1 lost) | `artifacts/final/sandbox-15/` |
| run b | 40 arrivals, seed 8, 39 kept (1 lost) | `artifacts/final/sandbox/` |
| eval | the gated two-lane eval, 60 learn → 58 sealed, three route sources | `artifacts/cmp-rules/`, `cmp-model/`, `cmp-jev/` |

## the short version

the safety half is solid, and i'd defend it in a review. the calibration half is real but thin — it
learns, it just hasn't been given enough benign mail to learn from, so "asks less over time" is
demonstrated at the level of "4 fewer asks in this one mailbox", not at the level of a trend.

- the floor held in every configuration: 0 floor violations, 0 unauthorized commits, 0 sends, and
  20/20 adversarial mail escalated. that's not just observed, it's tested — 1000 synthetic approvals
  then 1000 reverts (each revert weighing 3x) against a money-class and an external-send case still
  leaves the ballot at `{escalate}`.
- asking less works: 14 fewer asks in run b, 4 fewer in run a.
- but most of that came from the learner's posteriors, not from recalled rules. in run a, literally
  0 stored rules ever fired.
- route accuracy went 76% → 84% just by putting Jev in front of the same text model, and routing got
  3x faster while costing $0.00003 a call.
- the numbers that look best for a writeup are the weakest ones. "agreement with the brief" is 57-63%
  and the brief disagrees with itself — the writer model's own opinion scores 86% on the same mail.

## the four states, in plain words

| state | what actually happens | who's in the loop |
|---|---|---|
| `PROCEED_SILENTLY` | the tool runs — label, archive, read. no receipt is written for you | nobody |
| `PROCEED_AND_NOTIFY` | same, plus a receipt you can see afterwards | nobody, but you can see it |
| `ASK_FIRST_WITH_PREDRAFT` | nothing is committed. a reply or an action is drafted and waits on you | you, at that decision |
| `ESCALATE` | nothing is prepared at all. `AUTHORIZATION_REFUSED`, and no draft is offered | you, from scratch |

silent vs notify is decided by reversibility. ask vs escalate is decided by whether a predraft is
even safe to put in front of you — a wire-transfer demand gets no draft, because a convincing draft
is itself the risk.

## run a — 15 arrivals, 7 to learn on, 7 cold

| | result |
|---|---|
| proceeded silently | 2/7 (29%) |
| proceeded and notified | 2/7 (29%) |
| asked you first | 0/7 (0%) |
| escalated | 3/7 (43%) |
| decided without asking you | **4/7 (57%)** |
| agreement with the brief | 4/7 (57%) |
| agreement with the writer's own opinion | 6/7 (86%) |

| safety | result |
|---|---|
| floor violations | 0/7 |
| unauthorized commits | 0 |
| sends | 0 |
| hostile mail escalated | 2/2 |
| learning writes on the cold half | 0 |

| calibration | result |
|---|---|
| arrivals | 7 |
| needed the user | 7 of 7 (100%) |
| committed without asking | 0 |
| rules confirmed | 4 |
| rules that ever fired | **0** |
| posterior updates | 4 |
| asks, taught vs memoryless | 10 vs 14 → **4 fewer** |

cost $0.0172 over 28 arrivals = **$0.0006 an arrival**, 42 calls (1.50 each). two thirds of that is
the *world* writing the mail and playing you (`writer $0.0107`, `user $0.0038`); the agent's own
thinking is `jev/route $0.0006` over 17 calls plus 4 proposal calls at $0.0021. pre-triage settled
**8 of 28 arrivals (29%)** with no model call at all.

the 15-arrival run is the one where you can see the weakness clearly. every single teaching arrival
escalated, so the agent got no evidence about where autonomy is safe, and three of the four rules it
kept name one specific email address that never writes again. the reduction happened, but through
the class-level posteriors rather than anything a human could point at.

## run b — 40 arrivals, 20 to learn on, 19 cold

| | result |
|---|---|
| proceeded silently | 5/19 (26%) |
| proceeded and notified | 2/19 (11%) |
| asked you first | 0/19 (0%) |
| escalated | 12/19 (63%) |
| decided without asking you | **7/19 (37%)** |
| agreement with the brief | 12/19 (63%) |
| agreement with the writer's own opinion | 12/19 (63%) |

| safety | result |
|---|---|
| floor violations | 0/19 |
| unauthorized commits | 0 |
| sends | 0 |
| hostile mail escalated | 8/8 |
| learning writes on the cold half | 0 |

| calibration | result |
|---|---|
| arrivals | 20 |
| needed the user | 13 of 20 (65%) |
| committed without asking | 7 |
| rules confirmed | 6 |
| rules that ever fired | 3 arrivals |
| asks, taught vs memoryless | 25 vs 39 → **14 fewer** |

cost $0.0487 over 78 arrivals = **$0.0006 an arrival**, 163 calls (2.09 each). pre-triage settled
**14 of 78 (18%)**. the judge ran this time: **route defensible 0.917** over 12 judged cases, draft
grounded not scored.

per class, asks with nothing remembered → asks after learning:

| class | arrivals | memoryless | taught |
|---|---|---|---|
| newsletter | 3 | 3 | 0 |
| security notice | 2 | 2 | 0 |
| large receipt | 1 | 1 | 0 |
| small receipt | 4 | 4 | 1 |
| recruiter | 3 | 3 | 1 |
| scheduling | 3 | 3 | 1 |
| build notice | 3 | 3 | 2 |
| credential harvest | 3 | 3 | 3 |
| spoofed invoice | 4 | 4 | 4 |
| confidential ask | 2 | 2 | 2 |
| colleague question | 3 | 3 | 3 |
| injection | 2 | 2 | 2 |
| cloud invoice | 3 | 3 | 3 |
| destructive ask | 3 | 3 | 3 |

read the middle of that table, not the top. newsletters, security notices and receipts going to zero
is the system working — one class-shaped preference, the class stops asking. every hostile class
staying at 3/3 and 4/4 is also the system working: the floor refused to let learning move them. the
classes that didn't move at all are the ones where the mail was genuinely the user's call.

## run a vs run b

| | run a (15) | run b (40) |
|---|---|---|
| arrivals kept | 14 | 39 |
| automated on the cold half | 4/7 (57%) | 7/19 (37%) |
| escalated on the cold half | 3/7 (43%) | 12/19 (63%) |
| brief agreement, cold half | 4/7 (57%) | 12/19 (63%) |
| asks, taught vs memoryless | 10 vs 14 (**4 fewer**) | 25 vs 39 (**14 fewer**) |
| rules in force / that fired | 4 / 0 | 6 / 3 |
| judge | never ran | 0.917 route defensible |
| floor violations · sends | 0 · 0 | 0 · 0 |
| cost per arrival | $0.0006 | $0.0006 |

what's stable across both: the floor, the zero sends, the cost per arrival, and the fact that a
fresh mailbox produces a different mix of benign and hostile mail. what swings: how much the agent does
on its own, and that swing is a mailbox effect more than a learning effect. **you cannot
read "it improved" from these two runs, and i'm not going to.** the honest read is that both runs
show a cautious agent that stays inside its fence, and run b additionally shows three stored rules
actually being used.

## no LLM vs LLM only vs Jev + LLM

the fair place to compare is the gated eval: same 60 teaching cases, same 58 sealed cases, same
floor, same learner, only the thing proposing the route changes. `rules` is pure python — regex and
sender heuristics, no network call at all.

| on the sealed 58 | rules (no LLM) | LLM only | **Jev + LLM** |
|---|---|---|---|
| route accuracy | 47/58 (81%) | 44/58 (76%) | **49/58 (84%)** |
| action accuracy | 20/24 (83%) | 23/24 (96%) | **23/24 (96%)** |
| floor violations | 0/58 | 0/58 | 0/58 |
| unauthorized commits | 0 | 0 | 0 |
| adversarial escalated | 20/20 | 20/20 | 20/20 |
| learning writes | 0 | 0 | 0 |
| automated without asking | 30 | 33 | 28 |
| held for the user | 5 | 3 | 7 |
| escalated | 23 | 22 | 23 |
| asks during calibration | 19/60 (32%) | 20/60 (33%) | 22/60 (37%) |

so what did Jev buy. five route calls a day, 84% instead of 76%, and it kept the text model's action
quality (96%) that pure python can't reach (83%). the safety column is identical in all three, which
is exactly why swapping the router was safe to try — none of those numbers are the router's, they're
the floor's.

and here's the interesting bit, from a separate live measurement *(console only, run when the Jev
path was built, not re-run for this doc)* — the same 60 calibration cases, comparing the **raw**
route each source proposed against the gold route:

| route source | agreed with gold | median latency | cost a call |
|---|---|---|---|
| `inference-net/schematron-v2-small` | **15/60 (25%)** | 1221 ms | ~$0.00004 |
| rules provider (no LLM) | 43/60 (72%) | — | $0 |
| `~typesafe/jev-latest` | **58/60 (97%)** | 407 ms | $0.000028 |

the 25% row is the finding of the whole project. the text model answers `PROCEED_AND_NOTIFY` on 44 of
its 45 misses, so asking it for a route was buying almost nothing — the pipeline's decent numbers
were the floor and the router repairing a route that carried almost no information. ask a model
trained to answer narrow typed questions instead and the same pipeline jumps to 97% raw, twice as
fast, for less money. that's the whole case for the hybrid.

## what's actually good

- **the floor.** 0 violations across every configuration, and it's proven rather than asserted. one
  test drives 1000 approvals then 1000 reverts at a money-class case and an external-send case and
  checks the ballot is still `{escalate}` — after the posteriors moved. the fence also keys on triage
  signals, not on the model's opinion of the action, which is what took adversarial from 14/20 to
  20/20 while the model was still proposing.
- **escalate means nothing is prepared, and nothing is ever sent.** the simulated send tool exists
  and is never committed in any run.
- **it fails closed and it fails loudly.** malformed provider output gets one repair retry then fails
  closed. if Jev is unreachable, the run falls back to the model's route *and writes that into the
  rationale* rather than silently pretending the routing was Jev's.
- **the cheap layer earns its keep.** pre-triage settled 18-29% of arrivals with no model call.

## what's weak, honestly

1. **n is tiny.** 14 and 39 arrivals. the autonomy share moved 57% → 37% between two mailboxes and
   that's mailbox variance, not a trend. neither run can support a claim about improvement over time.
2. **the learning delta is confounded.** the control pass is a second walk that re-asks the live model
   with a fresh learner and no memory. it is not a replay of the taught run's own proposals. at
   temperature 0 the proposals should be identical, but "should be" isn't a measurement. this is the
   single biggest weakness in the whole evaluation, and it's fixable by caching proposals and
   replaying them.
3. **recall is thin.** 3 of 19 cold arrivals in run b, 0 of 7 in run a. most learned rules are pinned
   to one address (`escalate future mail from priya.raman@…`), which generalizes to nobody. the wins
   come from the class-shaped rules.
4. **the teaching half of a fresh mailbox is mostly hostile mail.** the right answer there is always
   escalate, so the learner gets paid for caution and learns nothing about where autonomy is safe.
5. **"agreement with the brief" is a weak oracle.** 57-63%, while the writer's own opinion of the same
   mail scores 86% in run a. the brief in `mailbox.jsonl` is a hypothesis, never a label.
6. **the judge is a single point of failure and it fell over.** run a was judged zero times because of
   a connection error; run b got 12 cases. the semantic columns should never be load-bearing.
7. **the eval report doesn't record its models.** the three-config table above is right, but you can't
   read which model produced it out of `report.json` — only out of the command someone kept in their
   shell history. that's a provenance hole in anything you hand in.
8. **a run that dies can't resume.** the pipeline has died mid-run twice on transient network stalls,
   each time after the mailbox was written and paid for. `mailbox.jsonl` is already on disk; nothing
   reads it back in.

## what i'd do next, in order

1. **cache the proposals and replay them into the control pass.** until that's done, the "asks
   fewer" number is a hypothesis, not a measurement. this is the one that changes what you can claim.
2. **make runs resumable from `mailbox.jsonl`.** stops paying for mail twice and stops losing runs.
3. **teach classes, not addresses.** the owner's card already does this for some lines; the stored
   rules should prefer the class shape, and the mailbox should guarantee every class appears in both
   halves.
4. **put the models in the eval report** and let it write the three-config table itself.
5. **harden the judge** — retry, and report `not judged` separately from `failed` so a zero is never
   ambiguous.
6. **claim learning on the sealed lane, not on a fresh mailbox.** the eval lane has a fixed 60 → 58
   split and a frozen learner; that's where an improvement number can actually be defended.

## how to reproduce

```bash
# run a and run b (each writes its own folder, ~20 and ~55 min, ~$0.02 and ~$0.05)
uv run wajo sandbox run --count 15 --seed 8 --out artifacts/final/sandbox-15
uv run wajo sandbox run --count 40 --seed 8 --out artifacts/final/sandbox

# the gated eval, once per route source (~4 min, ~$0.007 total)
uv run wajo eval all --provider rules         --out artifacts/cmp-rules
uv run wajo eval all --provider openrouter    --out artifacts/cmp-model
uv run wajo eval all --provider openrouter+jev --out artifacts/cmp-jev
```

## where everything lives

| file | what |
|---|---|
| `docs/transcript1.md` | run a's console verbatim, plus its tables and per-arrival verdicts |
| `artifacts/final/sandbox-15/` | run a: `report.md`, `report.json`, `learner.json`, `rules.jsonl`, `charts/` |
| `artifacts/final/sandbox/` | run b: same set, including all four charts |
| `artifacts/cmp-*/report.json` | the three-config eval numbers |
| `tests/test_floor_protection.py` | the proof the floor can't be moved by feedback |
