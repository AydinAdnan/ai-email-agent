# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 90 files · ~77,412 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2362 nodes · 5510 edges · 154 communities (113 shown, 41 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 773 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `97711a0e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- route_decision
- graph.py
- evaluate
- ClaimStore
- Session
- feedback.py
- Manifest
- Bucket
- test_feedback_parser.py
- ActionPayload
- test_claim_schema.py
- ChatRunner
- EmailContext
- Handler
- test_ui_session.py
- cli.py
- HeldOutReport
- test_floor.py
- ValueError
- GraphState
- EventValidationError
- test_sim.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- validate_stream
- ProposalGateway
- agent/state.py
- app.js
- ProposalRequest
- drafts.py
- Message
- test_predrafts.py
- trace.py
- Learner
- test_replay.py
- ._run
- mask_for_llm
- PresidioMasker
- .start
- run_typed
- SimulatedMailbox
- claims.py
- schedule
- main
- Case
- test_triage.py
- test_graph_resume.py
- retrieve_style
- Routes
- test_the_default_view_never_shows_the_answer_key
- test_graph.py
- ContextPhoneRecognizer
- OpenAICompatibleProvider
- registry.py
- RememberedProvider
- run_scenario
- Tool
- SentExample
- test_gateway.py
- Thread
- Any
- gateway.py
- plan_deviation
- test_events.py
- safety/__init__.py
- test_cases.py
- test_freeze.py
- run_simulation
- ClaimStore
- masker.py
- get_token_map
- dataset.py
- test_graph_state.py
- DecisionSource
- Block
- .load
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
- EmailEvent
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
- LoopReport
- .proposal_for
- ScoringError
- Cutoffs
- NotifyUser
- parse_proposal
- first_interrupt_of
- FeedbackEvent
- classify_action
- server.py
- harness.py
- record_from_chat
- test_loop.py
- ProposalProvider
- dispositions
- _case_from_mail_row
- LearningConsent
- graph_run
- _check_base64_injection
- test_benign_workplace_clean_pass
- SenderIdentity
- RuntimeError
- Case
- ClaimStore
- IO
- Router
- SimulatedMailbox
- CaptureFixture
- MonkeyPatch
- ProposalProvider
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- sim/__init__.py
- Route
- Any
- datetime
- InterruptHook
- IO
- Queue

## God Nodes (most connected - your core abstractions)
1. `Route` - 102 edges
2. `Router` - 41 edges
3. `Learner` - 41 edges
4. `Bucket` - 40 edges
5. `Message` - 37 edges
6. `ActionPayload` - 36 edges
7. `run_simulation()` - 34 edges
8. `Manifest` - 33 edges
9. `floor_check()` - 32 edges
10. `ClaimStore` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `main()` --uses--> `ScoringError`  [INFERRED]
  src/agent/cli.py → evals/harness.py
