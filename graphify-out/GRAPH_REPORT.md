# Graph Report - ai-email-agent  (2026-09-18)

## Corpus Check
- 77 files · ~53,443 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 7, .example 1, .css 1)

## Summary
- 1687 nodes · 4294 edges · 99 communities (83 shown, 16 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 707 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- hashlib & json
- parse_proposal() & ProposalGateway
- CompiledStateGraph & langgraph_graph
- tools/__init__.py & Simulated tools a...
- learning/__init__.py & claims.py
- Lane & LaneView
- re & feedback.py
- dataset.py & _attachment()
- Random & .__init__()
- confirm_claim() & confirm_words()
- ActionPayload & floor_check()
- .__post_init__() & ClaimError
- Decision & .interrupts()
- floor.py & ActionClass
- AbstractEventLoop & BaseHTTPRequestHa...
- asyncio & os
- Namespace & The pair's name, so a run...
- _dependencies_first() & dependencies_...
- test_floor.py & Unit tests for the de...
- Command & GraphOutcome
- Case & .labelled()
- OutOfOrderEventError & Reject a strea...
- _label_derived() & label_for()
- build_registry() & Every simulated to...
- .apply() & .check()
- importlib_util & pytest
- Learner & .refusals()
- Message & One email message, in a thr...
- ._trace() & One line per decision, an...
- app.js & action()
- Attachment & .__post_init__()
- Manifest & .lane_cases()
- test_graph_state.py & message()
- AnswerQueue & .get()
- digest_of() & A short stable digest o...
- collections_abc & dataclasses
- bandit.py & ._approved()
- build_provider() & ProposalError
- mask_for_llm() & Sanitize subject and...
- PresidioMasker & .forget_thread()
- A reconstructed thread: its roots, pl...
- arrivals() & dataset_routes()
- io & test_loop.py
- _claim_from_record() & _claim_record()
- test_triage.py & message()
- EntityRecognizer & RecognizerResult
- langgraph_checkpoint_memory & Walk a ...
- .__init__() & Any
- test_graph_resume.py & approval_for()
- AnalyzerEngine & presidio_analyzer
- ArgumentParser & build_parser()
- base64 & injection.py
- build_reply_tree() & Reconstruct the ...
- Everything a commit can change, and n...
- Endpoint & .label()
- argparse & dotenv
- _action_words() & _bears_on()
- classify_action() & _extract_recipien...
- ExplodingPolicy & .decide()
- InterruptHook & IO
- decision_sources() & DecisionSource
- Who an email claims to come from, and...
- RuntimeError & The trace could not be...
- ABC & ArchiveEmail
- EmailEvent & .message_id()
- ._ask() & .propose()
- EffectLog & .__init__()
- first_interrupt_of() & gold_route()
- CaptureFixture & MonkeyPatch
- .posterior() & Posterior
- plan_deviation() & Any
- email_tools.py & action_vocabulary()
- block_of() & interrupting_case_ids()
- LoopReport & .asked_after()
- get_token_map() & .get_instance()
- ui/__init__.py & Block
- close_input() & Tell a scripted run t...
- Notification & NotifyUser
- parametrize & Verify that every tool ...
- .may_learn() & .why_not()
- _order_key() & _ordered_roots()
- RuntimeError & Raised when a run cann...
- guesses() & manifest()
- email-autonomy-agent

## God Nodes (most connected - your core abstractions)
1. `Route` - 100 edges
2. `ChatRunner` - 50 edges
3. `Message` - 47 edges
4. `ClaimStore` - 47 edges
5. `Manifest` - 41 edges
6. `Claim` - 39 edges
7. `Case` - 37 edges
8. `Triage` - 37 edges
9. `Lane` - 36 edges
10. `ActionPayload` - 36 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_a_line_is_refused_when_nothing_waits()` --uses--> `Session`  [INFERRED]
  tests/test_ui_session.py → src/agent/ui/session.py
- `set_session()` --uses--> `Session`  [INFERRED]
  frontend-ui/server.py → src/agent/ui/session.py
- `Handler` --uses--> `Session`  [INFERRED]
  frontend-ui/server.py → src/agent/ui/session.py
- `test_a_calibration_run_counts_what_the_user_said()` --uses--> `Learner`  [INFERRED]
  tests/learning/test_updates.py → src/agent/autonomy/bandit.py

## Import Cycles
- None detected.

## Communities (99 total, 16 thin omitted)

### Community 0 - "hashlib & json"
Cohesion: 0.05
Nodes (50): hashlib, json, EventStream, _json_default(), Any, datetime, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, A stable hash of the replay log. (+42 more)

### Community 1 - "parse_proposal() & ProposalGateway"
Cohesion: 0.08
Nodes (41): parse_proposal(), ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., Validate one provider answer. Anything unexpected is an error, not a default., BrokenProvider, message(), parametrize, The model proposal gateway: untrusted output, one repair, then fail closed. (+33 more)

### Community 2 - "CompiledStateGraph & langgraph_graph"
Cohesion: 0.08
Nodes (43): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), _bound(), build_graph() (+35 more)

### Community 3 - "tools/__init__.py & Simulated tools a..."
Cohesion: 0.07
Nodes (35): Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _digest(), _notify_text(), _params_brief() (+27 more)

### Community 4 - "learning/__init__.py & claims.py"
Cohesion: 0.12
Nodes (35): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Capability, ConsentRequired, Grant, LearningConsent, RuntimeError (+27 more)

### Community 5 - "Lane & LaneView"
Cohesion: 0.06
Nodes (31): Lane, LaneView, RuntimeError, StrEnum, Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case. (+23 more)

### Community 6 - "re & feedback.py"
Cohesion: 0.09
Nodes (36): re, _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed() (+28 more)

### Community 7 - "dataset.py & _attachment()"
Cohesion: 0.10
Nodes (33): _attachment(), _case_from_mail_row(), _case_from_row(), CaseLabels, event_from_row(), ManifestError, _message(), Any (+25 more)

### Community 8 - "Random & .__init__()"
Cohesion: 0.10
Nodes (24): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+16 more)

### Community 9 - "confirm_claim() & confirm_words()"
Cohesion: 0.11
Nodes (33): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means. (+25 more)

### Community 10 - "ActionPayload & floor_check()"
Cohesion: 0.09
Nodes (34): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated. (+26 more)

### Community 11 - ".__post_init__() & ClaimError"
Cohesion: 0.11
Nodes (28): ClaimError, ClaimScope, ValueError, Raised when a claim is underspecified, or about something never stored., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., _require_text() (+20 more)

### Community 12 - "Decision & .interrupts()"
Cohesion: 0.13
Nodes (16): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.… (+8 more)

### Community 13 - "floor.py & ActionClass"
Cohesion: 0.13
Nodes (29): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+21 more)

### Community 14 - "AbstractEventLoop & BaseHTTPRequestHa..."
Cohesion: 0.13
Nodes (14): AbstractEventLoop, BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent. (+6 more)

### Community 15 - "asyncio & os"
Cohesion: 0.11
Nodes (19): asyncio, os, Protocol, _domain(), proposal_from(), The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered. (+11 more)

### Community 16 - "Namespace & The pair's name, so a run..."
Cohesion: 0.14
Nodes (27): Namespace, The pair's name, so a run says where a proposal could have come from., graph_run(), _keep_rules(), loop_run(), _open_store(), _policy(), _proposing() (+19 more)

### Community 17 - "_dependencies_first() & dependencies_..."
Cohesion: 0.11
Nodes (28): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them. (+20 more)

### Community 18 - "test_floor.py & Unit tests for the de..."
Cohesion: 0.07
Nodes (28): Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles., An authority claim we cannot tie to a sender address is unresolved, not trusted., An in-org sender claiming an internal role is not an authority spoof. (+20 more)

### Community 19 - "Command & GraphOutcome"
Cohesion: 0.12
Nodes (17): Command, GraphOutcome, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A… (+9 more)

### Community 20 - "Case & .labelled()"
Cohesion: 0.13
Nodes (24): Case, Whether this case carries the dataset's answer at all., One dataset row: its lane, its canonical event, its labels and the raw record., The four autonomy outcomes a candidate action can be routed to.…, Immutable outcome of evaluating a proposed action against the safety floor., Route, SafetyVerdict, Streaming inbox simulator: arrival schedule, chat loop and reply-tree… (+16 more)

### Community 21 - "OutOfOrderEventError & Reject a strea..."
Cohesion: 0.12
Nodes (27): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, The dataset's answers live on the Case, so a decision path cannot read them. (+19 more)

### Community 22 - "_label_derived() & label_for()"
Cohesion: 0.11
Nodes (21): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), Proposal, The route this mail compels on the persona's own account, or None when free.…, An untrusted suggestion. Nothing acts on it without the floor. (+13 more)

### Community 23 - "build_registry() & Every simulated to..."
Cohesion: 0.16
Nodes (25): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+17 more)

### Community 24 - ".apply() & .check()"
Cohesion: 0.16
Nodes (13): CreateDraft, _email_id(), LabelEmail, Any, Writes a private draft. Reversible, and never a send., A send that validates like a real one and never leaves the mailbox. Recipients…, Applies one label to one message., SendEmail (+5 more)

### Community 25 - "importlib_util & pytest"
Cohesion: 0.11
Nodes (23): importlib_util, pytest, _call(), Any, Path, A choice the page must not offer: nothing the user says takes this one off the…, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET. (+15 more)

### Community 26 - "Learner & .refusals()"
Cohesion: 0.17
Nodes (21): Learner, Counts what the user said into posteriors, once per event, never from silence.…, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., FeedbackKind, StrEnum, What the user did after seeing a decision. Values are the dataset's…, feedback() (+13 more)

### Community 27 - "Message & One email message, in a thr..."
Cohesion: 0.12
Nodes (19): Message, One email message, in a thread, in one direction., The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), RuleProvider, amount_in() (+11 more)

### Community 28 - "._trace() & One line per decision, an..."
Cohesion: 0.15
Nodes (21): One line per decision, and one per reply: ids, hashes, bounded records., hint_fields(), message_digest(), _plain(), prepared_fields(), Any, What was committed. Effect targets are scrubbed by the sink., An enum becomes its value, so a round trip through the checkpointer is exact. (+13 more)

### Community 29 - "app.js & action()"
Cohesion: 0.23
Nodes (21): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), poll() (+13 more)

### Community 30 - "Attachment & .__post_init__()"
Cohesion: 0.12
Nodes (17): Attachment, DuplicateEventError, EventValidationError, ValueError, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text() (+9 more)

### Community 31 - "Manifest & .lane_cases()"
Cohesion: 0.13
Nodes (18): Manifest, Path, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows., Every case in one lane, in sequence order., Counts per split and per lane, for the validator's output., view(), manifest() (+10 more)

### Community 32 - "test_graph_state.py & message()"
Cohesion: 0.13
Nodes (19): message(), Path, Not just the serde: a compiled graph through a saver hands back the same values., The allowlist is the schema: a new field is traceable, not silently dropped., The body and subject are inputs to the decision, and must not reach the file., No line may contain these words, in a key or in a value., Error handling at the boundary: a path that is not a file names itself., The run that dies is the one worth tracing, so lines are flushed as written. (+11 more)

### Community 33 - "AnswerQueue & .get()"
Cohesion: 0.13
Nodes (10): AnswerQueue, Path, One calibration run, driven a line at a time. The run is the one the CLI drives…, Load the lane and begin the run. A failure here is the caller's to report., Called while a decision is on screen and before its line is read., Append one block, with the number the page polls from., The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed. (+2 more)

### Community 34 - "digest_of() & A short stable digest o..."
Cohesion: 0.20
Nodes (17): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file. (+9 more)

### Community 35 - "collections_abc & dataclasses"
Cohesion: 0.18
Nodes (13): collections_abc, dataclasses, datetime, enum, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).…, Windowed-random arrival scheduling (plan Commit 3.5). A lane replayed in… (+5 more)

### Community 36 - "bandit.py & ._approved()"
Cohesion: 0.14
Nodes (13): Count one explicit decision about one bucket, at most once. False if uncounted., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, FeedbackEvent, is_learnable(), What the user did with a decision, and whether it may teach the learner., Return whether this kind of feedback may update the learner., Whether a learner may use this, which is the kind's own rule. (+5 more)

### Community 37 - "build_provider() & ProposalError"
Cohesion: 0.15
Nodes (16): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch (+8 more)

### Community 38 - "mask_for_llm() & Sanitize subject and..."
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker & .forget_thread()"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "A reconstructed thread: its roots, pl..."
Cohesion: 0.14
Nodes (15): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _body_lines(), _prior_lines(), Reconstruct one case's thread, bounded by the reply-tree caps., The arriving mail the way an inbox shows it. Sender, recipients, subject, body… (+7 more)

### Community 41 - "arrivals() & dataset_routes()"
Cohesion: 0.14
Nodes (18): arrivals(), dataset_routes(), labelled_routes(), Path, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints., The plan's check, against the labels: only ask-first and escalate lines wait. (+10 more)

### Community 42 - "io & test_loop.py"
Cohesion: 0.20
Nodes (16): io, asked(), _drained(), loop(), Queue, Nothing hangs on a prompt the script never feeds: it is told a line that does…, A named case still waits for the second line, so an unanswered echo stores…, test_a_decision_the_script_does_not_answer_is_passed_on() (+8 more)

### Community 43 - "_claim_from_record() & _claim_record()"
Cohesion: 0.13
Nodes (11): _claim_from_record(), _claim_record(), Any, datetime, Path, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''. (+3 more)

### Community 44 - "test_triage.py & message()"
Cohesion: 0.18
Nodes (13): message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker(), test_an_ambiguous_message_asks_for_a_model(), test_an_unverified_authority_claim_is_spoofing() (+5 more)

### Community 45 - "EntityRecognizer & RecognizerResult"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 46 - "langgraph_checkpoint_memory & Walk a ..."
Cohesion: 0.25
Nodes (15): langgraph_checkpoint_memory, Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing() (+7 more)

### Community 47 - ".__init__() & Any"
Cohesion: 0.17
Nodes (13): Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did., Feedback a learner would accept, which is nothing until Commit 3.6., How many times a tool actually ran, counted from the receipts. (+5 more)

### Community 48 - "test_graph_resume.py & approval_for()"
Cohesion: 0.23
Nodes (15): approval_for(), The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, The yes a reviewer would send back for the work they were shown., session(), test_a_crash_before_the_work_ran_leaves_the_decision_waiting(), test_a_decision_that_moved_between_asking_and_answering_is_refused() (+7 more)

### Community 49 - "AnalyzerEngine & presidio_analyzer"
Cohesion: 0.14
Nodes (13): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+5 more)

### Community 50 - "ArgumentParser & build_parser()"
Cohesion: 0.14
Nodes (15): ArgumentParser, build_parser(), main(), The flags both replay paths take: which mail, which lane, who proposes, a trace., Entry point for the ``wajo`` console script., The CLI's argument grammar., _replay_flags(), CaptureFixture (+7 more)

### Community 51 - "base64 & injection.py"
Cohesion: 0.18
Nodes (14): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, Prompt injection tripwires and plan-deviation verification. Zero LLM dependence…, Scan untrusted email content and headers for prompt injection indicators. (+6 more)

### Community 52 - "build_reply_tree() & Reconstruct the ..."
Cohesion: 0.30
Nodes (14): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected(), test_cycle_is_walked_once(), test_depth_cap_stops_the_walk() (+6 more)

### Community 53 - "Everything a commit can change, and n..."
Cohesion: 0.15
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 54 - "Endpoint & .label()"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "argparse & dotenv"
Cohesion: 0.17
Nodes (12): argparse, dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., Point the server at a session, which is what the tests and the page both need., serve(), set_session() (+4 more)

### Community 56 - "_action_words() & _bears_on()"
Cohesion: 0.21
Nodes (10): _action_words(), _bears_on(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The claims in force that bear on one mail, narrowest first. A claim with no…, The work in the user's own terms, from the pipeline's action vocabulary., One thing to remember, with the evidence that justifies it. Required by the… (+2 more)

### Community 57 - "classify_action() & _extract_recipien..."
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 58 - "ExplodingPolicy & .decide()"
Cohesion: 0.18
Nodes (12): ExplodingPolicy, The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case., Fixture case ids in the order the windows deliver them., scheduled_case_ids(), test_a_failing_policy_names_the_case_it_stopped_on(), test_a_line_queued_before_the_first_arrival_has_no_decision_to_bind_to(), test_an_arrival_shows_the_mail_a_production_inbox_shows() (+4 more)

### Community 59 - "InterruptHook & IO"
Cohesion: 0.17
Nodes (9): InterruptHook, IO, Queue, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., run_loop(), ScriptedReplies (+1 more)

### Community 60 - "decision_sources() & DecisionSource"
Cohesion: 0.17
Nodes (12): decision_sources(), DecisionSource, Which decision source produced the routes in a labelled run., Sender, subject and body are inputs in production; labels are only answers.…, Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines…, run_typed(), test_end_of_input_is_silence_not_approval(), test_one_reply_then_silence_for_the_rest() (+4 more)

### Community 61 - "Who an email claims to come from, and..."
Cohesion: 0.18
Nodes (10): Who an email claims to come from, and whether that claim is verified.…, SenderIdentity, _address(), The address a reader sees, with its unverified display name left visible., History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread() (+2 more)

### Community 62 - "RuntimeError & The trace could not be..."
Cohesion: 0.24
Nodes (6): RuntimeError, The trace could not be written where it was asked to go., Append-only JSONL trace, one line per decision, flushed as it is written., Close the file. Safe to call twice, which an except-block may do., TraceError, TraceSink

### Community 63 - "ABC & ArchiveEmail"
Cohesion: 0.20
Nodes (7): ABC, ArchiveEmail, Files a message out of the inbox., One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit., Tool

### Community 64 - "EmailEvent & .message_id()"
Cohesion: 0.20
Nodes (7): EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The manifest hands out EmailEvents, not raw rows., test_events_are_canonical_events()

### Community 65 - "._ask() & .propose()"
Cohesion: 0.22
Nodes (6): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask the provider, repair once if the answer does not parse, then fail closed., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…

### Community 66 - "EffectLog & .__init__()"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 67 - "first_interrupt_of() & gold_route()"
Cohesion: 0.24
Nodes (10): first_interrupt_of(), gold_route(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing() (+2 more)

### Community 68 - "CaptureFixture & MonkeyPatch"
Cohesion: 0.24
Nodes (9): CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., test_a_broken_input_stream_ends_the_run_instead_of_hanging(), test_buffered_input_is_recorded_as_corrections_not_answers(), test_cli_replays_the_fixture(), test_cli_seed_flag_changes_the_replay_digest() (+1 more)

### Community 69 - ".posterior() & Posterior"
Cohesion: 0.22
Nodes (5): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., What is believed about this bucket, through the chain when it has no history.

### Community 70 - "plan_deviation() & Any"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 71 - "email_tools.py & action_vocabulary()"
Cohesion: 0.22
Nodes (7): action_vocabulary(), Draft, The simulated email tools (Phase 3.3). Six tools over one in-memory mailbox:…, What a proposer may ask for, and what each action needs, as prompt lines., A private draft. Preparation, not sending., Read-only: returns the message it was pointed at., ReadEmail

### Community 72 - "block_of() & interrupting_case_ids()"
Cohesion: 0.22
Nodes (9): block_of(), interrupting_case_ids(), One arrival's text, from its header up to the next arrival., A user typing rules at an escalation would be teaching the wrong thing., Fixture cases whose gold route asks the user, in delivery order., test_a_correction_typed_at_a_prompt_binds_to_that_decision(), test_a_prompt_no_rule_can_quieten_says_so(), test_a_reply_prompt_is_reported_for_the_case_that_waits() (+1 more)

### Community 73 - "LoopReport & .asked_after()"
Cohesion: 0.25
Nodes (5): LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 74 - "get_token_map() & .get_instance()"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 75 - "ui/__init__.py & Block"
Cohesion: 0.25
Nodes (6): Block, classify(), Any, One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 76 - "close_input() & Tell a scripted run t..."
Cohesion: 0.29
Nodes (7): close_input(), Tell a scripted run that no further lines are coming (EOF)., The wiring, not just the rule: a line confirmed at a prompt moves a posterior., test_a_calibration_run_counts_what_the_user_said(), hook(), hook(), hook()

### Community 77 - "Notification & NotifyUser"
Cohesion: 0.29
Nodes (4): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else.

### Community 78 - "parametrize & Verify that every tool ..."
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 79 - ".may_learn() & .why_not()"
Cohesion: 0.33
Nodes (3): datetime, Whether this consent still stands at a moment., One line a transcript can print about why nothing was kept.

### Community 80 - "_order_key() & _ordered_roots()"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

### Community 81 - "RuntimeError & Raised when a run cann..."
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

### Community 82 - "guesses() & manifest()"
Cohesion: 1.00
Nodes (3): guesses(), manifest(), fixture

## Knowledge Gaps
- **4 isolated node(s):** `ROUTES`, `CHOICES`, `email-autonomy-agent`, `WAJO Calibration UI`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 702 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Case & .labelled()` to `parse_proposal() & ProposalGateway`, `tools/__init__.py & Simulated tools a...`, `learning/__init__.py & claims.py`, `re & feedback.py`, `confirm_claim() & confirm_words()`, `ActionPayload & floor_check()`, `.__post_init__() & ClaimError`, `Decision & .interrupts()`, `floor.py & ActionClass`, `asyncio & os`, `test_floor.py & Unit tests for the de...`, `OutOfOrderEventError & Reject a strea...`, `_label_derived() & label_for()`, `build_registry() & Every simulated to...`, `importlib_util & pytest`, `Learner & .refusals()`, `Message & One email message, in a thr...`, `._trace() & One line per decision, an...`, `Manifest & .lane_cases()`, `collections_abc & dataclasses`, `bandit.py & ._approved()`, `arrivals() & dataset_routes()`, `_claim_from_record() & _claim_record()`, `_action_words() & _bears_on()`, `classify_action() & _extract_recipien...`, `decision_sources() & DecisionSource`, `first_interrupt_of() & gold_route()`, `block_of() & interrupting_case_ids()`, `parametrize & Verify that every tool ...`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `Manifest` connect `Manifest & .lane_cases()` to `hashlib & json`, `AnswerQueue & .get()`, `parse_proposal() & ProposalGateway`, `first_interrupt_of() & gold_route()`, `learning/__init__.py & claims.py`, `Lane & LaneView`, `dataset.py & _attachment()`, `block_of() & interrupting_case_ids()`, `io & test_loop.py`, `langgraph_checkpoint_memory & Walk a ...`, `asyncio & os`, `Namespace & The pair's name, so a run...`, `test_graph_resume.py & approval_for()`, `guesses() & manifest()`, `ExplodingPolicy & .decide()`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `PresidioMasker` connect `PresidioMasker & .forget_thread()` to `AnalyzerEngine & presidio_analyzer`, `get_token_map() & .get_instance()`, `EntityRecognizer & RecognizerResult`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 81 inferred relationships involving `Route` (e.g. with `proposal_from()` and `FeedbackEvent`) actually correct?**
  _`Route` has 81 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `ChatRunner` (e.g. with `Learner` and `Case`) actually correct?**
  _`ChatRunner` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `Message` (e.g. with `RememberedProvider` and `_mail_rules()`) actually correct?**
  _`Message` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `ClaimStore` (e.g. with `RememberedProvider` and `_keep_rules()`) actually correct?**
  _`ClaimStore` has 25 INFERRED edges - model-reasoned connections that need verification._