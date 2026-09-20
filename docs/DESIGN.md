# DESIGN.md

The short version of how the agent is put together and why the load bearing decisions are
what they are. Route semantics in full live in `docs/routes.md`; measured runs live in
`docs/analysis.md`.

## One arrival, one route, and the route names the work

Every mail ends on exactly one of four routes. The route is a promise about what ran, not a
label for how risky the mail felt:

| Route | What happened |
| --- | --- |
| `PROCEED_SILENTLY` | the tools ran, nobody was told |
| `PROCEED_AND_NOTIFY` | the tools ran, a receipt was written |
| `ASK_FIRST_WITH_PREDRAFT` | a draft is prepared and waiting |
| `ESCALATE` | nothing was prepared at all |

`Route` in `src/agent/safety/floor.py` is the only definition. The dataset, the events, the
traces and the reports all use these four words, so nothing translates between spellings.
When two sources disagree, the strictest route wins.

## The floor masks the ballot before anything is scored

`floor_check` is a pure function with no model in it. It reads the mail's risk signals and
the proposed action's class and removes routes. A forbidden route is gone, not penalised, so
the router and the learner never see it and there is nothing to vote on.

| Signal | Routes left |
| --- | --- |
| money, credentials, injection, an unknown tool | `ESCALATE` alone |
| external send, mass send, permanent delete | ask or escalate |
| irreversible internal | notify, ask or escalate |
| anything reversible or read only | all four |

Money, credentials and injection come from the mail and the sender, not from whatever the
model proposed, so a harmless looking label on a spoofed invoice still ends at escalate.
That change alone took adversarial escalation from 14/20 to 20/20 while the model kept
proposing. `FLOOR_VERSION = "1.0"` is code, not configuration.

Silence is not approval. `Learner.observe` moves only on an explicit decision (`approve`,
`reject`, `edit_draft`, `change_tier`, `revert`, `always_do_this`, `never_do_this`), a revert
counts as three rejections, and every update is keyed by the feedback event's id so a
replayed run counts once.

## Scoring is expected loss in one unit

Once the ballot is masked, each surviving route is priced in handoffs, the cost of the user
reading the mail, deciding, and doing the work. `ESCALATE` is that unit, so every other
number reads as a fraction of handing the mail over. Costs are `LOSS_V1` in
`src/agent/autonomy/loss.py`, versioned rather than edited. A tie goes to the more cautious
route. Safety is the mask, never a term in the arithmetic.

## The model proposes, the code decides

- **Pre-triage** is pure Python (known senders, system notifications, intent markers) and
  settles 18 to 29 percent of arrivals with no model call at all.
- **The gateway** returns an untrusted proposal and nothing else. There is no path from
  gateway output to a grant. Malformed output gets one schema repair retry, then fails
  closed.
- **Jev** answers narrow typed questions about the mail in about 400ms and its route answer
  becomes the router's route evidence. If Jev is unreachable the run falls back to the text
  model's route and says so in the rationale instead of pretending.
- **Triage signals can fence the ballot on their own**, so an adversarial mail the model
  reads as harmless cannot slip under the action class fence.

One provider name (`rules`, `openrouter`, `openrouter+jev`) resolves the whole recipe, so a
run is described by a single flag and by `WAJO_PROVIDER` in the environment.

## Tools are one contract: prepare, authorize, commit

`prepare` computes the steps and validates parameters, and mutates nothing. `authorize` is
the only gate and it reads the route plus the prepared action's digest, so an approval
cannot be replayed onto different work. `commit` is the only thing that changes state and
writes one receipt per committed action, which is what the learner and the eval attribute
feedback to. The send tool exists and is never committed in any run.

## Learning is posteriors plus scoped rules

A bucket per (intent, domain, sender class, action) holds a Beta posterior, updated from
receipts and explicit feedback. Posteriors and adapted thresholds decide which autonomous
routes are even eligible, then the router picks by expected loss. A confirmed rule can
refuse an arm. It can never grant one.

## Replay and the split firewall

A seeded clock, an append only event stream, and a manifest pinning the dataset digest, the
lane and the split. Interactive code cannot open held out rows, held out code cannot write
learner state, and a breach is `SPLIT_VIOLATION` rather than a warning. Two same seed runs
produce byte identical event logs, and every run reports a replay digest.

## State and traces carry ids, never mail

`GraphState` holds ids, hashes and bounded data. The trace sink redacts bodies, secrets and
PII maps, so `traces/` never contains the mail itself.

## The harness runs the real graph

The sandbox and the eval harness drive the same compiled graph the CLI does. Nothing is
measured through a second implementation, so a number cannot come from code that only the
bench exists to run.

## Deliberately not built

No service, no queue, no database: a run is a process and its state is files. No agent
framework beyond LangGraph and a checkpointer. No second definition of the routes anywhere.
No configuration for the floor.
