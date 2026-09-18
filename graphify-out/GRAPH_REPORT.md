# Graph Report - ai-email-agent  (2026-09-18)

## Corpus Check
- 83 files · ~67,024 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2050 nodes · 5015 edges · 113 communities (94 shown, 19 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 766 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a9b505e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- route_decision
- graph.py
- registry.py
- ClaimStore
- FeedbackKind
- feedback.py
- dataset.py
- Bucket
- ScopeAnchor
- test_floor.py
- test_claim_schema.py
- ChatRunner
- floor.py
- Handler
- Session
- graph_run
- test_gateway.py
- injection.py
- ManifestError
- gateway.py
- EventValidationError
- test_sim.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- Learner
- test_triage.py
- state.py
- app.js
- ._arrival_block
- drafts.py
- preferences.py
- test_predrafts.py
- test_graph_state.py
- test_floor_protection.py
- test_replay.py
- build_provider
- mask_for_llm
- PresidioMasker
- Manifest
- arrivals
- test_loop.py
- claims.py
- schedule
- main
- SplitViolation
- .run
- test_graph_resume.py
- retrieve_style
- Routes
- run_typed
- test_graph.py
- ContextPhoneRecognizer
- OpenAICompatibleProvider
- Block
- RoutingRequest
- run_scenario
- Cutoffs
- SentExample
- run_simulation
- ScriptedProvider
- interrupting_case_ids
- classify_action
- plan_deviation
- test_events.py
- test_benign_workplace_clean_pass
- runner.py
- Message
- ScriptedReplies
- Style
- masker.py
- get_token_map
- _server
- _background_loop
- _bucket_of
- ._run
- ExplodingPolicy
- test_a_traced_run_writes_the_decision_and_never_the_mail
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- _order_key
- Any
- Workflow: graphify
- email-autonomy-agent
- router.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- StrEnum
- parametrize
- .predraft
- .lines
- .interrupts
- ._waited
- InterruptHook
- Queue
- datetime
- ValueError
- parametrize

## God Nodes (most connected - your core abstractions)
1. `Route` - 128 edges
2. `Learner` - 43 edges
3. `Router` - 42 edges
4. `Message` - 41 edges
5. `Bucket` - 40 edges
6. `Manifest` - 38 edges
7. `Claim` - 37 edges
8. `ActionPayload` - 36 edges
9. `ClaimStore` - 36 edges
10. `run_simulation()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_a_crash_inside_a_commit_recovers_to_exactly_one_effect()` --uses--> `GraphError`  [INFERRED]
  tests/test_graph_resume.py → src/agent/graph.py
- `test_resuming_a_decision_that_does_not_exist_fails_with_its_name()` --uses--> `GraphError`  [INFERRED]
  tests/test_graph_resume.py → src/agent/graph.py
- `test_a_case_the_lane_does_not_hold_fails_with_its_name()` --uses--> `GraphError`  [INFERRED]
  tests/test_graph.py → src/agent/graph.py
- `cold_control()` --uses--> `Decision`  [INFERRED]
  evals/run_canonical.py → src/agent/sim/policy.py

## Import Cycles
- None detected.

## Communities (113 total, 19 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.06
Nodes (30): EventStream, _json_default(), Any, datetime, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time. (+22 more)

### Community 1 - "route_decision"
Cohesion: 0.09
Nodes (29): EmailContext, RoutingRequest, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, email_context_for(), named_route(), _params_with_case(), Any (+21 more)

### Community 2 - "graph.py"
Cohesion: 0.06
Nodes (59): Command, CompiledStateGraph, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled() (+51 more)

### Community 3 - "registry.py"
Cohesion: 0.07
Nodes (42): hashlib, json, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused (+34 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (42): ClaimStore, datetime, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once. (+34 more)

### Community 5 - "FeedbackKind"
Cohesion: 0.23
Nodes (17): FeedbackKind, StrEnum, What the user did after seeing a decision. Values are the dataset's…, feedback(), Never tell me about these" is a never in the user's words and a yes in effect., One recorded line, as the simulator writes it., A confirmed rule, the way the parser hands one over., A decision nobody answered is not an approval, and not evidence of any kind. (+9 more)

### Community 6 - "feedback.py"
Cohesion: 0.08
Nodes (39): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+31 more)

### Community 7 - "dataset.py"
Cohesion: 0.10
Nodes (35): _attachment(), Case, _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime (+27 more)

### Community 8 - "Bucket"
Cohesion: 0.11
Nodes (24): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.11
Nodes (35): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum (+27 more)

### Community 10 - "test_floor.py"
Cohesion: 0.06
Nodes (51): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate. (+43 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.14
Nodes (24): pytest, ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., memory(), preference(), parametrize, Protected attributes are out of memory by construction, not by a filter: the… (+16 more)

### Community 12 - "ChatRunner"
Cohesion: 0.16
Nodes (14): FeedbackContext, FeedbackKind, Reading, Decision, What the simulator does with one arrival., ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Ask the one bounded question and store the rule only if it is confirmed. (+6 more)

### Community 13 - "floor.py"
Cohesion: 0.12
Nodes (31): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+23 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (10): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one. (+2 more)

### Community 15 - "Session"
Cohesion: 0.12
Nodes (22): Point the server at a session, which is what the tests and the page both need., set_session(), importlib_util, Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive… (+14 more)

### Community 16 - "graph_run"
Cohesion: 0.09
Nodes (36): ArgumentParser, Namespace, The pair's name, so a run says where a proposal could have come from., build_parser(), graph_run(), _keep_rules(), loop_run(), _open_store() (+28 more)

### Community 17 - "test_gateway.py"
Cohesion: 0.09
Nodes (38): parse_proposal(), ProposalGateway, The offline provider: proposes from triage, no network, deterministic. It is a…, Turns provider text into a validated proposal, with one repair attempt., Validate one provider answer. Anything unexpected is an error, not a default., RuleProvider, message(), parametrize (+30 more)

### Community 18 - "injection.py"
Cohesion: 0.07
Nodes (31): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+23 more)

### Community 19 - "ManifestError"
Cohesion: 0.15
Nodes (15): CaseLabels, ManifestError, ValueError, The dataset's answer for this case, for scoring and debugging only., Build a manifest from parsed rows, rejecting duplicate case ids and splits., Raised when the dataset itself violates the manifest schema., The dataset's ground truth for a case. These are answers: what the case was…, A bare KeyError says nothing about which of the cases is malformed. (+7 more)

### Community 20 - "gateway.py"
Cohesion: 0.17
Nodes (15): os, _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), Model proposal gateway (plan Commit 5.3). A thin provider interface with a…, The route this mail compels on the persona's own account, or None when free.… (+7 more)

