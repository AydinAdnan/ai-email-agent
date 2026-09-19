# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 93 files · ~81,965 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2466 nodes · 5809 edges · 166 communities (110 shown, 56 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 814 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `adba3333`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- policy.py
- graph.py
- evaluate
- ClaimStore
- test_economics.py
- feedback.py
- ManifestError
- Bucket
- test_feedback_parser.py
- test_floor.py
- ClaimScope
- ChatRunner
- floor.py
- Handler
- pytest
- ProposalGateway
- HeldOutReport
- injection.py
- ValueError
- RuleProvider
- validate_stream
- test_sim.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- .render
- test_gateway.py
- agent/state.py
- app.js
- ProposalRequest
- drafts.py
- Message
- test_predrafts.py
- Posterior
- Learner
- test_replay.py
- ._run
- mask_for_llm
- PresidioMasker
- Session
- arrivals
- _feedback
- Claim
- run_simulation
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
- drafting_for
- SimpleNamespace
- .proposal_for
- Any
- agent/triage.py
- calibration_report
- test_events.py
- plan_deviation
- validate_cases
- test_freeze.py
- IO
- ClaimStore
- masker.py
- get_token_map
- Router
- trace.py
- DecisionSource
- RememberedProvider
- view
- IO
- .state
- test_loop.py
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
- EventStream
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
- Block
- test_eval_run.py
- Cutoffs
- _background_loop
- valid
- interrupting_case_ids
- FeedbackEvent
- classify_action
- dataset.py
- test_every_dataset_route_parses_without_an_adapter
- record_from_chat
- build_parser
- ProposalProvider
- dispositions
- _case_from_mail_row
- claims.py
- ProposalGateway
- serve
- test_a_strangers_instructions_fence_every_route_whatever_the_action
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
- Validation
- Any
- datetime
- InterruptHook
- IO
- Queue
- .matching
- EmailContext
- StrEnum
- Case
- Proposal
- ProposalGateway
- ProposalProvider
- Route
- Router
- SafetyVerdict
- Triage

