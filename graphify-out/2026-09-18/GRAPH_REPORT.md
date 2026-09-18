# Graph Report - ai-email-agent  (2026-09-18)

## Corpus Check
- 77 files · ~55,783 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1720 nodes · 4365 edges · 95 communities (87 shown, 8 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 679 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `80b40716`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- test_gateway.py
- graph.py
- runner.py
- ClaimStore
- FeedbackKind
- feedback.py
- dataset.py
- Bucket
- ScopeAnchor
- ActionPayload
- ClaimScope
- ChatRunner
- floor.py
- Handler
- cli.py
- graph_run
- schedule.py
- test_floor.py
- GraphSession
- Case
- test_events.py
- gateway.py
- Route
- Effect
- test_ui_session.py
- Learner
- Message
- state.py
- app.js
- events.py
- Manifest
- ProposalRequest
- ProposalGateway
- TraceSink
- ReplyTree
- test_replay.py
- FakeCompletions
- mask_for_llm
- PresidioMasker
- email_tools.py
- test_sim.py
- test_loop.py
- claims.py
- test_triage.py
- ContextPhoneRecognizer
- test_graph.py
- run_simulation
- test_graph_resume.py
- masker.py
- Routes
- injection.py
- build_reply_tree
- SimulatedMailbox
- OpenAICompatibleProvider
- json
- Posterior
- classify_action
- test_dataset_feedback_vocabulary_and_flags_are_representable
- .describe
- .levels
- SenderIdentity
- Session
- Tool
- EmailEvent
- EffectLog
- main
- _background_loop
- get_token_map
- Block
- Transcript
- NotifyUser
- test_benign_workplace_clean_pass
- .labels
- SimError
- Workflow: graphify
- email-autonomy-agent
- rules/graphify.md
- DESIGN.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `Route` - 111 edges
2. `ChatRunner` - 50 edges
3. `Message` - 47 edges
4. `ClaimStore` - 47 edges
5. `Manifest` - 41 edges
6. `Claim` - 39 edges
7. `Case` - 37 edges
8. `Lane` - 36 edges
9. `ActionPayload` - 36 edges
10. `Learner` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `set_session()` --uses--> `Session`  [INFERRED]
  frontend-ui/server.py → src/agent/ui/session.py
- `Handler` --uses--> `Session`  [INFERRED]
  frontend-ui/server.py → src/agent/ui/session.py
- `test_a_calibration_run_counts_what_the_user_said()` --uses--> `Learner`  [INFERRED]
  tests/learning/test_updates.py → src/agent/autonomy/bandit.py
- `test_a_confirmed_rule_counts_the_route_it_chose_not_the_words_that_chose_it()` --uses--> `Learner`  [INFERRED]
  tests/learning/test_updates.py → src/agent/autonomy/bandit.py

## Import Cycles
- None detected.

## Communities (95 total, 8 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.09
Nodes (22): EventStream, _json_default(), Any, datetime, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., The current simulated time. (+14 more)

### Community 1 - "test_gateway.py"
Cohesion: 0.07
Nodes (49): build_provider(), parse_proposal(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Validate one provider answer. Anything unexpected is an error, not a default., Resolve a provider by name, refusing one that cannot run here. The model comes…, BrokenProvider (+41 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (43): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), _bound(), build_graph() (+35 more)

### Community 3 - "runner.py"
Cohesion: 0.06
Nodes (44): Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).…, build_registry(), Every simulated tool, over one mailbox., Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused (+36 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (42): _open_store(), The run's memory: the rules already kept, and the file they live in., ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Capability, ConsentRequired (+34 more)

### Community 5 - "FeedbackKind"
Cohesion: 0.20
Nodes (19): FeedbackKind, What the user did after seeing a decision. Values are the dataset's…, feedback(), Never tell me about these" is a never in the user's words and a yes in effect., The wiring, not just the rule: a line confirmed at a prompt moves a posterior., One recorded line, as the simulator writes it., A confirmed rule, the way the parser hands one over., A decision nobody answered is not an approval, and not evidence of any kind. (+11 more)

### Community 6 - "feedback.py"
Cohesion: 0.09
Nodes (34): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+26 more)

### Community 7 - "dataset.py"
Cohesion: 0.21
Nodes (17): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime, Dataset manifest and the split firewall (Phase 3.2). The dataset is loaded… (+9 more)

### Community 8 - "Bucket"
Cohesion: 0.13
Nodes (22): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+14 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.11
Nodes (33): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means. (+25 more)

### Community 10 - "ActionPayload"
Cohesion: 0.07
Nodes (39): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions. (+31 more)

### Community 11 - "ClaimScope"
Cohesion: 0.12
Nodes (25): claim_id_for(), ClaimScope, A stable id for the same claim said twice, so it is never stored twice., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., memory(), preference() (+17 more)

### Community 12 - "ChatRunner"
Cohesion: 0.13
Nodes (16): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.… (+8 more)

### Community 13 - "floor.py"
Cohesion: 0.12
Nodes (31): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+23 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (10): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one. (+2 more)

### Community 15 - "cli.py"
Cohesion: 0.08
Nodes (27): asyncio, collections_abc, Protocol, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, _policy() (+19 more)

### Community 16 - "graph_run"
Cohesion: 0.19
Nodes (17): Namespace, The pair's name, so a run says where a proposal could have come from., graph_run(), _keep_rules(), loop_run(), IO, Say what the reader is looking at, since labels change the calibration., Say what a run starts with, so it is obvious whether earlier rules are in force. (+9 more)

### Community 17 - "schedule.py"
Cohesion: 0.11
Nodes (28): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, _dependencies_first(), RuntimeError, Windowed-random arrival scheduling (plan Commit 3.5). A lane replayed in…, Raised when a case names a dependency no window can deliver before it., One released window: its cases in delivery order, and the seed that ordered it., The window's case ids in the order they will arrive., Cut a lane into ordered windows, shuffling only inside each one. (+20 more)

### Community 18 - "test_floor.py"
Cohesion: 0.09
Nodes (26): Scan untrusted email content and headers for prompt injection indicators., scan(), Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles. (+18 more)

### Community 19 - "GraphSession"
Cohesion: 0.12
Nodes (17): Command, GraphError, GraphOutcome, GraphSession, Any, RuntimeError, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the… (+9 more)

### Community 20 - "Case"
Cohesion: 0.13
Nodes (17): Case, Whether this case carries the dataset's answer at all., Open one case from this lane. Refuses any other lane's case., One dataset row: its lane, its canonical event, its labels and the raw record., email_context_for(), floor_verdict_for(), _params_with_case(), Any (+9 more)

### Community 21 - "test_events.py"
Cohesion: 0.10
Nodes (28): _event(), _feedback(), parametrize, Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, Empty ids and malformed fields fail at construction, not at use., A replayed stream can refuse a shape it does not understand., The dataset's answers live on the Case, so a decision path cannot read them., A unique, ascending stream passes. (+20 more)

### Community 22 - "gateway.py"
Cohesion: 0.13
Nodes (25): os, re, proposal_from(), One claim as a proposal, or None when the claim names no route., _label_derived(), label_for(), _mail_rules(), _persona_checked() (+17 more)

### Community 23 - "Route"
Cohesion: 0.08
Nodes (52): dataclasses, Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of… (+44 more)

### Community 24 - "Effect"
Cohesion: 0.16
Nodes (13): CreateDraft, _email_id(), LabelEmail, Any, Writes a private draft. Reversible, and never a send., A send that validates like a real one and never leaves the mailbox. Recipients…, Applies one label to one message., SendEmail (+5 more)

### Community 25 - "test_ui_session.py"
Cohesion: 0.14
Nodes (16): importlib_util, pytest, _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., The run writes the summary a line at a time; the page has to read it as one… (+8 more)

### Community 26 - "Learner"
Cohesion: 0.13
Nodes (12): Learner, Counts what the user said into posteriors, once per event, never from silence.…, Count one explicit decision about one bucket, at most once. False if uncounted., The confirmed rule that refused this arm, or '' when the user has not refused…, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this… (+4 more)

### Community 27 - "Message"
Cohesion: 0.11
Nodes (23): Message, One email message, in a thread, in one direction., The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), RuleProvider, amount_in() (+15 more)