### Community 21 - "EventValidationError"
Cohesion: 0.17
Nodes (10): DuplicateEventError, EventValidationError, ValueError, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text(), History ids are unique, even though the dataset reuses them across cases., The enum is the vocabulary; a loose string is refused rather than coerced. (+2 more)

### Community 22 - "test_sim.py"
Cohesion: 0.21
Nodes (18): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+10 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.18
Nodes (23): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+15 more)

### Community 24 - "email_tools.py"
Cohesion: 0.06
Nodes (36): ABC, action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification (+28 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.16
Nodes (28): DraftCode, Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the…, validate_draft(), StrEnum, case() (+20 more)

### Community 26 - "Learner"
Cohesion: 0.10
Nodes (18): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+10 more)

### Community 27 - "test_triage.py"
Cohesion: 0.14
Nodes (17): guesses(), manifest(), message(), fixture, Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+9 more)

### Community 28 - "state.py"
Cohesion: 0.10
Nodes (28): Claim, Drafting, FeedbackEvent, Routing, Record the route the router chose, which is what authorization checks., route(), Feedback a learner would accept, which is nothing until Commit 3.6., One line per decision, and one per reply: ids, hashes, bounded records. (+20 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "._arrival_block"
Cohesion: 0.18
Nodes (13): ReplyTree, SenderIdentity, _address(), _body_lines(), _prior_lines(), The arriving mail the way an inbox shows it. Sender, recipients, subject, body…, One compact field for the labelled view: reconstructed messages and depth., The address a reader sees, with its unverified display name left visible. (+5 more)

### Community 31 - "drafts.py"
Cohesion: 0.08
Nodes (28): Case, draft_reply(), Drafting, drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+20 more)

