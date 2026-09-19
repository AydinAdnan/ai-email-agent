# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 93 files · ~80,095 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2437 nodes · 5671 edges · 155 communities (109 shown, 46 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 775 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fc414a37`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- policy.py
- graph.py
- run_eval.py
- ClaimStore
- test_economics.py
- feedback.py
- Manifest
- Bucket
- test_feedback_parser.py
- ActionPayload
- ClaimScope
- runner.py
- EmailContext
- Handler
- Session
- eval_all
- harness.py
- test_floor.py
- ValueError
- GraphSession
- EventValidationError
- test_sim.py
- test_sim_tools.py
- Effect
- test_draft_validation.py
- Ledger
- test_gateway.py
- agent/state.py
- app.js
- ProposalRequest
- drafts.py
- agent/triage.py
- test_predrafts.py
- RoutingRequest
- Learner
- test_replay.py
- session.py
- mask_for_llm
- PresidioMasker
- _split_problems
- arrivals
- SimulatedMailbox
- claims.py
- Case
- main
- LaneView
- test_triage.py
- test_graph_resume.py
- retrieve_style
- Routes
- run_typed
- test_graph.py
- ContextPhoneRecognizer
- OpenAICompatibleProvider
- registry.py
- .load
- run_canonical.py
- EffectLog
- SentExample
- FakeCompletions
- Thread
- Any
- gateway.py
- Tool
- test_events.py
- floor.py
- test_cases.py
- test_freeze.py
- run_simulation
- ClaimStore
- masker.py
- get_token_map
- events.py
- trace.py
- DecisionSource
- CaseReport
- view
- IO
- replay
- run_loop
- Any
- Workflow: graphify
- test_denominators.py
- email-autonomy-agent
- router.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- StrEnum
- parametrize
- ProposalGateway
- replay.py
- Any
- datetime
- InterruptHook
- Queue
- datetime
- ValueError
- parametrize
- RuntimeError
- StrEnum
- fixture
- SafetyVerdict
- .predraft
- test_eval_run.py
- Cutoffs
- email_tools.py
- valid
- first_interrupt_of
- FeedbackEvent
- classify_action
- dataset.py
- EvalReport
- record_from_chat
- test_loop.py
- ProposalProvider
- dispositions
- _case_from_mail_row
- datetime
- ProposalGateway
- Any
- test_benign_workplace_clean_pass
- RuntimeError
- RuntimeError
- Case
- ClaimStore
- IO
- Router
- SimulatedMailbox
- CaptureFixture
- MonkeyPatch
- ProposalProvider
- MonkeyPatch
- _order_key
- Route
- parametrize
- Any
- datetime
- InterruptHook
- IO
- Queue

## God Nodes (most connected - your core abstractions)
1. `Route` - 85 edges
2. `Learner` - 42 edges
3. `Router` - 41 edges
4. `Bucket` - 40 edges
5. `ActionPayload` - 36 edges
6. `Lane` - 34 edges
7. `run_simulation()` - 34 edges
8. `floor_check()` - 32 edges
9. `ClaimStore` - 31 edges
10. `Manifest` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_a_model_nobody_prices_is_unpriced_rather_than_free()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_an_empty_run_reports_zero_rather_than_dividing_by_it()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_the_deflection_rate_counts_arrivals_not_calls()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_the_table_names_the_stage_the_model_and_the_price()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py

## Import Cycles
- None detected.

## Communities (155 total, 46 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.09
Nodes (20): datetime, A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., SeededClock, An arrival numbered before the last one is out of order, not a new arrival., Append-only is structural: there is no update, delete or reorder., Each arrival is stamped by the clock, one tick apart. (+12 more)

### Community 1 - "policy.py"
Cohesion: 0.09
Nodes (34): RoutingRequest, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Decision, GoldPolicy, named_route(), _params_with_case(), ProposalPolicy (+26 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (41): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), _bound(), build_graph() (+33 more)