### Community 28 - "state.py"
Cohesion: 0.14
Nodes (21): hashlib, One line per decision, and one per reply: ids, hashes, bounded records., hint_fields(), message_digest(), _plain(), prepared_fields(), Any, What was committed. Effect targets are scrubbed by the sink. (+13 more)

### Community 29 - "app.js"
Cohesion: 0.23
Nodes (21): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), poll() (+13 more)

### Community 30 - "events.py"
Cohesion: 0.16
Nodes (15): Attachment, DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, An attachment as metadata, plus its text when the text is extractable.…, Reject a stream that repeats a case or message, or drifts out of order. Order… (+7 more)

### Community 31 - "Manifest"
Cohesion: 0.10
Nodes (27): Manifest, ManifestError, Path, ValueError, Every case in the dataset, sorted by sequence index, with its digest.…, Build a manifest from parsed rows, rejecting duplicate case ids and splits., Load the manifest from a JSONL dataset file, or from plain mail rows., Return the lane-bound handle for one lane. (+19 more)

### Community 32 - "ProposalRequest"
Cohesion: 0.14
Nodes (9): _domain(), Answer from a claim where one bears on this mail, otherwise ask the inner one., What the user's own words amount to for this mail, if anything., ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask the provider, repair once if the answer does not parse, then fail closed. (+1 more)

