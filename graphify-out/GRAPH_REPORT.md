# Graph Report - ai-email-agent  (2026-09-20)

## Corpus Check
- 100 files · ~104,773 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2717 nodes · 6960 edges · 152 communities (125 shown, 27 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 1043 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0d68bd2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphState
- Case
- GraphRuntime
- registry.py
- ClaimStore
- test_economics.py
- feedback.py
- _case_from_mail_row
- Bucket
- run_simulation
- test_floor.py
- ClaimScope
- ChatRunner
- .route
- Handler
- SandboxOutcome
- test_sandbox.py
- HeldOutReport
- main
- runner.py
- test_gateway.py
- persona_demanded_route
- floor.py
- test_sim_tools.py
- Effect
- test_draft_validation.py
- .render
- ProposalError
- .load
- app.js
- Route
- drafts.py
- test_jev.py
- Drafting
- Posterior
- Learner
- ._line
- test_events.py
- test_pii.py
- PresidioMasker
- Session
- SimulatedMailbox
- run_scenario
- claims.py
- ReplyTree
- test_sim.py
- drafting_for
- SplitViolation
- test_graph_resume.py
- retrieve_style
- Routes
- Lane
- run_graph
- SafetyVerdict
- _usage
- Block
- test_feedback_parser.py
- run_sandbox
- EffectLog
- injection.py
- ToolRegistry
- agent/state.py
- ModelUser
- pytest
- EventValidationError
- build_parser
- harness.py
- test_cases.py
- _background_loop
- test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in
- build_provider
- test_benign_workplace_clean_pass
- test_replay.py
- test_floor_protection.py
- _redacted
- ContextPhoneRecognizer
- _server
- write_mailbox
- ProposalRequest
- write_report
- test_loop.py
- test_freeze.py
- Workflow: graphify
- test_denominators.py
- email-autonomy-agent
- router.py
- Routing
- .lines
- rules/graphify.md
- DESIGN.md
- README.md
- analysis.md — how the agent actually did
- Transcript
- LoopReport
- .labels
- Transcript 1 - a live mailbox, decided end to end
- Judge
- masker.py
- TraceSink
- Validation
- charts
- EmailEvent
- set_session
- graph_run
- session_grant
- FeedbackContext
- Message
- test_eval_run.py
- .get_instance
- LearningConsent
- plan_deviation
- first_interrupt_of
- server.py
- Style
- _context
- SenderIdentity
- Queue
- Random
- DecisionSource
- EvalReport
- test_explicit_decisions_must_be_flagged_learnable
- _action_for
- .start
- RecognizerResult
- _provider_for
- mask_for_llm
- AnswerQueue
- _order_key
- .case_ids
- action_vocabulary
- _scope_for
- reply
- Exception
- .interrupts
- .predraft
- FeedbackContext
- GraphSession
- IO
- Reading
- datetime
- FeedbackContext

## God Nodes (most connected - your core abstractions)
1. `Route` - 176 edges
2. `Lane` - 70 edges
3. `Router` - 69 edges
4. `Learner` - 61 edges
5. `Manifest` - 54 edges
6. `ChatRunner` - 53 edges
7. `Case` - 50 edges
8. `ProposalGateway` - 49 edges
9. `run_sandbox()` - 46 edges
10. `ActionPayload` - 45 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `main()` --uses--> `SandboxError`  [INFERRED]
  src/agent/cli.py → evals/sandbox.py
- `FakeModel` --uses--> `SandboxError`  [INFERRED]
  tests/eval/test_sandbox.py → evals/sandbox.py
- `test_a_brief_the_writer_cannot_answer_is_named_not_guessed()` --uses--> `SandboxError`  [INFERRED]
  tests/eval/test_sandbox.py → evals/sandbox.py
- `ModelUser` --uses--> `FeedbackContext`  [INFERRED]
  evals/sandbox.py → src/agent/learning/feedback.py

## Import Cycles
- None detected.

## Communities (152 total, 27 thin omitted)

### Community 0 - "GraphState"
Cohesion: 0.14
Nodes (17): Command, GraphError, GraphSession, Any, RuntimeError, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human. (+9 more)

### Community 1 - "Case"
Cohesion: 0.11
Nodes (16): Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., _params_with_case(), Any, Give the action the ids the floor needs to resolve recipients and targets., RuntimeError, Reconstruct one case's thread, bounded by the reply-tree caps. (+8 more)

### Community 2 - "GraphRuntime"
Cohesion: 0.09
Nodes (32): CompiledStateGraph, authorize(), _bound(), build_graph(), _case(), commit(), consent(), GraphRuntime (+24 more)

### Community 3 - "registry.py"
Cohesion: 0.10
Nodes (28): ABC, _authorized_settled(), Authorize from the state alone, so a decision approved before a crash still…, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused (+20 more)

### Community 4 - "ClaimStore"
Cohesion: 0.12
Nodes (30): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Capability, ConsentRequired, Grant, RuntimeError, StrEnum (+22 more)

### Community 5 - "test_economics.py"
Cohesion: 0.09
Nodes (33): OpenAICompatibleProvider, A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions (+25 more)

### Community 6 - "feedback.py"
Cohesion: 0.15
Nodes (18): Claim, datetime, FeedbackKind, _claim_reading(), _decision_reading(), _nothing(), _question(), Constrained feedback parser and scope echo (plan Commit 3.6, plan section 4.6).… (+10 more)

### Community 7 - "_case_from_mail_row"
Cohesion: 0.17
Nodes (18): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime, Canonicalize one dataset row into an EmailEvent. (+10 more)

### Community 8 - "Bucket"
Cohesion: 0.09
Nodes (24): The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "run_simulation"
Cohesion: 0.12
Nodes (23): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+15 more)