- `test_a_record_that_decided_fewer_cases_than_it_processed_is_refused()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py
- `test_a_report_cannot_be_written_where_it_cannot_be_read()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py
- `test_a_route_the_report_does_not_know_is_refused_rather_than_counted()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py

## Import Cycles
- None detected.

## Communities (154 total, 41 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.09
Nodes (24): EventStream, _json_default(), Any, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., An append-only log of arriving events. There is no update, no delete and no…, The canonical JSONL replay log: header line, then one line per arrival., SeededClock (+16 more)

### Community 1 - "route_decision"
Cohesion: 0.07
Nodes (38): EmailContext, Predraft, RoutingRequest, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Decision, email_context_for(), named_route() (+30 more)

### Community 2 - "graph.py"
Cohesion: 0.09
Nodes (40): CompiledStateGraph, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), build_graph() (+32 more)

### Community 3 - "evaluate"
Cohesion: 0.14
Nodes (16): EvalOutcome, evaluate(), _frozen(), main(), Any, LaneView, Path, ProposalProvider (+8 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (32): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., ConsentRequired (+24 more)

### Community 5 - "Session"
Cohesion: 0.20
Nodes (12): Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The four states are the colours on the page, so each card needs the route it…, test_a_session_shows_the_mail_and_takes_a_line() (+4 more)

### Community 6 - "feedback.py"
Cohesion: 0.09
Nodes (38): ClaimScope, datetime, ScopeAnchor, _action_for(), _claim_reading(), _clean_label(), confirm_claim(), confirm_words() (+30 more)

### Community 7 - "Manifest"
Cohesion: 0.10
Nodes (27): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, _case_from_row(), Manifest, ManifestError, Build one case, naming the case on anything the row gets wrong. A bare…, Every case in the dataset, sorted by sequence index, with its digest.…, Build a manifest from parsed rows, rejecting duplicate case ids and splits. (+19 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "test_feedback_parser.py"
Cohesion: 0.11
Nodes (31): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to… (+23 more)

### Community 10 - "ActionPayload"
Cohesion: 0.08
Nodes (36): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated. (+28 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.13
Nodes (26): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), What a session carries when a human is present and typing. Consent is granted…, session_grant(), memory(), preference() (+18 more)

### Community 12 - "ChatRunner"
Cohesion: 0.07
Nodes (35): Bucket, Claim, Decision, FeedbackContext, Reading, ReplyTree, _body_lines(), _bucket_of() (+27 more)

### Community 13 - "EmailContext"
Cohesion: 0.15
Nodes (23): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+15 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "test_ui_session.py"
Cohesion: 0.15
Nodes (15): importlib_util, _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., The run writes the summary a line at a time; the page has to read it as one…, _server() (+7 more)

### Community 16 - "cli.py"
Cohesion: 0.13
Nodes (29): ArgumentParser, ClaimStore, IO, Namespace, build_parser(), data_validate(), eval_all(), _keep_rules() (+21 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.12
Nodes (10): Gate, HeldOutReport, Any, Path, _rate(), A count and its denominator, which is the only honest way to print a rate., A hard gate: a number that has to hold, not a curve that has to trend., The sealed lane: the only place accuracy is measured, and the hard gates. (+2 more)

### Community 18 - "test_floor.py"
Cohesion: 0.07
Nodes (31): pytest, _check_authority_claims(), _check_zero_width_chars(), Scan untrusted email content and headers for prompt injection indicators., Detect presence of invisible zero-width characters used for steganography., Flag authority claims whose backing identity is external or unverifiable. A…, scan(), Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails… (+23 more)

### Community 20 - "GraphState"
Cohesion: 0.13
Nodes (19): Command, _bound(), GraphError, GraphSession, Any, RuntimeError, Hand a node its runtime. The graph only ever sees the state., What resuming a held decision did, or why the answer could not be used. (+11 more)

### Community 21 - "EventValidationError"
Cohesion: 0.31
Nodes (6): DuplicateEventError, EventValidationError, ValueError, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text()

### Community 22 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.14
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.12
Nodes (21): action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Any, The simulated email tools (Phase 3.3). Six tools over one in-memory mailbox:… (+13 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.14
Nodes (29): DraftCode, Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the…, validate_draft(), StrEnum (+21 more)

### Community 26 - "validate_stream"
Cohesion: 0.13
Nodes (19): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), The dataset's answers live on the Case, so a decision path cannot read them., A unique, ascending stream passes., The same case arriving twice would double-count in the report denominators. (+11 more)

### Community 27 - "ProposalGateway"
Cohesion: 0.16
Nodes (20): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., message(), The rules belong to the mail, so a model proposing a quiet route does not win., A small model copies the example it was shown, so the example carries no value., No folder for this mail means a blocked step at the registry, not a made-up one., The floor wins over a confident proposal, which is the whole contract., A provider that answers from a script, so the repair logic is testable. (+12 more)

### Community 28 - "agent/state.py"
Cohesion: 0.11
Nodes (26): Drafting, Routing, The chosen route's expected loss, in handoffs., Record the route the router chose, which is what authorization checks., route(), One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields() (+18 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "ProposalRequest"
Cohesion: 0.14
Nodes (12): ProposalError, ProposalRequest, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Ask the provider, repair once if the answer does not parse, then fail closed., Ask once. A provider that fails in any way is a failed proposal, not a crash. A… (+4 more)

### Community 31 - "drafts.py"
Cohesion: 0.09
Nodes (26): Case, draft_reply(), Drafting, drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+18 more)

### Community 32 - "Message"
Cohesion: 0.11
Nodes (23): Message, One email message, in a thread, in one direction., The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), RuleProvider, amount_in() (+15 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (23): drafting(), held(), Case, Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+15 more)

### Community 34 - "trace.py"
Cohesion: 0.20
Nodes (17): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file. (+9 more)

### Community 35 - "Learner"
Cohesion: 0.06
Nodes (59): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+51 more)

### Community 36 - "test_replay.py"
Cohesion: 0.07
Nodes (36): fixture, hashlib, RuntimeError, Lane, Raised when code reaches across the learning/held-out firewall., Where a case sits relative to learning., SplitViolation, Seeded clock and append-only event stream (Phase 3.2). Replay has to be… (+28 more)

### Community 37 - "._run"
Cohesion: 0.20
Nodes (5): AnswerQueue, LaneView, The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Transcript

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - ".start"
Cohesion: 0.22
Nodes (6): AbstractEventLoop, _background_loop(), Load the lane and begin the run. A failure here is the caller's to report., Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 41 - "run_typed"
Cohesion: 0.10
Nodes (31): arrivals(), dataset_routes(), labelled_routes(), DecisionSource, Path, TraceSink, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order. (+23 more)

### Community 42 - "SimulatedMailbox"
Cohesion: 0.20
Nodes (5): build_registry(), Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., SimulatedMailbox, test_the_registry_refuses_two_tools_with_one_name()

### Community 43 - "claims.py"
Cohesion: 0.09
Nodes (28): _action_words(), _bears_on(), Claim, _claim_from_record(), claim_id_for(), _claim_record(), ClaimScope, Any (+20 more)

### Community 44 - "schedule"
Cohesion: 0.09
Nodes (31): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., One released window: its cases in delivery order, and the seed that ordered it., The window's case ids in the order they will arrive., The ids a case says must arrive before it, from… (+23 more)

### Community 45 - "main"
Cohesion: 0.21
Nodes (13): CaptureFixture, main(), Run both lanes and print the report, so the scorer can be read before it is…, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., test_a_broken_input_stream_ends_the_run_instead_of_hanging(), test_buffered_input_is_recorded_as_corrections_not_answers() (+5 more)

### Community 46 - "Case"
Cohesion: 0.09
Nodes (13): Case, CaseLabels, LaneView, The dataset's ground truth for a case. These are answers: what the case was…, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., The dataset's answer for this case, for scoring and debugging only., Return the lane-bound handle for one lane. (+5 more)

### Community 47 - "test_triage.py"
Cohesion: 0.13
Nodes (17): Direction, StrEnum, Which way a message travelled in its thread., message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+9 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.09
Nodes (30): parametrize, approval_for(), Crash, Crashing, Flaky, Message, Proposal, ProposalGateway (+22 more)

### Community 49 - "retrieve_style"
Cohesion: 0.16
Nodes (21): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from. (+13 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 52 - "test_graph.py"
Cohesion: 0.12
Nodes (26): GraphOutcome, LaneView, ProposalGateway, Router, SimulatedMailbox, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., What a lane through the graph did. (+18 more)

### Community 53 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "registry.py"
Cohesion: 0.07
Nodes (40): ABC, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest() (+32 more)

### Community 56 - "RememberedProvider"
Cohesion: 0.22
Nodes (6): ClaimStore, ProposalProvider, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider

### Community 57 - "run_scenario"
Cohesion: 0.11
Nodes (18): cold_control(), main(), What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it… (+10 more)

### Community 58 - "Tool"
Cohesion: 0.14
Nodes (7): EffectLog, One capability. Small on purpose: check refuses, apply acts., Do the work and say what changed. Only ever called by a commit., What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran., Tool

### Community 59 - "SentExample"
Cohesion: 0.12
Nodes (16): examples_from_row(), How many examples this case allows. The row's ``needs_draft`` is deliberately…, What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., The word the user opens with, borrowed from the best example and cited as such., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+8 more)

### Community 60 - "test_gateway.py"
Cohesion: 0.16
Nodes (16): build_provider(), Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch, SimpleNamespace, The model proposal gateway: untrusted output, one repair, then fail closed., The slice of the OpenAI client the provider uses, capturing the request. (+8 more)

### Community 61 - "Thread"
Cohesion: 0.22
Nodes (9): A conversation: the messages that arrived before this case, oldest first., Thread, EmailEvent, History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread(), test_thread_rejects_a_message_from_another_thread() (+1 more)

### Community 62 - "Any"
Cohesion: 0.20
Nodes (17): Any, _entries(), freeze(), load(), Learner, Path, Router, Freezing what a run learned, so the next one starts where it stopped. Three… (+9 more)

### Community 63 - "gateway.py"
Cohesion: 0.18
Nodes (15): os, _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), Proposal, Model proposal gateway (plan Commit 5.3). A thin provider interface with a… (+7 more)

### Community 64 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 65 - "test_events.py"
Cohesion: 0.12
Nodes (25): FeedbackEvent, FeedbackKind, event(), _feedback(), _load_dataset(), parametrize, Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, Empty ids and malformed fields fail at construction, not at use. (+17 more)

### Community 66 - "safety/__init__.py"
Cohesion: 0.20
Nodes (9): FloorRule, Representation of an audited, immutable safety floor rule., Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, Safety module: floor guardrails, action taxonomy, and injection tripwires., InjectionScanResult, Outcome of scanning text and metadata for prompt injection signals., Assert SafetyVerdict instances are frozen to prevent tampering. (+1 more)

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (63): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+55 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.21
Nodes (13): Learner, Path, Router, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw() (+5 more)

### Community 69 - "run_simulation"
Cohesion: 0.12
Nodes (21): InterruptHook, Learner, Queue, Router, SimulatedMailbox, A hook that hands the waiting decision its lines, and closes input at the end., Any, DecisionSource (+13 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 73 - "dataset.py"
Cohesion: 0.14
Nodes (25): asyncio, base64, collections_abc, dataclasses, enum, The four reference cases, run end to end and printed as transcripts. Each case…, pathlib, re (+17 more)

### Community 74 - "test_graph_state.py"
Cohesion: 0.10
Nodes (28): RuntimeError, The trace could not be written where it was asked to go., Append-only JSONL trace, one line per decision, flushed as it is written., Close the file. Safe to call twice, which an except-block may do., TraceError, TraceSink, message(), Path (+20 more)

### Community 76 - "Block"
Cohesion: 0.18
Nodes (8): Block, classify(), Any, Append one block, with the number the page polls from., Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 77 - ".load"
Cohesion: 0.12
Nodes (20): Load the manifest from a JSONL dataset file, or from plain mail rows., block_of(), ExplodingPolicy, interrupting_case_ids(), Lane, One arrival's text, from its header up to the next arrival., The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case. (+12 more)

### Community 79 - "replay"
Cohesion: 0.12
Nodes (14): datetime, Replay events through a fresh seeded stream., The current simulated time., Move simulated time forward and return the new time., replay(), The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival. (+6 more)

### Community 80 - "run_loop"
Cohesion: 0.20
Nodes (8): LaneView, ClaimStore, ProposalProvider, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Types scripted lines at the decisions that wait for a human. A line handed over…, run_loop(), ScriptedReplies, TraceSink

### Community 83 - "test_denominators.py"
Cohesion: 0.09
Nodes (50): held_out_report(), Score the sealed lane, refusing outright if anything about it could teach. Both…, Route, _decision(), _feedback(), _gold(), Lane, LaneView (+42 more)

### Community 88 - "router.py"
Cohesion: 0.09
Nodes (32): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys… (+24 more)

### Community 98 - "Route"
Cohesion: 0.12
Nodes (37): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, _mask_routes(), Drop every route the floor forbade, so the learner never sees them as options., The four autonomy outcomes a candidate action can be routed to.…, The least autonomous of these routes, which is the one that wins a…, Route, strictest() (+29 more)

### Community 105 - "EmailEvent"
Cohesion: 0.25
Nodes (5): EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…

### Community 116 - "LoopReport"
Cohesion: 0.25
Nodes (5): LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 117 - ".proposal_for"
Cohesion: 0.16
Nodes (12): Message, Proposal, ProposalRequest, _domain(), proposal_from(), Claim, One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one. (+4 more)

### Community 118 - "ScoringError"
Cohesion: 0.14
Nodes (22): Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, load_script(), The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, ScriptedTeaching, Manifest (+14 more)

### Community 119 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 120 - "NotifyUser"
Cohesion: 0.29
Nodes (4): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else.

### Community 121 - "parse_proposal"
Cohesion: 0.15
Nodes (13): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., The tool an action id means, or the id itself when no tool holds it., tool_for_action(), parametrize, One vocabulary: the offline stand-in cannot drift from the model's schema., The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses() (+5 more)

### Community 122 - "first_interrupt_of"
Cohesion: 0.24
Nodes (11): first_interrupt_of(), gold_route(), Route, The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed() (+3 more)

### Community 124 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 125 - "server.py"
Cohesion: 0.20
Nodes (10): dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., Point the server at a session, which is what the tests and the page both need., serve(), set_session(), http_server (+2 more)

### Community 126 - "harness.py"
Cohesion: 0.10
Nodes (23): argparse, ask_curve(), Block, calibration_report(), CalibrationReport, EvalReport, LaneView, The two-lane scorer: what the agent did, counted where it happened. The report… (+15 more)

### Community 127 - "record_from_chat"
Cohesion: 0.17
Nodes (11): LaneRecord, Lane, What one lane run recorded, in the shape the report reads. Built from a chat…, Refuse a record whose counts cannot add up to what the run processed., Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., record_from_chat(), record_from_graph() (+3 more)

### Community 128 - "test_loop.py"
Cohesion: 0.22
Nodes (15): asked(), _drained(), loop(), Queue, Nothing hangs on a prompt the script never feeds: it is told a line that does…, A named case still waits for the second line, so an unanswered echo stores…, test_a_decision_the_script_does_not_answer_is_passed_on(), test_a_named_entry_is_typed_at_the_case_it_names() (+7 more)

### Community 129 - "ProposalProvider"
Cohesion: 0.33
Nodes (4): Protocol, ProposalProvider, A source of untrusted proposal text., Return raw proposal text for one request.

### Community 130 - "dispositions"
Cohesion: 0.15
Nodes (9): Disposition, dispositions(), How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to., Count routes into the three dispositions, refusing a route nobody defined., The plan's rule: three dispositions, one per case, adding up to all of them., A fifth route is a bug, and an uncounted case is the same bug wearing a number., test_a_route_the_report_does_not_know_is_refused_rather_than_counted() (+1 more)

### Community 131 - "_case_from_mail_row"
Cohesion: 0.12
Nodes (18): Direction, SenderIdentity, _attachment(), _case_from_mail_row(), event_from_row(), _message(), EmailEvent, Canonicalize one dataset row into an EmailEvent. (+10 more)

### Community 132 - "LearningConsent"
Cohesion: 0.40
Nodes (3): LearningConsent, What may be learned, for what purpose, kept how long, and until when., Whether this consent still stands at a moment.

### Community 133 - "graph_run"
Cohesion: 0.14
Nodes (15): DecisionSource, GraphSession, ProposalGateway, The pair's name, so a run says where a proposal could have come from., graph_run(), _policy(), _proposing(), ProposalProvider (+7 more)

### Community 134 - "_check_base64_injection"
Cohesion: 0.50
Nodes (4): _check_base64_injection(), _decode_base64_candidate(), Return the decoded text of a base64 candidate, or None when it is not valid…, Inspect text for embedded base64 payloads that decode into control instructions.

### Community 135 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 146 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 147 - "sim/__init__.py"
Cohesion: 0.15
Nodes (12): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, GoldPolicy, Choose the dataset's route when the floor still allows it, else escalate. The…, _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A reconstructed thread: its roots, plus every message's children by parent id.… (+4 more)

## Knowledge Gaps
- **14 isolated node(s):** `email-autonomy-agent`, `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `Message`, `parse_proposal`, `safety/__init__.py`, `Learner`, `test_events.py`, `route_decision`, `test_feedback_parser.py`, `dataset.py`, `claims.py`, `test_claim_schema.py`, `EmailContext`, `test_graph_state.py`, `test_floor.py`, `test_sim_tools.py`, `router.py`, `run_scenario`, `ProposalGateway`, `gateway.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `Claim` connect `claims.py` to `Route`, `Learner`, `ClaimStore`, `feedback.py`, `test_feedback_parser.py`, `test_claim_schema.py`, `run_scenario`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `route_decision`, `run_simulation`, `._run`, `.start`, `dataset.py`, `Block`, `ChatRunner`, `Handler`, `test_ui_session.py`, `server.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 86 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 86 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Bucket` (e.g. with `Learner` and `Router`) actually correct?**
  _`Bucket` has 16 INFERRED edges - model-reasoned connections that need verification._