## God Nodes (most connected - your core abstractions)
1. `Route` - 129 edges
2. `ActionPayload` - 45 edges
3. `Learner` - 42 edges
4. `floor_check()` - 41 edges
5. `Bucket` - 41 edges
6. `Router` - 41 edges
7. `ProposalGateway` - 34 edges
8. `Lane` - 34 edges
9. `run_simulation()` - 34 edges
10. `ClaimStore` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_a_second_failure_fails_closed()` --uses--> `ProposalError`  [INFERRED]
  tests/test_gateway.py → src/agent/gateway.py
- `test_a_usage_object_that_arrives_as_a_mapping_reads_the_same()` --uses--> `ProposalRequest`  [INFERRED]
  tests/eval/test_economics.py → src/agent/gateway.py
- `test_a_wrapper_that_hides_the_provider_does_not_split_the_meter()` --uses--> `ProposalRequest`  [INFERRED]
  tests/eval/test_economics.py → src/agent/gateway.py

## Import Cycles
- None detected.

## Communities (166 total, 56 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.10
Nodes (18): datetime, A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., SeededClock, An arrival numbered before the last one is out of order, not a new arrival., Each arrival is stamped by the clock, one tick apart., Same seed, same time; different seed, different start. (+10 more)

### Community 1 - "policy.py"
Cohesion: 0.10
Nodes (29): Case, cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, Predraft, Router, RoutingRequest, persona_demanded_route(), Proposal (+21 more)

### Community 2 - "graph.py"
Cohesion: 0.06
Nodes (59): Command, CompiledStateGraph, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled() (+51 more)

### Community 3 - "evaluate"
Cohesion: 0.17
Nodes (15): evaluate(), _frozen(), main(), Any, LaneView, Path, ProposalProvider, What the run did, in the order a reader wants it: provenance, then the numbers. (+7 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (33): ClaimStore, Path, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once. (+25 more)

### Community 5 - "test_economics.py"
Cohesion: 0.09
Nodes (30): Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price. (+22 more)

### Community 6 - "feedback.py"
Cohesion: 0.09
Nodes (36): ClaimScope, datetime, ScopeAnchor, _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext (+28 more)

### Community 7 - "ManifestError"
Cohesion: 0.15
Nodes (15): _case_from_row(), ManifestError, Build one case, naming the case on anything the row gets wrong. A bare…, Build a manifest from parsed rows, rejecting duplicate case ids and splits., Build a manifest from plain mail: sender, recipients, subject and body. A…, Raised when the dataset itself violates the manifest schema., A bare KeyError says nothing about which of the cases is malformed., Labels are not needed to arrive, only to grade, so the failure lands there. (+7 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "test_feedback_parser.py"
Cohesion: 0.12
Nodes (28): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a…, The one reading the parser will not assume is the one it stores only when said., A claim has to name the mail it came from, so a rule stated with nothing in… (+20 more)

### Community 10 - "test_floor.py"
Cohesion: 0.07
Nodes (56): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate. (+48 more)

### Community 11 - "ClaimScope"
Cohesion: 0.11
Nodes (28): ClaimError, ClaimScope, ValueError, Raised when a claim is underspecified, or about something never stored., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., _require_text() (+20 more)

### Community 12 - "ChatRunner"
Cohesion: 0.07
Nodes (34): Bucket, Claim, Decision, FeedbackContext, Reading, ReplyTree, _body_lines(), _bucket_of() (+26 more)

### Community 13 - "floor.py"
Cohesion: 0.15
Nodes (26): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+18 more)

### Community 14 - "Handler"
Cohesion: 0.21
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one.

### Community 15 - "pytest"
Cohesion: 0.14
Nodes (16): importlib_util, pytest, _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., The run writes the summary a line at a time; the page has to read it as one… (+8 more)

### Community 16 - "ProposalGateway"
Cohesion: 0.16
Nodes (15): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, router, route out., A small model copies the example it was shown, so the example carries no value., No folder for this mail means a blocked step at the registry, not a made-up one., The floor wins over a confident proposal, which is the whole contract., A provider that answers from a script, so the repair logic is testable. (+7 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.08
Nodes (19): CalibrationReport, EvalReport, Gate, HeldOutReport, Any, Path, _rate(), A count and its denominator, which is the only honest way to print a rate. (+11 more)

### Community 18 - "injection.py"
Cohesion: 0.07
Nodes (33): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+25 more)

### Community 20 - "RuleProvider"
Cohesion: 0.15
Nodes (16): The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., RuleProvider, A table that hid the rules provider would show a run spending nothing and doing…, test_the_offline_provider_is_counted_and_costs_nothing(), message(), The noun decides: 'the Redis sharding key' is a field, and escalating it is…, The ask shape decides too: 'consider changing your password' is advice. (+8 more)

### Community 21 - "validate_stream"
Cohesion: 0.17
Nodes (12): DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., Raised when a stream is not in ascending sequence order. (+4 more)

### Community 22 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, Reconstruct one case's thread, bounded by the reply-tree caps., thread_tree_for(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.13
Nodes (29): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+21 more)

### Community 24 - "email_tools.py"
Cohesion: 0.07
Nodes (32): action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser (+24 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.14
Nodes (30): DraftCode, Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the…, source_text() (+22 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (10): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+2 more)

### Community 27 - "test_gateway.py"
Cohesion: 0.10
Nodes (26): main(), Run the lanes, then print what they cost., MonkeyPatch, SimpleNamespace, build_provider(), ProposalError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes… (+18 more)

### Community 28 - "agent/state.py"
Cohesion: 0.10
Nodes (25): Drafting, Routing, The chosen route's expected loss, in handoffs., Record the route the router chose, which is what authorization checks., route(), draft_fields(), hint_fields(), _plain() (+17 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "ProposalRequest"
Cohesion: 0.15
Nodes (9): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, A proposer that has to guess a tool name from a dataset id guesses wrong., test_the_prompt_names_every_action_and_what_it_needs(), A model in the shape of the provider protocol, answering from a script. (+1 more)

### Community 31 - "drafts.py"
Cohesion: 0.12
Nodes (22): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, What style the draft may borrow, and how the archive was narrowed to it., One line naming what was kept and why, for a transcript. (+14 more)

### Community 32 - "Message"
Cohesion: 0.11
Nodes (20): LaneView, Walk both lanes with nobody at the keyboard, and score what they did. Input is…, run_two_lanes(), Message, One email message, in a thread, in one direction., A conversation: the messages that arrived before this case, oldest first., Thread, A reconstructed thread: its roots, plus every message's children by parent id.… (+12 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (23): drafting(), held(), Case, Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+15 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.10
Nodes (33): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+25 more)

### Community 36 - "test_replay.py"
Cohesion: 0.07
Nodes (39): fixture, Lane, Every case in one lane, in sequence order., Where a case sits relative to learning., Replay events through a fresh seeded stream., replay(), Load the lane and begin the run. A failure here is the caller's to report., Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:… (+31 more)

### Community 37 - "._run"
Cohesion: 0.20
Nodes (5): AnswerQueue, LaneView, The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Transcript

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Session"
Cohesion: 0.17
Nodes (14): Point the server at a session, which is what the tests and the page both need., set_session(), Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable… (+6 more)

### Community 41 - "arrivals"
Cohesion: 0.13
Nodes (21): arrivals(), block_of(), dataset_routes(), labelled_routes(), The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints., One arrival's text, from its header up to the next arrival. (+13 more)

### Community 42 - "_feedback"
Cohesion: 0.16
Nodes (15): FeedbackEvent, FeedbackKind, event(), _feedback(), parametrize, Empty ids and malformed fields fail at construction, not at use., Each kind survives construction with explicit_for_learning intact., Silence is not approval": a non-decision claiming the learning flag fails. (+7 more)

### Community 43 - "Claim"
Cohesion: 0.24
Nodes (8): _action_words(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The work in the user's own terms, from the pipeline's action vocabulary., One thing to remember, with the evidence that justifies it. Required by the…, _scope_words(), _start_words()

### Community 44 - "run_simulation"
Cohesion: 0.05
Nodes (56): InterruptHook, Queue, SimulatedMailbox, Case, CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all. (+48 more)

### Community 45 - "main"
Cohesion: 0.32
Nodes (8): CaptureFixture, main(), Run both lanes and print the report, so the scorer can be read before it is…, test_cli_refuses_to_open_the_sealed_lane(), test_cli_replays_the_fixture(), test_cli_requires_a_subcommand(), test_cli_seed_flag_changes_the_replay_digest(), test_cli_show_labels_flag_is_off_by_default()

### Community 46 - "LaneView"
Cohesion: 0.09
Nodes (15): RuntimeError, LaneView, Raised when code reaches across the learning/held-out firewall., Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach. (+7 more)

### Community 47 - "test_triage.py"
Cohesion: 0.13
Nodes (17): Direction, StrEnum, Which way a message travelled in its thread., message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+9 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.09
Nodes (30): parametrize, approval_for(), Crash, Crashing, Flaky, Message, Proposal, ProposalGateway (+22 more)

### Community 49 - "retrieve_style"
Cohesion: 0.14
Nodes (22): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., What the kept examples cost, in the same rough unit as the cap., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example() (+14 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "run_typed"
Cohesion: 0.13
Nodes (16): decision_sources(), DecisionSource, Path, TraceSink, Which decision source produced the routes in a labelled run., Sender, subject and body are inputs in production; labels are only answers.…, On a real run: one line per arrival, and no mail text in any of them., Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines… (+8 more)

### Community 52 - "test_graph.py"
Cohesion: 0.12
Nodes (26): GraphOutcome, LaneView, ProposalGateway, Router, SimulatedMailbox, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., What a lane through the graph did. (+18 more)

### Community 53 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.11
Nodes (14): Ledger, _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured. (+6 more)

### Community 55 - "registry.py"
Cohesion: 0.07
Nodes (41): ABC, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest() (+33 more)

### Community 56 - ".load"
Cohesion: 0.16
Nodes (18): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Manifest, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows., Counts per split and per lane, for the validator's output., view(), view() (+10 more)

### Community 57 - "run_canonical.py"
Cohesion: 0.14
Nodes (19): main(), preference_for(), The four reference cases, run end to end and printed as transcripts. Each case…, The scoped preference a confirmed rule would leave behind for this sender.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route. (+11 more)

### Community 58 - "EffectLog"
Cohesion: 0.22
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "drafting_for"
Cohesion: 0.13
Nodes (14): Drafting, drafting_for(), examples_from_row(), How many examples this case allows. The row's ``needs_draft`` is deliberately…, A draft, what it read, and whether it may be shown., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+6 more)

### Community 61 - ".proposal_for"
Cohesion: 0.16
Nodes (12): Message, Proposal, ProposalRequest, _domain(), proposal_from(), Claim, One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one. (+4 more)

### Community 62 - "Any"
Cohesion: 0.20
Nodes (17): Any, _entries(), freeze(), load(), Learner, Path, Router, Freezing what a run learned, so the next one starts where it stopped. Three… (+9 more)

### Community 63 - "agent/triage.py"
Cohesion: 0.08
Nodes (32): _label_derived(), label_for(), _mail_rules(), _persona_checked(), _persona_refused(), persona_rule(), Message, Which persona rule this mail trips, in words, or None when it trips none. The… (+24 more)

### Community 64 - "calibration_report"
Cohesion: 0.17
Nodes (10): ask_curve(), Block, calibration_report(), The interruption curve: how many cases each block of the lane needed the user…, Score the calibration lane: the dispositions, the typings and the ask curve., One block of a lane, in delivery order, and how much of it asked for the user., The denominator is the run's own count, so a partial record cannot be scored., Blocks are the stream's own order, and four cases at block 12 is one block of… (+2 more)

### Community 65 - "test_events.py"
Cohesion: 0.11
Nodes (25): _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, A replayed stream can refuse a shape it does not understand., The dataset's answers live on the Case, so a decision path cannot read them., A unique, ascending stream passes., The same case arriving twice would double-count in the report denominators., The same message arriving twice is a replay, not a new arrival. (+17 more)

### Community 66 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 67 - "validate_cases"
Cohesion: 0.05
Nodes (60): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+52 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.21
Nodes (13): Learner, Path, Router, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw() (+5 more)

### Community 69 - "IO"
Cohesion: 0.09
Nodes (39): ClaimStore, DecisionSource, GraphSession, IO, Namespace, Protocol, The pair's name, so a run says where a proposal could have come from., data_validate() (+31 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 73 - "Router"
Cohesion: 0.12
Nodes (36): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., approve(), ask_again(), bucket_for(), case() (+28 more)

### Community 74 - "trace.py"
Cohesion: 0.07
Nodes (44): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+36 more)

### Community 76 - "RememberedProvider"
Cohesion: 0.22
Nodes (6): ClaimStore, ProposalProvider, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider

### Community 77 - "view"
Cohesion: 0.13
Nodes (16): ExplodingPolicy, Lane, The lane is delivered window by window, not in the dataset's sequence order., A piped stream has no prompt to answer, so its lines are corrections. Reading…, A decision source that fails, to check the failure names its case., If the read fails, the prompts must see end of input, not wait forever., Fixture case ids in the order the windows deliver them., scheduled_case_ids() (+8 more)

### Community 79 - ".state"
Cohesion: 0.25
Nodes (3): Any, Every block the page has not seen yet., What the page's side panel shows: what the run did and what it now knows.

### Community 80 - "test_loop.py"
Cohesion: 0.08
Nodes (27): LaneView, LoopReport, ClaimStore, ProposalProvider, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Types scripted lines at the decisions that wait for a human. A line handed over…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet. (+19 more)

### Community 83 - "test_denominators.py"
Cohesion: 0.09
Nodes (48): held_out_report(), Score the sealed lane, refusing outright if anything about it could teach. Both…, Route, _decision(), _feedback(), _gold(), Lane, LaneView (+40 more)

### Community 88 - "router.py"
Cohesion: 0.11
Nodes (27): What the router considered, which every canonical run keeps., Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of… (+19 more)

### Community 98 - "Route"
Cohesion: 0.10
Nodes (36): The route the run actually chose., Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route, named_route() (+28 more)

### Community 105 - "EventStream"
Cohesion: 0.11
Nodes (15): EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., EventStream, _json_default(), Any, A stable hash of the replay log., An append-only log of arriving events. There is no update, no delete and no… (+7 more)

### Community 116 - "SafetyVerdict"
Cohesion: 0.25
Nodes (8): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), Assert SafetyVerdict instances are frozen to prevent tampering., test_verdict_immutability(), test_strictest_allowed_is_the_least_autonomous_route(), verdict()

### Community 117 - "Block"
Cohesion: 0.29
Nodes (6): Block, classify(), Append one block, with the number the page polls from., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 118 - "test_eval_run.py"
Cohesion: 0.14
Nodes (22): Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, load_script(), The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, ScriptedTeaching, Manifest (+14 more)

### Community 119 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 120 - "_background_loop"
Cohesion: 0.33
Nodes (4): AbstractEventLoop, _background_loop(), End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 121 - "valid"
Cohesion: 0.19
Nodes (14): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., quiet_but_wrong(), A provider that would happily label suspicious mail and move on., The rules belong to the mail, so a model never gets to propose a quiet route…, The net under the gate: a proposal from some other path still cannot land…, The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses() (+6 more)

### Community 122 - "interrupting_case_ids"
Cohesion: 0.17
Nodes (16): first_interrupt_of(), gold_route(), interrupting_case_ids(), Route, The plan's check, against the labels: only ask-first and escalate lines wait., The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts. (+8 more)

### Community 124 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 125 - "dataset.py"
Cohesion: 0.14
Nodes (28): argparse, asyncio, collections_abc, dataclasses, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The two-lane scorer: what the agent did, counted where it happened. The report…, The evaluation run: teach the learning lane, freeze it, score the sealed lane… (+20 more)

### Community 126 - "test_every_dataset_route_parses_without_an_adapter"
Cohesion: 0.20
Nodes (6): Assert FLOOR_RULES is an immutable tuple of rules., The floor routes ARE the dataset's autonomy vocabulary. Adding, renaming or…, Gold outcomes and autonomy ceilings are valid Route values as written., test_every_dataset_route_parses_without_an_adapter(), test_route_vocabulary_is_the_dataset_vocabulary(), test_rule_table_immutability()

### Community 127 - "record_from_chat"
Cohesion: 0.17
Nodes (11): LaneRecord, Lane, What one lane run recorded, in the shape the report reads. Built from a chat…, Refuse a record whose counts cannot add up to what the run processed., Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., record_from_chat(), record_from_graph() (+3 more)

### Community 128 - "build_parser"
Cohesion: 0.33
Nodes (7): ArgumentParser, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), Calibrating on the same mail twice asks once: the rule answers the second time., test_the_simulator_answers_from_a_saved_rule_without_asking()

### Community 130 - "dispositions"
Cohesion: 0.17
Nodes (9): Disposition, dispositions(), How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to., Count routes into the three dispositions, refusing a route nobody defined., The plan's rule: three dispositions, one per case, adding up to all of them., A fifth route is a bug, and an uncounted case is the same bug wearing a number., test_a_route_the_report_does_not_know_is_refused_rather_than_counted() (+1 more)

### Community 131 - "_case_from_mail_row"
Cohesion: 0.14
Nodes (16): Direction, SenderIdentity, _attachment(), _case_from_mail_row(), event_from_row(), _message(), EmailEvent, Canonicalize one dataset row into an EmailEvent. (+8 more)

### Community 132 - "claims.py"
Cohesion: 0.12
Nodes (23): enum, _claim_from_record(), claim_id_for(), _claim_record(), ClaimType, Any, datetime, StrEnum (+15 more)

### Community 134 - "serve"
Cohesion: 0.50
Nodes (4): main(), Start the server, ready to be run by the caller., serve(), ThreadingHTTPServer

### Community 135 - "test_a_strangers_instructions_fence_every_route_whatever_the_action"
Cohesion: 0.22
Nodes (9): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., The mail fences, not the proposed action: a harmless label still collapses to…, test_a_strangers_instructions_fence_every_route_whatever_the_action(), test_benign_workplace_clean_pass(), test_classify_action_matrix() (+1 more)

### Community 147 - "_order_key"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

## Knowledge Gaps
- **14 isolated node(s):** `The safety floor decides who is on the ballot`, `Silence is not approval`, `Worked example: the AWS invoice`, `Worked example: the ambiguous refund`, `What an ask carries` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **56 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `policy.py`, `claims.py`, `test_a_strangers_instructions_fence_every_route_whatever_the_action`, `test_feedback_parser.py`, `test_floor.py`, `ClaimScope`, `floor.py`, `ProposalGateway`, `injection.py`, `RuleProvider`, `test_sim_tools.py`, `Learner`, `Claim`, `.load`, `run_canonical.py`, `agent/triage.py`, `test_events.py`, `Router`, `trace.py`, `router.py`, `SafetyVerdict`, `valid`, `classify_action`, `dataset.py`, `test_every_dataset_route_parses_without_an_adapter`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `PresidioMasker` connect `PresidioMasker` to `get_token_map`, `ContextPhoneRecognizer`, `masker.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `LaneView` connect `LaneView` to `Route`, `_case_from_mail_row`, `Router`, `test_graph.py`, `.load`, `dataset.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 110 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 110 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ActionPayload` (e.g. with `test_an_external_send_is_never_silent_or_notified()` and `test_a_credential_named_by_a_stranger_fences_a_harmless_action()`) actually correct?**
  _`ActionPayload` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Bucket` (e.g. with `Learner` and `Router`) actually correct?**
  _`Bucket` has 17 INFERRED edges - model-reasoned connections that need verification._