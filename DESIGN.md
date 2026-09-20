# DESIGN.md

How the agent is put together and why the load bearing choices are what they are. The four
routes in full words live in `docs/routes.md`. Measured runs and their numbers live in
`docs/analysis.md` and `docs/transcript1.md`.

## What it measures at

- The floor: 0 violations, 0 real sends, 0 unauthorized commits across every run and every
  route configuration. Hostile mail escalated 5 of 5 in the sandbox and 20 of 20 on the
  sealed lane with the real model proposing, which is where it originally failed at 14 of 20.
  A thousand synthetic approvals and a thousand reverts against a money class and an external
  send still leave the ballot at `ESCALATE` alone.
- The four-way decision: on the final 20 mail run, 17 of 20 agree with the brief for the whole
  mailbox, 9 of 10 on the cold half the agent never saw, and the judge scores 0.88 on whether
  each route was defensible. Every escalation was correct.
- Route sources compared on the same lane: the raw text model agreed with the intended route
  25 percent of the time, the pure rules provider 76, the Jev plus LLM hybrid 84, at about
  $0.00003 a Jev call and three times the speed. The agent's own cost is about $0.0002 per
  arrival with 20 percent of arrivals settled before any model call.
- Calibration: 6 of 10 teaching arrivals handled without asking, 4 rules confirmed, and one
  clean before and after, a rule taught on one question produced an approved predraft on cold
  mail from the same sender that the memoryless pass escalated with nothing prepared.
- The honest limits: one mailbox and one seed is evidence, not a benchmark. The one predraft
  scored 0.20 on groundedness. The judge is one model's opinion and never gates anything. The
  ask count is a wash at this size, so the learning claim rests on the rule recall above.

## One arrival, one route, and the route names the work

Every mail ends on exactly one of four routes. The route promises what ran, not how risky
the mail felt:

| Route | What happened |
| --- | --- |
| `PROCEED_SILENTLY` | the tools ran, nobody was told |
| `PROCEED_AND_NOTIFY` | the tools ran, a receipt was written |
| `ASK_FIRST_WITH_PREDRAFT` | a draft is prepared and waiting |
| `ESCALATE` | nothing was prepared at all |

`Route` in `src/agent/safety/floor.py` is the only definition. The dataset, the events,
the traces and the reports all use these four words, so nothing translates between
spellings. When two sources disagree, the strictest route wins.

## The floor masks the ballot before anything is scored

`floor_check` is pure and has no model in it. It reads the mail's risk signals and the
proposed action's class, then removes routes. A forbidden route is gone, not penalised, so
the router and the learner never see it and there is nothing to vote on.

| Signal | Routes left |
| --- | --- |
| money, credentials, injection, an unknown tool | `ESCALATE` alone |
| external send, mass send, permanent delete | ask or escalate |
| irreversible internal | notify, ask or escalate |
| anything reversible or read only | all four |

Money, credentials and injection come from the mail and the sender, never from whatever
the model proposed, so a harmless looking label on a spoofed invoice still ends at
escalate. `FLOOR_VERSION` is code, not configuration. Silence is not approval:
`Learner.observe` moves only on an explicit decision, a revert counts as three rejections,
and every update is keyed by the feedback event's id so a replay counts once.

## Scoring is expected loss in one unit

Once the ballot is masked, each surviving route is priced in handoffs, meaning the cost of
the user reading the mail, deciding and doing the work. `ESCALATE` is that unit, so every
other number reads as a fraction of handing the mail over. Costs are `LOSS_V1` in
`src/agent/autonomy/loss.py`, versioned rather than edited. A tie goes to the more
cautious route. Safety is the mask, never a term in the arithmetic.

## The model proposes, the code decides

- Pre-triage is pure Python (known senders, machine notifications, intent markers) and
  settles 15 to 30 percent of arrivals with no model call at all.
- The gateway returns an untrusted proposal and nothing else. There is no path from
  gateway output to a grant. Malformed output gets one schema repair retry, then fails
  closed.
- Jev answers narrow typed questions about the mail in about 400ms and its route answer
  becomes the router's route evidence. If Jev is unreachable the run falls back to the
  text model's route and says so in the rationale instead of pretending.
- Triage signals can fence the ballot on their own, so an adversarial mail the model reads
  as harmless cannot slip under the action class fence.

One provider name (`rules`, `openrouter`, `openrouter+jev`) resolves the whole recipe, so a
run is described by a single flag and by `WAJO_PROVIDER` in the environment.

## The graph is one LangGraph, driven by everything

`build_graph` in `src/agent/graph.py` compiles a single `StateGraph(GraphState)` and that
compiled graph is what the CLI, the sandbox and the eval harness all run. There is no
second implementation for the bench to run, so a measured number cannot come from code
that only the benchmark exercises.

Eleven nodes run in a straight line, one arrival at a time:

```
START -> ingest -> consent -> minimize -> pre_triage -> proposal -> route
      -> prepare -> authorize -> interrupt ->(conditional)-> commit -> receipt -> END
```