### Community 10 - "test_floor.py"
Cohesion: 0.05
Nodes (66): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate. (+58 more)

### Community 11 - "ClaimScope"
Cohesion: 0.11
Nodes (27): ClaimError, ClaimScope, ValueError, Raised when a claim is underspecified, or about something never stored., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., _require_text() (+19 more)

### Community 12 - "ChatRunner"
Cohesion: 0.15
Nodes (15): Decision, What the simulator does with one arrival., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.…, Ask the one bounded question and store the rule only if it is confirmed. (+7 more)

### Community 13 - ".route"
Cohesion: 0.09
Nodes (25): _answer(), JevAnswer, JevError, _post(), Any, Message, Route, RuntimeError (+17 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "SandboxOutcome"
Cohesion: 0.09
Nodes (15): as_dict(), _learning_section(), What the learning bought, measured against the same mailbox with nothing…, The machine-readable run, for the charts and for anyone reading it later., Everything one sandbox run produced, in the shape the report and charts read., The arrivals of the half the agent had never seen, in delivery order., The route an arrival took, whichever half decided it., Arrivals the pipeline routed the way the brief (or the writer) said it should.… (+7 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.11
Nodes (31): _by_id(), The arrivals one record decided, in the order it decided them., Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, The endpoint that answers everything except the owner's own questions., Each half decides exactly the arrivals it was given, and nothing goes missing., The model user is what makes the calibration half teach: it has to be asked., Nothing hostile is committed on its own, and the count says so with its… (+23 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.10
Nodes (12): Gate, HeldOutReport, Any, _rate(), A count and its denominator, which is the only honest way to print a rate., A hard gate: a number that has to hold, not a curve that has to trend., The sealed lane: the only place accuracy is measured, and the hard gates., The plan's hard gates, each stated with the count and its denominator. An empty… (+4 more)

### Community 18 - "main"
Cohesion: 0.13
Nodes (26): LoopReport, Namespace, data_validate(), eval_all(), _keep_rules(), loop_run(), main(), _open_store() (+18 more)

### Community 19 - "runner.py"
Cohesion: 0.11
Nodes (42): asyncio, collections_abc, dataclasses, The four reference cases, run end to end and printed as transcripts. Each case…, A live mailbox: fresh mail every run, through the real pipeline, judged from…, hashlib, json, langgraph_checkpoint_memory (+34 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.07
Nodes (47): Walk both lanes with nobody at the keyboard, and score what they did. Input is…, run_two_lanes(), ProposalGateway, The offline provider: proposes from triage, no network, deterministic. It is a…, Turns provider text into a validated proposal, with one repair attempt., RuleProvider, ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, router, route out. (+39 more)

### Community 21 - "persona_demanded_route"
Cohesion: 0.12
Nodes (23): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule(), Message (+15 more)

### Community 22 - "floor.py"
Cohesion: 0.10
Nodes (40): ActionClass, classify_action(), EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement() (+32 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.16
Nodes (25): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., A tool takes mail, not a case: the same call works for any message., The plan's check: one receipt, zero sends, no payment tool anywhere. (+17 more)

### Community 24 - "Effect"
Cohesion: 0.09
Nodes (23): ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser, Any (+15 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.14
Nodes (31): DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the…, source_text() (+23 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (11): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+3 more)

### Community 27 - "ProposalError"
Cohesion: 0.08
Nodes (28): ProposalRequest, The claim's route, with whatever work the inner provider chose for the mail. An…, _with_inner_action(), parse_proposal(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Validate one provider answer. Anything unexpected is an error, not a default. (+20 more)

### Community 28 - ".load"
Cohesion: 0.20
Nodes (5): datetime, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., Keep a confirmed claim, if there is consent for it. The same claim is kept once.

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "Route"
Cohesion: 0.14
Nodes (32): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, The four autonomy outcomes a candidate action can be routed to.…, Route, GoldPolicy, Choose the dataset's route when the floor still allows it, else escalate. The…, case(), feedback() (+24 more)

### Community 31 - "drafts.py"
Cohesion: 0.12
Nodes (21): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Picked, Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, One example that fits the budget, and why it was the one kept. (+13 more)

### Community 32 - "test_jev.py"
Cohesion: 0.17
Nodes (23): answer(), FakeJev, hybrid(), message(), The Jev hybrid: Jev decides the route, the model does the work, the floor still…, A wrapped model, the model's own script, and the ledger both of them write into., Drive the wrapper the way the gateway does, and hand back what it answered., No work to prepare, so the text model is not called at all. (+15 more)

### Community 33 - "Drafting"
Cohesion: 0.12
Nodes (17): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), A reply the user cannot trust is worse than a mail handed back., One of the three fixture cases whose route is an ask with a predraft., An ask that arrives with nothing prepared is the gap this phase closes., The answer belongs to the user, so the draft quotes the ask and marks the gap. (+9 more)

### Community 34 - "Posterior"
Cohesion: 0.22
Nodes (5): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., Whether this route is on the ballot at all: the cautious ones always are.

### Community 35 - "Learner"
Cohesion: 0.07
Nodes (45): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Counts what the user said into posteriors, once per event, never from silence.…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence… (+37 more)

### Community 36 - "._line"
Cohesion: 0.33
Nodes (4): _json_default(), Any, A stable hash of the replay log., The canonical JSONL replay log: header line, then one line per arrival.

### Community 37 - "test_events.py"
Cohesion: 0.11
Nodes (29): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, A replayed stream can refuse a shape it does not understand. (+21 more)

### Community 38 - "test_pii.py"
Cohesion: 0.12
Nodes (17): get_token_map(), Retrieve the current token to original value map for a thread., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Session"
Cohesion: 0.14
Nodes (19): importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one… (+11 more)

### Community 41 - "SimulatedMailbox"
Cohesion: 0.20
Nodes (6): build_registry(), Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., SimulatedMailbox, End to end through the real contract: prepare, authorize, commit one draft., test_the_approved_draft_is_the_draft_that_is_committed()

### Community 42 - "run_scenario"
Cohesion: 0.12
Nodes (16): main(), Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it…, One canonical run: the pipeline's own output, plus what it decided and…, What the router considered, which every canonical run keeps. (+8 more)

### Community 43 - "claims.py"
Cohesion: 0.11
Nodes (26): enum, preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, _action_words(), _bears_on(), Claim, _claim_from_record(), claim_id_for() (+18 more)

### Community 44 - "ReplyTree"
Cohesion: 0.14
Nodes (15): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _address(), _body_lines(), _prior_lines(), The arriving mail the way an inbox shows it. Sender, recipients, subject, body… (+7 more)

### Community 45 - "test_sim.py"
Cohesion: 0.06
Nodes (65): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, interrupting_case_ids() (+57 more)

### Community 46 - "drafting_for"
Cohesion: 0.17
Nodes (12): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+4 more)

### Community 47 - "SplitViolation"
Cohesion: 0.12
Nodes (12): RuntimeError, Raised when code reaches across the learning/held-out firewall., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., SplitViolation, The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read., The separation is symmetric: a lane view only sees its own rows. (+4 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.13
Nodes (23): approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The plan's crash matrix: whether the work ran or not, a resume applies it once. (+15 more)

### Community 49 - "retrieve_style"
Cohesion: 0.18
Nodes (19): estimate_tokens(), A rough token count for a budget decision, not for a bill., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from., One sent reply, from the mailbox's own history., A reply the user sent this person beats an older one to anybody else. (+11 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Lane"
Cohesion: 0.06
Nodes (54): main(), Run the lanes, then print what they cost., main(), Run both lanes and print the report, so the scorer can be read before it is…, one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, main(), The eval run as a command, for anyone who would rather not go through the CLI. (+46 more)

### Community 52 - "run_graph"
Cohesion: 0.16
Nodes (17): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+9 more)

### Community 53 - "SafetyVerdict"
Cohesion: 0.25
Nodes (8): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), Assert SafetyVerdict instances are frozen to prevent tampering., test_verdict_immutability(), test_strictest_allowed_is_the_least_autonomous_route(), verdict()

### Community 54 - "_usage"
Cohesion: 0.12
Nodes (12): Ledger, _attribute(), Endpoint, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A client for this endpoint. Imported here so offline runs need no SDK., Ask the model for one proposal, off the event loop. (+4 more)

### Community 55 - "Block"
Cohesion: 0.20
Nodes (7): Block, classify(), Any, Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 56 - "test_feedback_parser.py"
Cohesion: 0.14
Nodes (25): The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a…, The one reading the parser will not assume is the one it stores only when said., An action with no scope word at all falls back to the mail in front of the…, A claim has to name the mail it came from, so a rule stated with nothing in…, The parser extracts candidates and cannot invent capability., A session's store: consent for this purpose, for this session., What confirming a reading with this answer would store, or None for nothing. (+17 more)

### Community 57 - "run_sandbox"
Cohesion: 0.12
Nodes (25): _banner(), _blocks(), _case_blocks(), _control_pass(), _judge_run(), _note(), _preview(), ProposalProvider (+17 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "injection.py"
Cohesion: 0.08
Nodes (30): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, _names_its_own_domain(), Prompt injection tripwires and plan-deviation verification. Zero LLM dependence… (+22 more)

### Community 60 - "ToolRegistry"
Cohesion: 0.08
Nodes (21): _brief(), _digest(), _notify_text(), _params_brief(), Any, Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit., Every tool the agent may hold, plus the three calls that gate one. (+13 more)

### Community 61 - "agent/state.py"
Cohesion: 0.13
Nodes (23): The chosen route's expected loss, in handoffs., Record the route the router chose, which is what authorization checks., route(), One line per decision, and one per reply: ids, hashes, bounded records., digest_of(), draft_fields(), hint_fields(), message_digest() (+15 more)

### Community 62 - "ModelUser"
Cohesion: 0.17
Nodes (14): Decision, ModelUser, Message, RuntimeError, Raised when the environment cannot be built or read., The person whose mailbox this is, played by a model that is not the proposer.…, The preference this mail's class calls for, said once and not repeated., What the reply parser may look at: the mail and the decision, never a label. (+6 more)

### Community 63 - "pytest"
Cohesion: 0.06
Nodes (48): pytest, _dependencies_first(), RuntimeError, Raised when a case names a dependency no window can deliver before it., Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., Keep the drawn order, moving a case after anything it says it waits for.…, release_order() (+40 more)

### Community 64 - "EventValidationError"
Cohesion: 0.18
Nodes (10): Attachment, DuplicateEventError, EventValidationError, ValueError, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text() (+2 more)

### Community 65 - "build_parser"
Cohesion: 0.16
Nodes (14): ArgumentParser, build_parser(), _default_provider(), The provider a run proposes with when the flag is absent. Read here rather than…, The provider the sandbox proposes with when the flag is absent. The sandbox…, The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags() (+6 more)

### Community 66 - "harness.py"
Cohesion: 0.07
Nodes (38): argparse, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, ask_curve(), Block, calibration_report(), CalibrationReport, dispositions(), RuntimeError (+30 more)

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (61): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+53 more)

### Community 68 - "_background_loop"
Cohesion: 0.29
Nodes (5): AbstractEventLoop, _background_loop(), Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 69 - "test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in"
Cohesion: 0.67
Nodes (3): CaptureFixture, MonkeyPatch, test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in()

### Community 70 - "build_provider"
Cohesion: 0.19
Nodes (13): build_provider(), Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request., The request carries the schema, so a model cannot omit a key or invent an… (+5 more)

### Community 71 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 72 - "test_replay.py"
Cohesion: 0.04
Nodes (55): EventStream, datetime, Replay events through a fresh seeded stream., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., An append-only log of arriving events. There is no update, no delete and no…, replay() (+47 more)

### Community 73 - "test_floor_protection.py"
Cohesion: 0.12
Nodes (30): Everything the router is allowed to consider for one arrival., RoutingRequest, email_context_for(), floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., Build the floor's view of a case from its canonical event., approve(), ask_again() (+22 more)

### Community 74 - "_redacted"
Cohesion: 0.14
Nodes (18): _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file., Keep the domain, drop the person: a local part becomes a digest. (+10 more)

### Community 75 - "ContextPhoneRecognizer"
Cohesion: 0.23
Nodes (7): EntityRecognizer, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span., Detects US Social Security Numbers (SSN) accurately.

### Community 76 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 77 - "write_mailbox"
Cohesion: 0.10
Nodes (23): Arrival, drawn_briefs(), generator_prompt(), parse_generated(), Any, How long a model call took, in the unit a reader cares about., One situation to write a mail about, and how a careful assistant would treat it., The request for one arrival. Everything fresh about it comes from this frame. (+15 more)

### Community 78 - "ProposalRequest"
Cohesion: 0.18
Nodes (7): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, A model in the shape of the provider protocol, answering from a script., ScriptedProvider

### Community 79 - "write_report"
Cohesion: 0.09
Nodes (23): main(), _markdown(), _rate(), What the run did, in the order a reader wants it., Write the run: the JSON, a readable markdown page, and the charts., The same reading as the terminal, as a page the numbers can be pasted from., The sandbox as a command, for anyone who would rather not go through the CLI., Rule off the next step, so a ten-minute run reads as parts, not one wall. (+15 more)

### Community 80 - "test_loop.py"
Cohesion: 0.14
Nodes (18): InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., ScriptedReplies, _drained(), loop(), Queue (+10 more)

### Community 81 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 83 - "test_denominators.py"
Cohesion: 0.08
Nodes (54): held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., Score the sealed lane, refusing outright if anything about it could teach. Both…, record_from_chat(), record_from_graph() (+46 more)

### Community 87 - "router.py"
Cohesion: 0.09
Nodes (26): is_approving(), Whether this reading is a vote for the agent acting on its own. The route a…, Random, Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the… (+18 more)

### Community 88 - "Routing"
Cohesion: 0.12
Nodes (25): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+17 more)

### Community 102 - "analysis.md — how the agent actually did"
Cohesion: 0.15
Nodes (12): analysis.md — how the agent actually did, how to reproduce, no LLM vs LLM only vs Jev + LLM, run a — 15 arrivals, 7 to learn on, 7 cold, run a vs run b, run b — 40 arrivals, 20 to learn on, 19 cold, the four states, in plain words, the short version (+4 more)

### Community 104 - "LoopReport"
Cohesion: 0.14
Nodes (8): LoopReport, Decisions that would still wait for a human, with the rules in front., Decisions the same lane waits on with nothing remembered, or 0 with no control., Arrivals a rule sent somewhere else than the lane would have gone on its own., Of those, the arrivals that came after the mail their rule was taught on. This…, Asking the rules took off the user, measured against the lane with no rules.…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions the chat pass waited on. Not a baseline: a rule takes effect from the…

### Community 105 - ".labels"
Cohesion: 0.50
Nodes (3): CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only.

### Community 106 - "Transcript 1 - a live mailbox, decided end to end"
Cohesion: 0.15
Nodes (12): 1. The console, verbatim, 2. The four states, and what each one actually does, 3. How well it did, on the half it had never seen, 4. Arrival by arrival, against the brief, 5. Analysis, 6. What this run cannot tell you, 7. Charts, Calibration — the half that teaches (+4 more)

### Community 107 - "Judge"
Cohesion: 0.17
Nodes (9): Judge, _judged(), Judgement, One judged case: the score, then the judge's own reason for it., One external opinion, with the reason it gave., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI. (+1 more)

### Community 108 - "masker.py"
Cohesion: 0.20
Nodes (9): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, _clean_person_name(), _create_analyzer(), PII Masking with Microsoft Presidio (Phase 2). Provides a warm singleton…, Build the Presidio analyzer, preferring the large spaCy model. (+1 more)

### Community 109 - "TraceSink"
Cohesion: 0.12
Nodes (24): Append-only JSONL trace, one line per decision, flushed as it is written., Close the file. Safe to call twice, which an except-block may do., TraceSink, message(), Path, Not just the serde: a compiled graph through a saver hands back the same values., The allowlist is the schema: a new field is traceable, not silently dropped., The body and subject are inputs to the decision, and must not reach the file. (+16 more)

### Community 111 - "charts"
Cohesion: 0.22
Nodes (10): charts(), Path, Route, Keep a run's transcript, naming the file in the error rather than failing mute., Keep the mailbox itself, so a report can be read next to the mail that produced…, The three pictures: what it decided, how often it asked, and how it matched., How many arrivals took each of the four routes., _save() (+2 more)

### Community 112 - "EmailEvent"
Cohesion: 0.14
Nodes (10): The lane's arriving events, in sequence order., EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread() (+2 more)

### Community 114 - "graph_run"
Cohesion: 0.33
Nodes (7): graph_run(), GraphSession, Walk a fixture through the decision graph and say what each arrival ended in., Answer one held decision with a yes and say what that committed., _resume_note(), The deliverable flow: calibrate once, then run autonomously in a later process., test_a_rule_kept_by_calibration_is_in_force_in_the_next_run()

### Community 115 - "session_grant"
Cohesion: 0.18
Nodes (11): _answered_cases(), IO, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Each arrival a rule answered, mapped to the arrival whose mail taught that rule., run_loop(), What a session carries when a human is present and typing. Consent is granted…, session_grant(), Path (+3 more)

### Community 116 - "FeedbackContext"
Cohesion: 0.20
Nodes (10): confirm_claim(), confirm_words(), FeedbackContext, _narrowed(), Read the user's answer to the scope echo: the claim to store, or None for no., The claim with the scope the answer named, or None when it named none., Whether a line confirms (True), refuses (False), or says something else (None)., The decision the user was looking at. The mail, never the dataset's labels. (+2 more)

### Community 117 - "Message"
Cohesion: 0.07
Nodes (39): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., The user's own words, consulted before the provider. Wraps another provider:…, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it. (+31 more)

### Community 118 - "test_eval_run.py"
Cohesion: 0.13
Nodes (23): load_script(), Any, Path, The async driver, run to completion., The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, run_eval() (+15 more)

### Community 119 - ".get_instance"
Cohesion: 0.25
Nodes (7): forget_thread(), Access or initialize the singleton PresidioMasker., Drop a thread's token registry and reverse map., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 120 - "LearningConsent"
Cohesion: 0.22
Nodes (5): LearningConsent, datetime, What may be learned, for what purpose, kept how long, and until when., Whether this consent still stands at a moment., One line a transcript can print about why nothing was kept.

### Community 121 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 122 - "first_interrupt_of"
Cohesion: 0.28
Nodes (9): first_interrupt_of(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing(), test_an_approval_releases_the_prepared_action_and_is_learnable() (+1 more)

### Community 123 - "server.py"
Cohesion: 0.25
Nodes (8): dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, ThreadingHTTPServer, webbrowser

### Community 124 - "Style"
Cohesion: 0.33
Nodes (4): What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., Style

### Community 125 - "_context"
Cohesion: 0.50
Nodes (4): _context(), The decision a standing preference is stated in front of., The card is only worth having if the pipeline's own parser reads it as a rule.…, test_every_standing_preference_the_owner_states_is_readable_as_a_rule()

### Community 126 - "SenderIdentity"
Cohesion: 0.29
Nodes (6): Who an email claims to come from, and whether that claim is verified.…, SenderIdentity, History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., test_thread_rejects_a_message_from_another_thread(), test_thread_rejects_duplicate_message_ids()

### Community 130 - "EvalReport"
Cohesion: 0.15
Nodes (7): Disposition, EvalReport, Path, Both lanes, kept apart: one disposition count over everything, two assessments., How a lane's cases were handled, mutually exclusive by construction., Write the report as JSON, naming the file in the error rather than failing mute., The counts, then the denominator they have to add up to.

### Community 131 - "test_explicit_decisions_must_be_flagged_learnable"
Cohesion: 0.29
Nodes (7): parametrize, Empty ids and malformed fields fail at construction, not at use., Silence is not approval": a non-decision claiming the learning flag fails., An explicit decision that disclaims learning is a bug, not a preference., test_explicit_decisions_must_be_flagged_learnable(), test_missing_identity_is_rejected(), test_silence_and_observation_cannot_teach()

### Community 132 - "_action_for"
Cohesion: 0.33
Nodes (6): _action_for(), _clean_label(), Any, Route, The route and action the user asked for, or nothing when they named neither., A folder name as the user wrote it, without the sentence around it.

### Community 135 - "_provider_for"
Cohesion: 0.20
Nodes (11): ClaimStore, DecisionSource, _policy(), _proposing(), _provider_for(), The proposer one name asks for: an endpoint, or an endpoint with Jev routing it., The pipeline's proposer: a rule already confirmed answers before the provider…, Pick the decision source and name it. Labels are a reference mode, not the… (+3 more)

### Community 136 - "mask_for_llm"
Cohesion: 0.50
Nodes (3): PII masking and anonymization package., mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only.

### Community 138 - "_order_key"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

### Community 141 - "_scope_for"
Cohesion: 0.22
Nodes (10): ClaimScope, ScopeAnchor, _from_context(), Resolve the scope from nouns first, and only then from the active item., Words the user used that also appear in the mail they were looking at., _scope_for(), _topic_overlap(), _words() (+2 more)

## Knowledge Gaps
- **35 isolated node(s):** `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `how to reproduce`, `no LLM vs LLM only vs Jev + LLM`, `run a — 15 arrivals, 7 to learn on, 7 cold` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `registry.py`, `test_economics.py`, `test_floor.py`, `ClaimScope`, `ChatRunner`, `HeldOutReport`, `runner.py`, `test_gateway.py`, `persona_demanded_route`, `floor.py`, `test_sim_tools.py`, `ProposalError`, `test_jev.py`, `Drafting`, `Posterior`, `Learner`, `test_events.py`, `Session`, `SimulatedMailbox`, `run_scenario`, `claims.py`, `test_sim.py`, `Lane`, `SafetyVerdict`, `ToolRegistry`, `harness.py`, `test_benign_workplace_clean_pass`, `test_floor_protection.py`, `test_freeze.py`, `test_denominators.py`, `router.py`, `Routing`, `TraceSink`, `Message`, `first_interrupt_of`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `Bucket` connect `Bucket` to `Learner`, `test_floor_protection.py`, `ChatRunner`, `runner.py`, `Message`, `router.py`, `Route`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `ChatRunner` connect `ChatRunner` to `GraphState`, `Case`, `registry.py`, `ClaimStore`, `.start`, `feedback.py`, `run_simulation`, `runner.py`, `test_gateway.py`, `Route`, `Learner`, `Session`, `SimulatedMailbox`, `run_scenario`, `claims.py`, `ReplyTree`, `Lane`, `ToolRegistry`, `agent/state.py`, `test_replay.py`, `TraceSink`, `FeedbackContext`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 146 inferred relationships involving `Route` (e.g. with `dispositions()` and `held_out_report()`) actually correct?**
  _`Route` has 146 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `Lane` (e.g. with `main()` and `CalibrationReport`) actually correct?**
  _`Lane` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 33 INFERRED edges - model-reasoned connections that need verification._