### Community 32 - "preferences.py"
Cohesion: 0.09
Nodes (23): Protocol, _domain(), proposal_from(), The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., Answer from a claim where one bears on this mail, otherwise ask the inner one., What the user's own words amount to for this mail, if anything. (+15 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.15
Nodes (20): drafting(), held(), Case, Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+12 more)

### Community 34 - "test_graph_state.py"
Cohesion: 0.07
Nodes (44): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+36 more)

### Community 35 - "test_floor_protection.py"
Cohesion: 0.12
Nodes (34): floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., approve(), ask_again(), bucket_for(), case(), feedback(), one_case_view() (+26 more)

### Community 36 - "test_replay.py"
Cohesion: 0.07
Nodes (34): Replay events through a fresh seeded stream., replay(), manifest(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival. (+26 more)

### Community 37 - "build_provider"
Cohesion: 0.13
Nodes (18): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Ask the provider, repair once if the answer does not parse, then fail closed., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client() (+10 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Manifest"
Cohesion: 0.07
Nodes (38): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Lane, LaneView, Manifest, Path, StrEnum, Every case in the dataset, sorted by sequence index, with its digest.… (+30 more)

### Community 41 - "arrivals"
Cohesion: 0.17
Nodes (16): arrivals(), block_of(), labelled_routes(), The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., One arrival's text, from its header up to the next arrival., The one error direction that matters: never act on mail the labels fence., Only one of the two has something to release, so only one says approval. (+8 more)

### Community 42 - "test_loop.py"
Cohesion: 0.14
Nodes (15): io, LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen., asked(), loop() (+7 more)

### Community 43 - "claims.py"
Cohesion: 0.13
Nodes (18): enum, _action_words(), _bears_on(), Claim, _claim_from_record(), _claim_record(), Any, Path (+10 more)

### Community 44 - "schedule"
Cohesion: 0.11
Nodes (28): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them. (+20 more)

### Community 45 - "main"
Cohesion: 0.19
Nodes (14): main(), Entry point for the ``wajo`` console script., test_the_cli_keeps_the_held_out_lane_shut(), CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., test_a_broken_input_stream_ends_the_run_instead_of_hanging() (+6 more)

### Community 46 - "SplitViolation"
Cohesion: 0.12
Nodes (12): RuntimeError, Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., Raised when code reaches across the learning/held-out firewall., SplitViolation, The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read., The separation is symmetric: a lane view only sees its own rows. (+4 more)

### Community 47 - ".run"
Cohesion: 0.20
Nodes (8): Case, RuntimeError, Reconstruct one case's thread, bounded by the reply-tree caps., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.…, Raised when a run cannot continue, naming the case it stopped on., SimError, thread_tree_for()

### Community 48 - "test_graph_resume.py"
Cohesion: 0.09
Nodes (30): parametrize, approval_for(), Crash, Crashing, Flaky, Message, Proposal, ProposalGateway (+22 more)

### Community 49 - "retrieve_style"
Cohesion: 0.18
Nodes (19): estimate_tokens(), A rough token count for a budget decision, not for a bill., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from., One sent reply, from the mailbox's own history., A reply the user sent this person beats an older one to anybody else. (+11 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "run_typed"
Cohesion: 0.14
Nodes (18): first_interrupt_of(), DecisionSource, The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., Sender, subject and body are inputs in production; labels are only answers.…, Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines… (+10 more)

### Community 52 - "test_graph.py"
Cohesion: 0.12
Nodes (25): GraphOutcome, LaneView, ProposalGateway, Router, SimulatedMailbox, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., What a lane through the graph did. (+17 more)

### Community 53 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "Block"
Cohesion: 0.22
Nodes (7): Block, classify(), Any, Append one block, with the number the page polls from., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 56 - "RoutingRequest"
Cohesion: 0.14
Nodes (10): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., RoutingRequest (+2 more)

### Community 57 - "run_scenario"
Cohesion: 0.09
Nodes (22): cold_control(), main(), What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it… (+14 more)

### Community 58 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 59 - "SentExample"
Cohesion: 0.15
Nodes (14): Any, examples_from_row(), How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over., The consented sent examples a case carries, if the mailbox offered any. Not the…, SentExample (+6 more)

### Community 60 - "run_simulation"
Cohesion: 0.12
Nodes (23): InterruptHook, Learner, Queue, InterruptHook, Queue, A hook that hands the waiting decision its lines, and closes input at the end., close_input(), Any (+15 more)

### Community 62 - "interrupting_case_ids"
Cohesion: 0.25
Nodes (8): dataset_routes(), interrupting_case_ids(), The dataset's route for each arrival, which only the label view prints., The plan's check, against the labels: only ask-first and escalate lines wait., Fixture cases whose gold route asks the user, in delivery order., test_a_correction_typed_at_a_prompt_binds_to_that_decision(), test_show_labels_reveals_the_decision_and_the_answer(), test_the_reference_policy_reproduces_the_dataset_routes()

### Community 63 - "classify_action"
Cohesion: 0.22
Nodes (11): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+3 more)

### Community 64 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 65 - "test_events.py"
Cohesion: 0.09
Nodes (37): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _feedback(), _load_dataset(), parametrize (+29 more)

### Community 66 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 67 - "runner.py"
Cohesion: 0.09
Nodes (37): argparse, asyncio, collections_abc, dataclasses, datetime, dotenv, The four reference cases, run end to end and printed as transcripts. Each case…, main() (+29 more)

### Community 68 - "Message"
Cohesion: 0.10
Nodes (21): Message, One email message, in a thread, in one direction., The rule proposal, before it is serialised like any other provider's., The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., amount_in() (+13 more)

### Community 69 - "ScriptedReplies"
Cohesion: 0.25
Nodes (7): Types scripted lines at the decisions that wait for a human. A line handed over…, ScriptedReplies, _drained(), Queue, Nothing hangs on a prompt the script never feeds: it is told a line that does…, test_a_decision_the_script_does_not_answer_is_passed_on(), test_a_named_entry_is_typed_at_the_case_it_names()

### Community 70 - "Style"
Cohesion: 0.22
Nodes (7): What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., The word the user opens with, borrowed from the best example and cited as such., _salutation(), Style, test_a_draft_falls_back_to_the_mail_when_there_is_no_example()

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 73 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 74 - "_background_loop"
Cohesion: 0.33
Nodes (4): AbstractEventLoop, _background_loop(), End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 75 - "_bucket_of"
Cohesion: 0.67
Nodes (3): Bucket, _bucket_of(), The bucket a decision belongs to: the mail's shape, and the work that was…

### Community 76 - "._run"
Cohesion: 0.20
Nodes (5): AnswerQueue, LaneView, The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Transcript

### Community 78 - "test_a_traced_run_writes_the_decision_and_never_the_mail"
Cohesion: 0.67
Nodes (3): Path, On a real run: one line per arrival, and no mail text in any of them., test_a_traced_run_writes_the_decision_and_never_the_mail()

### Community 79 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 80 - "_order_key"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

### Community 88 - "router.py"
Cohesion: 0.17
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "Route"
Cohesion: 0.16
Nodes (30): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, The four autonomy outcomes a candidate action can be routed to.…, Route, case(), feedback(), _hints(), Path (+22 more)

## Knowledge Gaps
- **14 isolated node(s):** `ROUTES`, `CHOICES`, `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `Silence is not approval` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `FeedbackKind`, `feedback.py`, `dataset.py`, `Bucket`, `ScopeAnchor`, `test_floor.py`, `test_claim_schema.py`, `floor.py`, `test_gateway.py`, `injection.py`, `gateway.py`, `test_sim_tools.py`, `Learner`, `preferences.py`, `test_graph_state.py`, `test_floor_protection.py`, `Manifest`, `arrivals`, `claims.py`, `run_typed`, `RoutingRequest`, `run_scenario`, `interrupting_case_ids`, `test_benign_workplace_clean_pass`, `Message`, `router.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `runner.py`, `Manifest`, `_background_loop`, `._waited`, `ChatRunner`, `._run`, `Handler`, `Block`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `mask_for_llm()` connect `mask_for_llm` to `get_token_map`, `graph.py`, `test_graph.py`, `masker.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 106 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 106 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Message` (e.g. with `RememberedProvider` and `_mail_rules()`) actually correct?**
  _`Message` has 24 INFERRED edges - model-reasoned connections that need verification._