- `interrupt` is the only branch. `_next_after_interrupt` sends the decision to `commit`
  when nothing is waiting on the user and to `END` when something is, which is what makes
  "escalate" mean nothing was prepared rather than something was prepared and withheld.
- Every node is bound to one injected `GraphRuntime` (the clock, the registry, the tools,
  the learner, the sink), so a node reads no globals and a test can hand it a fake.
- `GraphState` (in `src/agent/state.py`) is a `TypedDict` of ids, hashes and bounded data:
  `proposal`, `floor`, `routing`, `draft`, `pii`, `prepared`, `receipt`, `interrupt`,
  `approval`. It never holds a subject line or a body, because the state is what a
  checkpoint and a trace hold.
- The checkpointer is injectable and defaults to `InMemorySaver`. The sandbox freezes
  learner and rules next to the mailbox instead, which is what lets a taught half be
  replayed against a cold one.
- `authorize` re-derives from the state alone, so an approval granted before a crash still
  runs and is still bound to the digest of the work it approved.

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
refuse an arm. It can never grant one. A rule's scope is the class of the mail it was said
about, or the address when the user named one, and the catch-all class the classifier falls
back to is treated as "no class read", so it can never become the scope of a silence rule.

## The eval is deepeval GEval, and it never carries a gate

`evals/sandbox.py` asks one independent model two questions about a decision the code
cannot answer on its own, using deepeval's `GEval` with `OpenRouterModel` as the judge:

- `route defensible`: was this route right for this mail?
- `grounded`: does the draft only use facts the mail or its thread supports?

Each metric is built once, with `async_mode=False` and temperature 0, and asked with one
retry on failure because a dropped connection says nothing about the mail. A judge that
never answered is reported as `not judged`, never as a zero, and the semantic columns stay
off the gates. The hard numbers (floor violations, unauthorized commits, sends, adversarial
escalation, route and action agreement, cost, deflection rate) come from the code, and
`report.json` records its own provenance so a table can be audited later.

## Replay and the split firewall

A seeded clock, an append only event stream, and a manifest pinning the dataset digest, the
lane and the split. Interactive code cannot open held out rows, held out code cannot write
learner state, and a breach is `SPLIT_VIOLATION` rather than a warning. Two same seed runs
produce byte identical event logs, and every run reports a replay digest.

## State and traces carry ids, never mail

`GraphState` holds ids, hashes and bounded data. The trace sink redacts bodies, secrets and
PII maps, so `traces/` never contains the mail itself.

## Why these choices

**Why PII masking, and why Presidio.** A checkpoint, a trace and a provider call are each a
second copy of the user's mail, and copies outlive decisions. The `minimize` node runs the
mail through Presidio before anything leaves the process, so the model reasons over
`<PERSON_1>` and `<EMAIL_2>` instead of names and addresses. Masking is one way: the reverse
map never leaves the process, lives under a bounded per-thread registry, and is dropped with
the thread, so a draft can cite a fact while the artifact on disk holds a token. Two
boundaries stay deliberate. The floor reads the raw mail, because a masked body would hide
the wire request that makes it money mail. And the traces redact bodies, secrets and the PII
map, so the one place that persists everything proves it never held the mail at all.

**Why Jev.** The route decision is a classification, and the text model was bad at it in an
instructive way: it agreed with the intended route 25 percent of the time and answered
`PROCEED_AND_NOTIFY` on 44 of its 45 misses. It was not answering the routing question at
all. Jev answers one narrow typed question, returns a distribution instead of prose, runs in
about 400ms at about $0.00003 a call, and its answer becomes the router's route evidence
while the text model keeps the job it is good at, naming the action (96 percent accuracy).
If Jev is unreachable the run falls back and says so in the rationale.

**Why LangGraph.** One compiled `StateGraph` is what the CLI, the sandbox and the harness
all run, so no measured number can come from a code path only the benchmark exercises. The
checkpointer is what makes "waiting on you" a durable state rather than a hung process: an
interrupt suspends on saved state, an approval re-derives from the state alone, and a crash
replays to exactly one effect.

**Why deepeval GEval.** Whether a route was defensible is a judgement, and a judgement
graded by a rubric and a second model beats a keyword assertion pretending to be objective.
It is built once at temperature 0 with one retry, reported as `not judged` when it never
answered, and kept off the gates, because a semantic opinion must inform the hard numbers,
never replace them.

**Why posteriors and scoped rules instead of one or the other.** Posteriors alone make the
learning unfalsifiable (a threshold moved and nobody said why); rules alone never generalize
from one correction. A bucket per (intent, domain, sender class, action) updates from what
actually happened, and a confirmed rule can refuse an arm but never grant one, so the
user's words can make the agent more careful and nothing can make it less.

## Deliberately not built

No service, no queue, no database: a run is a process and its state is files. No agent
framework beyond LangGraph and a checkpointer. No second definition of the routes anywhere.
No configuration for the floor. No rule that a model wrote without a person confirming it.