### Community 3 - "run_eval.py"
Cohesion: 0.10
Nodes (29): CalibrationReport, The lane the user sat in front of: what they typed, and what it cost them., Lines the user typed: answers to a prompt, and corrections after one., Raised when a run cannot be scored as asked, rather than scored wrongly., Join the two lanes into the report, refusing a pair that cannot be one run., ScoringError, two_lane_report(), EvalOutcome (+21 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (39): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Capability, ConsentRequired (+31 more)

### Community 5 - "test_economics.py"
Cohesion: 0.11
Nodes (27): asyncio, MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price., No call, no tokens, and the deflection is what makes the saving countable., Two tables for one run is how a cost report starts under-reporting., The remembered provider sits between the gateway and the model, and holds no… (+19 more)

### Community 6 - "feedback.py"
Cohesion: 0.09
Nodes (38): ClaimScope, datetime, ScopeAnchor, _action_for(), _claim_reading(), _clean_label(), confirm_claim(), confirm_words() (+30 more)

### Community 7 - "Manifest"
Cohesion: 0.10
Nodes (25): _case_from_row(), Manifest, ManifestError, Build one case, naming the case on anything the row gets wrong. A bare…, Every case in the dataset, sorted by sequence index, with its digest.…, Build a manifest from parsed rows, rejecting duplicate case ids and splits., Build a manifest from plain mail: sender, recipients, subject and body. A…, Return the lane-bound handle for one lane. (+17 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "test_feedback_parser.py"
Cohesion: 0.11
Nodes (31): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to… (+23 more)

### Community 10 - "ActionPayload"
Cohesion: 0.08
Nodes (36): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated. (+28 more)

### Community 11 - "ClaimScope"
Cohesion: 0.12
Nodes (25): claim_id_for(), ClaimScope, A stable id for the same claim said twice, so it is never stored twice., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., memory(), preference() (+17 more)

### Community 12 - "runner.py"
Cohesion: 0.06
Nodes (42): Bucket, Claim, Decision, FeedbackContext, Reading, ReplyTree, _address(), _body_lines() (+34 more)

### Community 13 - "EmailContext"
Cohesion: 0.13
Nodes (24): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+16 more)

### Community 14 - "Handler"
Cohesion: 0.14
Nodes (11): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one. (+3 more)

### Community 15 - "Session"
Cohesion: 0.08
Nodes (30): Point the server at a session, which is what the tests and the page both need., set_session(), importlib_util, pytest, Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session (+22 more)

### Community 16 - "eval_all"
Cohesion: 0.10
Nodes (19): main(), Run the lanes, then print what they cost., The pair's name, so a run says where a proposal could have come from., data_validate(), eval_all(), main(), Print what a case set holds and everything wrong with it., Teach the calibration lane, freeze it, and score the sealed lane once. (+11 more)

### Community 17 - "harness.py"
Cohesion: 0.11
Nodes (14): ask_curve(), Block, Gate, HeldOutReport, _rate(), The two-lane scorer: what the agent did, counted where it happened. The report…, The interruption curve: how many cases each block of the lane needed the user…, A count and its denominator, which is the only honest way to print a rate. (+6 more)

### Community 18 - "test_floor.py"
Cohesion: 0.06
Nodes (30): Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles., An authority claim we cannot tie to a sender address is unresolved, not trusted., An in-org sender claiming an internal role is not an authority spoof. (+22 more)

### Community 20 - "GraphSession"
Cohesion: 0.15
Nodes (14): Command, GraphError, GraphSession, Any, RuntimeError, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human. (+6 more)

### Community 21 - "EventValidationError"
Cohesion: 0.18
Nodes (10): DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., Raised when a stream is not in ascending sequence order., Who an email claims to come from, and whether that claim is verified.… (+2 more)

### Community 22 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "Effect"
Cohesion: 0.17
Nodes (12): ArchiveEmail, _email_id(), LabelEmail, Any, Files a message out of the inbox., A send that validates like a real one and never leaves the mailbox. Recipients…, Applies one label to one message., SendEmail (+4 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.14
Nodes (29): DraftCode, Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the…, validate_draft(), StrEnum (+21 more)

### Community 26 - "Ledger"
Cohesion: 0.09
Nodes (13): The offline provider: proposes from triage, no network, deterministic. It is a…, RuleProvider, Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., Most-spending stage first, so the table reads as a ranking., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that…, A process's spend: every provider call, and every arrival it never had to ask… (+5 more)

### Community 27 - "test_gateway.py"
Cohesion: 0.08
Nodes (41): MonkeyPatch, build_provider(), ProposalError, ProposalGateway, Raised when a provider cannot produce a usable proposal, after one repair., Turns provider text into a validated proposal, with one repair attempt., Resolve a provider by name, refusing one that cannot run here. The model comes…, BrokenProvider (+33 more)

### Community 28 - "agent/state.py"
Cohesion: 0.08
Nodes (35): Drafting, Routing, The chosen route's expected loss, in handoffs., Record the route the router chose, which is what authorization checks., route(), One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields() (+27 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "ProposalRequest"
Cohesion: 0.12
Nodes (12): Protocol, ProposalProvider, ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., A source of untrusted proposal text., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A… (+4 more)

### Community 31 - "drafts.py"
Cohesion: 0.09
Nodes (26): Case, draft_reply(), Drafting, drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+18 more)

### Community 32 - "agent/triage.py"
Cohesion: 0.13
Nodes (18): Message, One email message, in a thread, in one direction., A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _first_intent(), intents_matching() (+10 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (23): drafting(), held(), Case, Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+15 more)

### Community 34 - "RoutingRequest"
Cohesion: 0.15
Nodes (9): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., RoutingRequest, Nobody has said anything anywhere: silence is not on the ballot and asking wins. (+1 more)

### Community 35 - "Learner"
Cohesion: 0.09
Nodes (38): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+30 more)