### Community 33 - "ProposalGateway"
Cohesion: 0.19
Nodes (8): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, route out., AnswerQueue, Load the lane and begin the run. A failure here is the caller's to report., Append one block, with the number the page polls from., The line queue the run reads from, which is also what "waiting" means. The run…

### Community 34 - "TraceSink"
Cohesion: 0.08
Nodes (38): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+30 more)

### Community 35 - "ReplyTree"
Cohesion: 0.14
Nodes (15): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _address(), _body_lines(), _prior_lines(), The arriving mail the way an inbox shows it. Sender, recipients, subject, body… (+7 more)

### Community 36 - "test_replay.py"
Cohesion: 0.05
Nodes (53): Lane, RuntimeError, StrEnum, Where a case sits relative to learning., Raised when code reaches across the learning/held-out firewall., SplitViolation, Replay events through a fresh seeded stream., replay() (+45 more)

### Community 37 - "FakeCompletions"
Cohesion: 0.40
Nodes (4): fake_client(), FakeCompletions, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request.

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "email_tools.py"
Cohesion: 0.22
Nodes (7): action_vocabulary(), Draft, The simulated email tools (Phase 3.3). Six tools over one in-memory mailbox:…, What a proposer may ask for, and what each action needs, as prompt lines., A private draft. Preparation, not sending., Read-only: returns the message it was pointed at., ReadEmail

### Community 41 - "test_sim.py"
Cohesion: 0.07
Nodes (59): arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, first_interrupt_of(), interrupting_case_ids(), labelled_routes() (+51 more)

### Community 42 - "test_loop.py"
Cohesion: 0.09
Nodes (28): ArgumentParser, io, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), InterruptHook, Queue (+20 more)

### Community 43 - "claims.py"
Cohesion: 0.08
Nodes (26): enum, pathlib, _action_words(), _bears_on(), Claim, _claim_from_record(), _claim_record(), ClaimError (+18 more)

### Community 44 - "test_triage.py"
Cohesion: 0.14
Nodes (17): guesses(), manifest(), message(), fixture, Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+9 more)

### Community 45 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 46 - "test_graph.py"
Cohesion: 0.14
Nodes (19): langgraph_checkpoint_memory, LaneView, A lane-bound handle over the manifest. A view can only open cases in its own…, Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path (+11 more)

### Community 47 - "run_simulation"
Cohesion: 0.15
Nodes (16): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did., Feedback a learner would accept, which is nothing until Commit 3.6. (+8 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.23
Nodes (15): approval_for(), The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, The yes a reviewer would send back for the work they were shown., session(), test_a_crash_before_the_work_ran_leaves_the_decision_waiting(), test_a_decision_that_moved_between_asking_and_answering_is_refused() (+7 more)

### Community 49 - "masker.py"
Cohesion: 0.14
Nodes (13): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+5 more)

### Community 50 - "Routes"
Cohesion: 0.25
Nodes (7): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "injection.py"
Cohesion: 0.09
Nodes (24): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+16 more)

### Community 52 - "build_reply_tree"
Cohesion: 0.14
Nodes (21): datetime, build_reply_tree(), _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…, Reconstruct the reply tree for a thread, bounded by depth and node caps.… (+13 more)

### Community 53 - "SimulatedMailbox"
Cohesion: 0.15
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "json"
Cohesion: 0.17
Nodes (12): argparse, dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., Point the server at a session, which is what the tests and the page both need., serve(), set_session() (+4 more)

