# Routes

Every arrival gets exactly one of four outcomes. The names below are the vocabulary the
dataset, the events, the traces and the reports all use, so nothing in the repo translates
between two spellings of the same route.

| Route | What happens | The user is told |
| --- | --- | --- |
| `PROCEED_SILENTLY` | The agent acts. | No |
| `PROCEED_AND_NOTIFY` | The agent acts, then reports it. | Yes, no decision needed |
| `ASK_FIRST_WITH_PREDRAFT` | The agent prepares the action and a draft, then waits for approval. | Yes, a bounded question |
| `ESCALATE` | The agent does nothing and hands the mail over with its context. | Yes, the work is theirs now |

The enum in `src/agent/safety/floor.py` (`Route`, in this order) is the only definition;
these four values are `PROCEED_SILENTLY`, `PROCEED_AND_NOTIFY`, `ASK_FIRST_WITH_PREDRAFT`
and `ESCALATE`. When two sources disagree about an arrival, the least autonomous route
wins (`strictest`), because the answer is never the average of two opinions.

## The safety floor decides who is on the ballot

`floor_check` is a pure function with no model anywhere near it. It reads the proposed
action's class and the mail's risk signals, and returns the routes still available. A
forbidden route is **removed**, not penalised: the router and the learner never see it, so
there is nothing to vote on.

`FLOOR_VERSION = "1.0"`. These ceilings are code, not configuration.

| Action class | Examples | Routes left |
| --- | --- | --- |
| `READ_ONLY` | summarize, search | all four |
| `REVERSIBLE` | archive, label, create draft, notify | all four |
| `IRREVERSIBLE_INTERNAL` | delete a mailbox item, send inside the org to a new recipient | `PROCEED_AND_NOTIFY`, `ASK_FIRST_WITH_PREDRAFT`, `ESCALATE` |
| `IRREVERSIBLE_EXTERNAL` | external send, forward, money, credentials, mass send | `ASK_FIRST_WITH_PREDRAFT`, `ESCALATE` |

A rule that fires narrows that further:

| Veto | Effect on the ballot |
| --- | --- |
| `ESCALATE` (money, credentials, injection, an unrecognised tool) | `ESCALATE` alone |
| `ASK` (external send, mass send, permanent deletion) | `ASK_FIRST_WITH_PREDRAFT` or `ESCALATE` |

So an invoice from a verified vendor, where somebody asks to change the bank account, ends
at `{ESCALATE}` no matter what the user has approved before. A learned posterior of 0.99
from a hundred clean invoices does not enter into it, because masking happens first.

## Silence is not approval

The learner moves only on an explicit decision. `LEARNABLE_FEEDBACK_KINDS` in
`src/agent/events.py` is the list: `approve`, `reject`, `edit_draft`, `change_tier`,
`revert`, `always_do_this`, `never_do_this`.

`none`, `ignore_observed` and the user's own `reply` are observations, not decisions. They
never move a posterior. `Learner.observe` refuses them a second time rather than trusting
the caller's flag, and every update is keyed by the feedback event's id, so a replayed run
or a re-delivered approval counts once.

Direction comes from the route a reading chose, not from its words: `PROCEED_SILENTLY` and
`PROCEED_AND_NOTIFY` are votes for the agent handling mail like this on its own, and the
asking routes are votes against. That is why *"never tell me about these"* — a refusal in
the sentence, silent handling in effect — raises the posterior rather than lowering it.

A revert counts as three rejections: a mistake the user had to clean up says more than a
silence they did not have to break.

## The one-unit loss matrix

Once the floor has masked the ballot, each remaining route is scored in one unit: **one
handoff**, meaning the user reads the mail, decides, and does the work themselves.
`ESCALATE`'s own cost is the unit, so every other number reads as a fraction of handing the
mail over.

```
loss(route) = sum over the outcomes that route can produce [ P(outcome | mail, route) x cost(outcome) ]
```

Costs live in `src/agent/autonomy/loss.py` as `LOSS_V1`, versioned rather than edited, and
the outcome names on the table are the outcome names the routes use, so the two vocabularies
cannot drift.

| Outcome | Cost | Why |
| --- | --- | --- |
| `missed_notification` | 1.4 | The user never learned what they needed to |
| `wrong_audience` | 2.0 | An effect reached somebody it did not concern, which cannot be fully undone |
| `wrong_action` | 0.6 | An action aimed wrongly at a class the floor still allows, undone by the receipt |
| `interruption` | 0.5 | One bounded question, work already done |
| `delay` | 0.2 | The work left the agent's queue and waits on the user's own |
| `notified` | 0.1 | A notification read but not answered |

What each route can produce: `PROCEED_SILENTLY` reads `wrong_action`, `wrong_audience` and
`missed_notification`; `PROCEED_AND_NOTIFY` reads the same action risks plus `notified`;
`ASK_FIRST_WITH_PREDRAFT` reads `interruption` alone; `ESCALATE` reads `interruption` and
`delay`. Silence cannot inform, so a route that reports nothing cannot be credited with the
user knowing — and only a handoff returns the work to the user's own queue, which is what
`delay` is charged for.

A tie goes to the more cautious route, so equal arithmetic never buys autonomy.

**Safety is not a term in this matrix.** Money, credentials, external sends, destructive
deletions and injection are removed by masking before any arithmetic runs. No cost value,
no feedback volume and no version of this table can put a fenced route back on the ballot.

### Worked example: the AWS invoice

A verified AWS billing sender, an invoice, and a persona rule that already fixes the
action: label Finance/Cloud and notify, never pay, never reply. The action is therefore not
in doubt and only the awareness is, so the mail carries no wrong-action or wrong-audience
risk.

| Route | Arithmetic | Loss |
| --- | --- | --- |
| `PROCEED_SILENTLY` | `1.0 x 1.4` | **1.4** |
| `PROCEED_AND_NOTIFY` | `1.0 x 0.1` | **0.1** |
| `ASK_FIRST_WITH_PREDRAFT` | `1.0 x 0.5` | **0.5** |
| `ESCALATE` | `1.0 x 0.5 + 1.0 x 0.2` | 0.7 |

The router picks `PROCEED_AND_NOTIFY`. Silence loses not because labeling is risky — it is
reversible — but because the awareness itself has value.

### Worked example: the ambiguous refund

*"Can you handle the refund?"* with no amount. A missing required field makes a wrong
commitment both likely and expensive, so every route that acts is dear and one bounded
question is cheap: `ASK_FIRST_WITH_PREDRAFT` at 0.5 against 2.7 for notify, 4.0 for silence
and 0.7 for a handoff. The router asks, with the question bounded: *the full amount, or the
partial one they mentioned?*

## The order the router applies

Fixed, and each step can only narrow what is left:

1. **Safety-floor mask.** Forbidden routes are gone before anything is scored.
2. **Active claim constraints.** A confirmed rule that refuses this arm removes it
   (`Learner.refuses`); a rule naming a route is evidence, not an instruction.
3. **Eligibility.** The bucket's posterior and adapted thresholds decide which of the
   remaining autonomous routes may be considered at all.
4. **Expected-loss argmin.** The cheapest surviving route wins, and every alternative is
   persisted with its posterior, its matching claim and its cost working, so a decision can
   be read back rather than re-derived.