### Community 36 - "test_replay.py"
Cohesion: 0.08
Nodes (32): fixture, Lane, Where a case sits relative to learning., manifest(), Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, Counts per split and per lane, with the dataset's real sizes., A replay can name the exact dataset it ran against., Ground truth has to be reachable by scoring and out of reach of a decision. (+24 more)

### Community 37 - "session.py"
Cohesion: 0.09
Nodes (17): AbstractEventLoop, AnswerQueue, _background_loop(), Block, classify(), Any, LaneView, Load the lane and begin the run. A failure here is the caller's to report. (+9 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "_split_problems"
Cohesion: 0.22
Nodes (10): DatasetProblem, One thing the case set gets wrong, named so it can be found and fixed., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender…, Check one row's fields and enums. Returns its problems and its warnings., The cross-row checks: ids and ordering, and nothing landing in two lanes., _row_problems(), _scenario() (+2 more)

### Community 41 - "arrivals"
Cohesion: 0.15
Nodes (19): arrivals(), dataset_routes(), labelled_routes(), The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints., The eval curve is built from these two, so they have to be the run's own record., The plan's check, against the labels: only ask-first and escalate lines wait. (+11 more)

### Community 42 - "SimulatedMailbox"
Cohesion: 0.22
Nodes (4): CreateDraft, Writes a private draft. Reversible, and never a send., Everything a commit can change, and nothing a prepare can., SimulatedMailbox

### Community 43 - "claims.py"
Cohesion: 0.10
Nodes (23): enum, _action_words(), _bears_on(), Claim, _claim_from_record(), _claim_record(), ClaimError, Any (+15 more)

### Community 44 - "Case"
Cohesion: 0.08
Nodes (38): Case, CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., The dataset's answer for this case, for scoring and debugging only., Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, _dependencies_first() (+30 more)

### Community 45 - "main"
Cohesion: 0.32
Nodes (8): CaptureFixture, main(), Run both lanes and print the report, so the scorer can be read before it is…, test_cli_refuses_to_open_the_sealed_lane(), test_cli_replays_the_fixture(), test_cli_requires_a_subcommand(), test_cli_seed_flag_changes_the_replay_digest(), test_cli_show_labels_flag_is_off_by_default()

### Community 46 - "LaneView"
Cohesion: 0.14
Nodes (8): RuntimeError, LaneView, Raised when code reaches across the learning/held-out firewall., A lane-bound handle over the manifest. A view can only open cases in its own…, Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., SplitViolation