### Community 56 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 57 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 58 - "test_dataset_feedback_vocabulary_and_flags_are_representable"
Cohesion: 0.29
Nodes (7): _load_dataset(), Every kind in the dataset parses, and its learner flag matches the rule. This…, Real rows (history, attachments, sender identity) fit the models as written., The dataset is in file order already, and its indices are unique and ascending., test_dataset_feedback_vocabulary_and_flags_are_representable(), test_dataset_rows_convert_to_canonical_events(), test_dataset_stream_survives_the_ordering_contract()

### Community 61 - "SenderIdentity"
Cohesion: 0.22
Nodes (10): A conversation: the messages that arrived before this case, oldest first., Who an email claims to come from, and whether that claim is verified.…, SenderIdentity, Thread, History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread() (+2 more)

### Community 62 - "Session"
Cohesion: 0.19
Nodes (11): Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, Poll a session the way the page does, so a slow line fails as one readable…, The four states are the colours on the page, so each card needs the route it…, test_a_session_shows_the_mail_and_takes_a_line() (+3 more)

### Community 63 - "Tool"
Cohesion: 0.20
Nodes (7): ABC, ArchiveEmail, Files a message out of the inbox., One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit., Tool

### Community 64 - "EmailEvent"
Cohesion: 0.17
Nodes (8): The lane's arriving events, in sequence order., EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The manifest hands out EmailEvents, not raw rows., test_events_are_canonical_events()

### Community 66 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 68 - "main"
Cohesion: 0.15
Nodes (17): main(), Entry point for the ``wajo`` console script., CaptureFixture, MonkeyPatch, test_the_cli_keeps_the_held_out_lane_shut(), test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in(), CaptureFixture, MonkeyPatch (+9 more)

### Community 71 - "_background_loop"
Cohesion: 0.33
Nodes (4): AbstractEventLoop, _background_loop(), End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 74 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 75 - "Block"
Cohesion: 0.25
Nodes (6): Block, classify(), Any, One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 77 - "NotifyUser"
Cohesion: 0.29
Nodes (4): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else.

### Community 78 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 80 - ".labels"
Cohesion: 0.50
Nodes (3): CaseLabels, The dataset's answer for this case, for scoring and debugging only., The dataset's ground truth for a case. These are answers: what the case was…

### Community 81 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

## Knowledge Gaps
- **13 isolated node(s):** `ROUTES`, `CHOICES`, `email-autonomy-agent`, `graphify`, `Steps` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `test_gateway.py`, `runner.py`, `FeedbackKind`, `feedback.py`, `ScopeAnchor`, `ActionPayload`, `ClaimScope`, `ChatRunner`, `floor.py`, `cli.py`, `test_floor.py`, `Case`, `gateway.py`, `Learner`, `Message`, `state.py`, `events.py`, `Manifest`, `test_sim.py`, `claims.py`, `injection.py`, `classify_action`, `test_dataset_feedback_vocabulary_and_flags_are_representable`, `Session`, `test_benign_workplace_clean_pass`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `ChatRunner` connect `ChatRunner` to `SeededClock`, `graph.py`, `runner.py`, `ClaimStore`, `FeedbackKind`, `feedback.py`, `schedule.py`, `Case`, `gateway.py`, `Route`, `Learner`, `state.py`, `ProposalGateway`, `TraceSink`, `ReplyTree`, `claims.py`, `test_graph.py`, `run_simulation`, `SimulatedMailbox`, `Session`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `Lane` connect `test_replay.py` to `EmailEvent`, `ProposalGateway`, `ClaimStore`, `FeedbackKind`, `dataset.py`, `test_sim.py`, `test_loop.py`, `test_graph.py`, `cli.py`, `graph_run`, `test_graph_resume.py`, `gateway.py`, `Session`, `Manifest`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 86 inferred relationships involving `Route` (e.g. with `Loss` and `route_loss()`) actually correct?**
  _`Route` has 86 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `ChatRunner` (e.g. with `Learner` and `Case`) actually correct?**
  _`ChatRunner` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `Message` (e.g. with `RememberedProvider` and `_mail_rules()`) actually correct?**
  _`Message` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ClaimStore` (e.g. with `RememberedProvider` and `_keep_rules()`) actually correct?**
  _`ClaimStore` has 13 INFERRED edges - model-reasoned connections that need verification._