### Community 47 - "test_triage.py"
Cohesion: 0.14
Nodes (16): amount_in(), The largest amount mentioned in a text, as a float., message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker() (+8 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.09
Nodes (30): parametrize, approval_for(), Crash, Crashing, Flaky, Message, Proposal, ProposalGateway (+22 more)

### Community 49 - "retrieve_style"
Cohesion: 0.16
Nodes (21): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from. (+13 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "run_typed"
Cohesion: 0.17
Nodes (13): DecisionSource, Path, TraceSink, Sender, subject and body are inputs in production; labels are only answers.…, On a real run: one line per arrival, and no mail text in any of them., Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines…, run_typed(), test_a_traced_run_writes_the_decision_and_never_the_mail() (+5 more)

### Community 52 - "test_graph.py"
Cohesion: 0.11
Nodes (28): langgraph_checkpoint_memory, GraphOutcome, LaneView, ProposalGateway, Router, SimulatedMailbox, TraceSink, Walk a lane through the graph, one decision per checkpoint thread. (+20 more)

### Community 53 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.17
Nodes (8): Endpoint, OpenAICompatibleProvider, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK., Ask the model for one proposal, off the event loop.

### Community 55 - "registry.py"
Cohesion: 0.07
Nodes (39): Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest(), _notify_text() (+31 more)

### Community 56 - ".load"
Cohesion: 0.20
Nodes (10): Load the manifest from a JSONL dataset file, or from plain mail rows., test_a_missing_fixture_is_reported_not_raised_raw(), block_of(), interrupting_case_ids(), One arrival's text, from its header up to the next arrival., Fixture cases whose gold route asks the user, in delivery order., test_a_correction_typed_at_a_prompt_binds_to_that_decision(), test_a_reply_prompt_is_reported_for_the_case_that_waits() (+2 more)

### Community 57 - "run_canonical.py"
Cohesion: 0.06
Nodes (37): cold_control(), main(), one_case_view(), The four reference cases, run end to end and printed as transcripts. Each case…, What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for. (+29 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "SentExample"
Cohesion: 0.12
Nodes (16): examples_from_row(), How many examples this case allows. The row's ``needs_draft`` is deliberately…, What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., The word the user opens with, borrowed from the best example and cited as such., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+8 more)

### Community 60 - "FakeCompletions"
Cohesion: 0.40
Nodes (4): fake_client(), FakeCompletions, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request.

### Community 61 - "Thread"
Cohesion: 0.22
Nodes (9): A conversation: the messages that arrived before this case, oldest first., Thread, EmailEvent, History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread(), test_thread_rejects_a_message_from_another_thread() (+1 more)

### Community 62 - "Any"
Cohesion: 0.20
Nodes (17): Any, _entries(), freeze(), load(), Learner, Path, Router, Freezing what a run learned, so the next one starts where it stopped. Three… (+9 more)

### Community 63 - "gateway.py"
Cohesion: 0.12
Nodes (28): Message, os, _attribute(), _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route() (+20 more)

### Community 64 - "Tool"
Cohesion: 0.25
Nodes (6): ABC, Read-only: returns the message it was pointed at., ReadEmail, One capability. Small on purpose: check refuses, apply acts., Do the work and say what changed. Only ever called by a commit., Tool

### Community 65 - "test_events.py"
Cohesion: 0.08
Nodes (41): FeedbackEvent, FeedbackKind, Reject a stream that repeats a case or message, or drifts out of order. Order…, validate_stream(), _event(), _feedback(), _load_dataset(), parametrize (+33 more)

### Community 66 - "floor.py"
Cohesion: 0.10
Nodes (26): base64, re, _eval_plan_deviation(), FloorRule, Safety Floor — Pure-function deterministic guardrails. FLOOR_VERSION = "1.0"…, Representation of an audited, immutable safety floor rule., FLR-INJ-002: Actions deviating from pre-committed plan must be escalated., The least autonomous of these routes, which is the one that wins a… (+18 more)

### Community 67 - "test_cases.py"
Cohesion: 0.09
Nodes (48): Path, Check a case set's counts, enums and splits before anything is asked to run it.…, validate_cases(), _codes(), _extra(), Path, The case set's own checks: counts, enums, and nothing in two lanes. ``wajo data…, A thread carries its own history, so a repeat reveals an earlier lane's mail. (+40 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.20
Nodes (14): event(), Learner, Path, Router, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught() (+6 more)

### Community 69 - "run_simulation"
Cohesion: 0.07
Nodes (47): ClaimStore, DecisionSource, GraphSession, InterruptHook, IO, Learner, Namespace, Queue (+39 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 73 - "events.py"
Cohesion: 0.09
Nodes (36): dataclasses, EmailContext, Direction, StrEnum, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, Which way a message travelled in its thread., email_context_for(), floor_verdict_for() (+28 more)

### Community 74 - "trace.py"
Cohesion: 0.08
Nodes (38): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+30 more)

### Community 76 - "CaseReport"
Cohesion: 0.25
Nodes (3): CaseReport, What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails.

### Community 77 - "view"
Cohesion: 0.14
Nodes (15): ExplodingPolicy, Lane, The lane is delivered window by window, not in the dataset's sequence order., A piped stream has no prompt to answer, so its lines are corrections. Reading…, A decision source that fails, to check the failure names its case., If the read fails, the prompts must see end of input, not wait forever., Fixture case ids in the order the windows deliver them., scheduled_case_ids() (+7 more)

### Community 79 - "replay"
Cohesion: 0.17
Nodes (12): Replay events through a fresh seeded stream., replay(), The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival., The log's order is the dataset's sequence order, not file order., A shuffled file replays identically, because order is sequence_index., test_a_different_seed_changes_the_log() (+4 more)

### Community 80 - "run_loop"
Cohesion: 0.11
Nodes (13): LaneView, LoopReport, ClaimStore, ProposalProvider, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Types scripted lines at the decisions that wait for a human. A line handed over…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet. (+5 more)

### Community 83 - "test_denominators.py"
Cohesion: 0.09
Nodes (52): calibration_report(), held_out_report(), Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both…, Route, _decision(), _feedback(), _gold() (+44 more)

### Community 88 - "router.py"
Cohesion: 0.13
Nodes (25): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+17 more)

### Community 98 - "Route"
Cohesion: 0.17
Nodes (29): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, The four autonomy outcomes a candidate action can be routed to.…, Route, case(), feedback(), _hints(), The plan's check: the floor is not weighed against a preference, it is applied… (+21 more)

### Community 105 - "replay.py"
Cohesion: 0.11
Nodes (15): hashlib, EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., EventStream, _json_default(), Any, Seeded clock and append-only event stream (Phase 3.2). Replay has to be… (+7 more)

### Community 116 - "SafetyVerdict"
Cohesion: 0.40
Nodes (5): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, Assert SafetyVerdict instances are frozen to prevent tampering., test_verdict_immutability(), verdict()

### Community 118 - "test_eval_run.py"
Cohesion: 0.23
Nodes (15): Manifest, evaluate(), mini_manifest(), mini_script(), Path, The eval run: teach the learning lane, freeze it, then score the sealed lane…, The first few committed rows of one split, so the test runs on the real case…, A tiny two-lane manifest built from the committed rows. The adversarial rows… (+7 more)

### Community 119 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 120 - "email_tools.py"
Cohesion: 0.15
Nodes (11): action_vocabulary(), Draft, Notification, NotifyUser, The simulated email tools (Phase 3.3). Six tools over one in-memory mailbox:…, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else., The tool an action id means, or the id itself when no tool holds it. (+3 more)

### Community 121 - "valid"
Cohesion: 0.23
Nodes (12): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., The net under the gate: a proposal from some other path still cannot land…, One vocabulary: the offline stand-in cannot drift from the model's schema., The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses(), test_a_valid_answer_parses(), test_an_action_nothing_implements_resolves_to_itself() (+4 more)

### Community 122 - "first_interrupt_of"
Cohesion: 0.24
Nodes (11): first_interrupt_of(), gold_route(), Route, The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed() (+3 more)

### Community 124 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 125 - "dataset.py"
Cohesion: 0.14
Nodes (20): argparse, collections_abc, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve() (+12 more)

### Community 126 - "EvalReport"
Cohesion: 0.17
Nodes (8): EvalReport, Any, LaneView, Path, Both lanes, kept apart: one disposition count over everything, two assessments., Write the report as JSON, naming the file in the error rather than failing mute., Walk both lanes with nobody at the keyboard, and score what they did. Input is…, run_two_lanes()

### Community 127 - "record_from_chat"
Cohesion: 0.17
Nodes (11): LaneRecord, Lane, What one lane run recorded, in the shape the report reads. Built from a chat…, Refuse a record whose counts cannot add up to what the run processed., Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., record_from_chat(), record_from_graph() (+3 more)

### Community 128 - "test_loop.py"
Cohesion: 0.13
Nodes (24): ArgumentParser, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), asked(), _drained(), loop() (+16 more)

### Community 130 - "dispositions"
Cohesion: 0.15
Nodes (9): Disposition, dispositions(), How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to., Count routes into the three dispositions, refusing a route nobody defined., The plan's rule: three dispositions, one per case, adding up to all of them., A fifth route is a bug, and an uncounted case is the same bug wearing a number., test_a_route_the_report_does_not_know_is_refused_rather_than_counted() (+1 more)

### Community 131 - "_case_from_mail_row"
Cohesion: 0.16
Nodes (14): Direction, SenderIdentity, _attachment(), _case_from_mail_row(), event_from_row(), _message(), EmailEvent, Canonicalize one dataset row into an EmailEvent. (+6 more)

### Community 132 - "datetime"
Cohesion: 0.33
Nodes (3): datetime, Whether this consent still stands at a moment., One line a transcript can print about why nothing was kept.

### Community 135 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 147 - "_order_key"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

## Knowledge Gaps
- **14 isolated node(s):** `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES`, `Silence is not approval` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `test_events.py`, `RoutingRequest`, `Learner`, `floor.py`, `test_feedback_parser.py`, `events.py`, `claims.py`, `ClaimScope`, `EmailContext`, `test_floor.py`, `SafetyVerdict`, `test_sim_tools.py`, `router.py`, `run_canonical.py`, `.load`, `agent/state.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `policy.py`, `run_simulation`, `session.py`, `runner.py`, `Handler`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `PresidioMasker` connect `PresidioMasker` to `get_token_map`, `ContextPhoneRecognizer`, `masker.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 71 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 71 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Bucket` (e.g. with `Learner` and `Router`) actually correct?**
  _`Bucket` has 16 INFERRED edges - model-reasoned connections that need verification._