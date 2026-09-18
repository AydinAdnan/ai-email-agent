# Graph Report - ai-email-agent  (2026-09-18)

## Corpus Check
- 83 files · ~67,024 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1999 nodes · 5255 edges · 104 communities (93 shown, 11 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 865 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b5ad063`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SeededClock
- test_gateway.py
- graph.py
- registry.py
- ClaimStore
- Learner
- feedback.py
- dataset.py
- Bucket
- ScopeAnchor
- test_floor.py
- session_grant
- ChatRunner
- VetoLevel
- Handler
- LoopReport
- cli.py
- ProposalGateway
- injection.py
- GraphError
- floor.py
- events.py
- test_sim.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- router.py
- test_triage.py
- state.py
- app.js
- EmailEvent
- drafts.py
- RememberedProvider
- test_predrafts.py
- trace.py
- test_floor_protection.py
- test_replay.py
- test_a_proposal_is_asked_for_under_the_enforced_schema
- test_pii.py
- PresidioMasker
- Manifest
- arrivals
- test_loop.py
- Claim
- test_ui_session.py
- main
- LaneView
- _claim_from_record
- test_graph_resume.py
- retrieve_style
- Routes
- run_typed
- test_graph.py
- ContextPhoneRecognizer
- OpenAICompatibleProvider
- SimulatedMailbox
- Routing
- run_canonical.py
- Cutoffs
- examples_from_row
- run_simulation
- ProposalRequest
- ProposalError
- classify_action
- plan_deviation
- test_events.py
- EffectLog
- runner.py
- RuleProvider
- ScriptedReplies
- SentExample
- masker.py
- .get_instance
- Validation
- ._line
- RecognizerResult
- session.py
- ExplodingPolicy
- test_a_traced_run_writes_the_decision_and_never_the_mail
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- Message
- Any
- Workflow: graphify
- email-autonomy-agent
- test_loss_matrix.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- StrEnum
- parametrize

## God Nodes (most connected - your core abstractions)
1. `Route` - 151 edges
2. `Router` - 59 edges
3. `ChatRunner` - 52 edges
4. `Learner` - 52 edges
5. `ClaimStore` - 49 edges
6. `Message` - 49 edges
7. `Manifest` - 46 edges
8. `Bucket` - 44 edges
9. `Case` - 43 edges
10. `Claim` - 42 edges

## Surprising Connections (you probably didn't know these)
- `test_the_salutation_follows_the_example_the_user_wrote_in()` --uses--> `SentExample`  [INFERRED]
  tests/test_predrafts.py → src/agent/drafts.py
- `test_a_draft_falls_back_to_the_mail_when_there_is_no_example()` --uses--> `Style`  [INFERRED]
  tests/test_predrafts.py → src/agent/drafts.py
- `test_a_draft_that_cannot_be_shown_escalates_instead_of_asking()` --uses--> `DraftCode`  [INFERRED]
  tests/test_predrafts.py → src/agent/drafts.py
- `drafting()` --uses--> `Drafting`  [INFERRED]
  tests/test_predrafts.py → src/agent/drafts.py
- `test_a_draft_that_cannot_be_shown_escalates_instead_of_asking()` --uses--> `Drafting`  [INFERRED]
  tests/test_predrafts.py → src/agent/drafts.py

## Import Cycles
- None detected.

## Communities (104 total, 11 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.08
Nodes (30): EventStream, datetime, Replay events through a fresh seeded stream., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., An append-only log of arriving events. There is no update, no delete and no…, replay() (+22 more)

### Community 1 - "test_gateway.py"
Cohesion: 0.16
Nodes (17): message(), MonkeyPatch, The model proposal gateway: untrusted output, one repair, then fail closed., A proposer that has to guess a tool name from a dataset id guesses wrong., One vocabulary: the offline stand-in cannot drift from the model's schema., SlowProvider, test_a_credential_request_escalates_even_from_inside(), test_a_persona_rule_leaves_an_ordinary_ask_alone() (+9 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (43): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), _bound(), build_graph() (+35 more)

### Community 3 - "registry.py"
Cohesion: 0.06
Nodes (44): ABC, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest() (+36 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (39): enum, pathlib, claim_id_for(), ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., A stable id for the same claim said twice, so it is never stored twice., Capability (+31 more)

### Community 5 - "Learner"
Cohesion: 0.15
Nodes (22): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The confirmed rule that refused this arm, or '' when the user has not refused…, FeedbackKind, StrEnum, What the user did after seeing a decision. Values are the dataset's… (+14 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (42): _action_for(), _claim_reading(), _clean_label(), confirm_claim(), confirm_words(), _decision_reading(), FeedbackContext, _from_context() (+34 more)

### Community 7 - "dataset.py"
Cohesion: 0.10
Nodes (33): _attachment(), _case_from_mail_row(), _case_from_row(), CaseLabels, event_from_row(), ManifestError, _message(), Any (+25 more)

### Community 8 - "Bucket"
Cohesion: 0.11
Nodes (24): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.12
Nodes (30): ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a…, The one reading the parser will not assume is the one it stores only when said. (+22 more)

### Community 10 - "test_floor.py"
Cohesion: 0.06
Nodes (55): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, parametrize, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify that every tool and parameter boundary resolves to the exact ActionClass., FLR-001: Financial transactions in action params must escalate. (+47 more)

### Community 11 - "session_grant"
Cohesion: 0.12
Nodes (26): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), What a session carries when a human is present and typing. Consent is granted…, session_grant(), Path, memory() (+18 more)

### Community 12 - "ChatRunner"
Cohesion: 0.07
Nodes (32): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., The draft this ask shows, or None when it shows none., _address(), _body_lines(), _bucket_of(), ChatRunner (+24 more)

### Community 13 - "VetoLevel"
Cohesion: 0.12
Nodes (27): ActionClass, EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion() (+19 more)

### Community 14 - "Handler"
Cohesion: 0.10
Nodes (21): argparse, BaseHTTPRequestHandler, dotenv, WAJO Calibration UI, Handler, main(), Any, Serve the calibration page. uv run python frontend-ui/server.py Standard… (+13 more)

### Community 15 - "LoopReport"
Cohesion: 0.17
Nodes (8): GraphOutcome, What a lane through the graph did., How many times a tool actually ran, counted from the receipts., LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 16 - "cli.py"
Cohesion: 0.11
Nodes (33): Namespace, The pair's name, so a run says where a proposal could have come from., graph_run(), _keep_rules(), loop_run(), _open_store(), _policy(), _proposing() (+25 more)

### Community 17 - "ProposalGateway"
Cohesion: 0.14
Nodes (15): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., The rules belong to the mail, so a model proposing a quiet route does not win., A small model copies the example it was shown, so the example carries no value., No folder for this mail means a blocked step at the registry, not a made-up one., The floor wins over a confident proposal, which is the whole contract., A provider that answers from a script, so the repair logic is testable., ScriptedProvider (+7 more)

### Community 18 - "injection.py"
Cohesion: 0.07
Nodes (31): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+23 more)

### Community 19 - "GraphError"
Cohesion: 0.14
Nodes (12): Command, GraphError, Any, RuntimeError, What resuming a held decision did, or why the answer could not be used., Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, The graph cannot continue, naming the case it stopped on. (+4 more)

### Community 20 - "floor.py"
Cohesion: 0.09
Nodes (34): os, re, _domain(), proposal_from(), What the user's own words amount to for this mail, if anything., One claim as a proposal, or None when the claim names no route., _label_derived(), label_for() (+26 more)

### Community 21 - "events.py"
Cohesion: 0.11
Nodes (19): Attachment, DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema. (+11 more)

### Community 22 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.12
Nodes (24): ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser, Any (+16 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.14
Nodes (30): parametrize, DraftCode, Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the…, validate_draft() (+22 more)

### Community 26 - "router.py"
Cohesion: 0.13
Nodes (17): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, is_learnable() (+9 more)

### Community 27 - "test_triage.py"
Cohesion: 0.11
Nodes (21): The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), amount_in(), The largest amount mentioned in a text, as a float., guesses(), manifest(), message(), fixture (+13 more)

### Community 28 - "state.py"
Cohesion: 0.13
Nodes (26): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields(), message_digest(), _plain(), prepared_fields() (+18 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "EmailEvent"
Cohesion: 0.14
Nodes (10): The lane's arriving events, in sequence order., EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread() (+2 more)

### Community 31 - "drafts.py"
Cohesion: 0.11
Nodes (24): Case, draft_reply(), Drafting, drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+16 more)

### Community 32 - "RememberedProvider"
Cohesion: 0.18
Nodes (10): Protocol, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, ProposalProvider, A source of untrusted proposal text., IO (+2 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.14
Nodes (22): drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its…, One of the three fixture cases whose route is an ask with a predraft. (+14 more)

### Community 34 - "trace.py"
Cohesion: 0.08
Nodes (39): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+31 more)

### Community 35 - "test_floor_protection.py"
Cohesion: 0.13
Nodes (28): approve(), ask_again(), bucket_for(), case(), one_case_view(), The floor's second hard requirement, as an executable proof. No posterior, no…, Count `count` approved-then-undone decisions, each worth three rejections., Route one arrival the way the pipeline does, with the user's own rule naming… (+20 more)

### Community 36 - "test_replay.py"
Cohesion: 0.06
Nodes (31): hashlib, json, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., Counts per split and per lane, with the dataset's real sizes., A replay can name the exact dataset it ran against. (+23 more)

### Community 37 - "test_a_proposal_is_asked_for_under_the_enforced_schema"
Cohesion: 0.32
Nodes (6): fake_client(), FakeCompletions, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request., The request carries the schema, so a model cannot omit a key or invent an…, test_a_proposal_is_asked_for_under_the_enforced_schema()

### Community 38 - "test_pii.py"
Cohesion: 0.12
Nodes (17): get_token_map(), Retrieve the current token to original value map for a thread., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Manifest"
Cohesion: 0.09
Nodes (35): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Lane, Manifest, Path, StrEnum, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows. (+27 more)

### Community 41 - "arrivals"
Cohesion: 0.14
Nodes (19): arrivals(), block_of(), dataset_routes(), labelled_routes(), The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints., One arrival's text, from its header up to the next arrival. (+11 more)

### Community 42 - "test_loop.py"
Cohesion: 0.13
Nodes (23): ArgumentParser, io, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), asked(), _drained() (+15 more)

### Community 43 - "Claim"
Cohesion: 0.19
Nodes (10): _action_words(), _bears_on(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The claims in force that bear on one mail, narrowest first. A claim with no…, The work in the user's own terms, from the pipeline's action vocabulary., One thing to remember, with the evidence that justifies it. Required by the… (+2 more)

### Community 44 - "test_ui_session.py"
Cohesion: 0.06
Nodes (45): importlib_util, pytest, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., release_order(), schedule(), fake(), lane() (+37 more)

### Community 45 - "main"
Cohesion: 0.15
Nodes (17): main(), Entry point for the ``wajo`` console script., CaptureFixture, MonkeyPatch, test_the_cli_keeps_the_held_out_lane_shut(), test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in(), CaptureFixture, MonkeyPatch (+9 more)

### Community 46 - "LaneView"
Cohesion: 0.10
Nodes (14): LaneView, RuntimeError, A lane-bound handle over the manifest. A view can only open cases in its own…, Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., Raised when code reaches across the learning/held-out firewall., SplitViolation (+6 more)

### Community 47 - "_claim_from_record"
Cohesion: 0.13
Nodes (11): _claim_from_record(), _claim_record(), Any, datetime, Path, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''. (+3 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.11
Nodes (25): approval_for(), Crash, Crashing, Flaky, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide. (+17 more)

### Community 49 - "retrieve_style"
Cohesion: 0.16
Nodes (21): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from. (+13 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "run_typed"
Cohesion: 0.13
Nodes (17): DecisionSource, Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., Sender, subject and body are inputs in production; labels are only answers.…, Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines…, run_typed(), test_a_correction_typed_at_a_prompt_binds_to_that_decision() (+9 more)

### Community 52 - "test_graph.py"
Cohesion: 0.18
Nodes (18): langgraph_checkpoint_memory, Walk a lane through the graph, one decision per checkpoint thread., run_graph(), PII masking and anonymization package., mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Path, The graph is not a second opinion: same proposals, same route, same receipts. (+10 more)

### Community 53 - "ContextPhoneRecognizer"
Cohesion: 0.23
Nodes (7): EntityRecognizer, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span., Detects US Social Security Numbers (SSN) accurately.

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "SimulatedMailbox"
Cohesion: 0.17
Nodes (4): build_registry(), Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., SimulatedMailbox

### Community 56 - "Routing"
Cohesion: 0.13
Nodes (10): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., The route chosen, and everything that was ruled out on the way., The chosen route's expected loss, in handoffs. (+2 more)

### Community 57 - "run_canonical.py"
Cohesion: 0.13
Nodes (19): main(), preference_for(), The four reference cases, run end to end and printed as transcripts. Each case…, The scoped preference a confirmed rule would leave behind for this sender.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route. (+11 more)

### Community 58 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 59 - "examples_from_row"
Cohesion: 0.21
Nodes (10): Any, examples_from_row(), How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Read one example from the shape a mailbox hands over., The consented sent examples a case carries, if the mailbox offered any. Not the…, style_limit(), The archive and its budget come from the mailbox's own rows, not from the… (+2 more)

### Community 60 - "run_simulation"
Cohesion: 0.15
Nodes (15): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+7 more)

### Community 61 - "ProposalRequest"
Cohesion: 0.18
Nodes (7): Answer from a claim where one bears on this mail, otherwise ask the inner one., ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., A model in the shape of the provider protocol, answering from a script., ScriptedProvider

### Community 62 - "ProposalError"
Cohesion: 0.16
Nodes (15): parse_proposal(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Ask the provider, repair once if the answer does not parse, then fail closed., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, Validate one provider answer. Anything unexpected is an error, not a default., parametrize (+7 more)

### Community 63 - "classify_action"
Cohesion: 0.22
Nodes (11): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+3 more)

### Community 64 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 65 - "test_events.py"
Cohesion: 0.09
Nodes (35): Reject a stream that repeats a case or message, or drifts out of order. Order…, validate_stream(), _event(), _feedback(), _load_dataset(), parametrize, Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, Empty ids and malformed fields fail at construction, not at use. (+27 more)

### Community 66 - "EffectLog"
Cohesion: 0.22
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 67 - "runner.py"
Cohesion: 0.06
Nodes (46): collections_abc, dataclasses, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Case, Whether this case carries the dataset's answer at all., One dataset row: its lane, its canonical event, its labels and the raw record., persona_demanded_route() (+38 more)

### Community 68 - "RuleProvider"
Cohesion: 0.28
Nodes (5): The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., RuleProvider, A gateway that keeps what the provider was allowed to see., Recording

### Community 69 - "ScriptedReplies"
Cohesion: 0.20
Nodes (7): InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., ScriptedReplies, The wiring, not just the rule: a line confirmed at a prompt moves a posterior., test_a_calibration_run_counts_what_the_user_said()

### Community 70 - "SentExample"
Cohesion: 0.20
Nodes (8): What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., The word the user opens with, borrowed from the best example and cited as such., One reply the user actually sent, consented for style., _salutation(), SentExample, Style

### Community 71 - "masker.py"
Cohesion: 0.20
Nodes (9): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, _clean_person_name(), _create_analyzer(), PII Masking with Microsoft Presidio (Phase 2). Provides a warm singleton…, Build the Presidio analyzer, preferring the large spaCy model. (+1 more)

### Community 72 - ".get_instance"
Cohesion: 0.25
Nodes (7): forget_thread(), Access or initialize the singleton PresidioMasker., Drop a thread's token registry and reverse map., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 74 - "._line"
Cohesion: 0.33
Nodes (4): _json_default(), Any, A stable hash of the replay log., The canonical JSONL replay log: header line, then one line per arrival.

### Community 76 - "session.py"
Cohesion: 0.09
Nodes (21): AbstractEventLoop, asyncio, ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, router, route out., AnswerQueue, _background_loop(), Block, classify() (+13 more)

### Community 78 - "test_a_traced_run_writes_the_decision_and_never_the_mail"
Cohesion: 0.67
Nodes (3): Path, On a real run: one line per arrival, and no mail text in any of them., test_a_traced_run_writes_the_decision_and_never_the_mail()

### Community 79 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 80 - "Message"
Cohesion: 0.16
Nodes (15): datetime, Message, One email message, in a thread, in one direction., _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A reconstructed thread: its roots, plus every message's children by parent id.… (+7 more)

### Community 88 - "test_loss_matrix.py"
Cohesion: 0.16
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "Route"
Cohesion: 0.11
Nodes (38): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+30 more)

## Knowledge Gaps
- **14 isolated node(s):** `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES`, `Silence is not approval` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `test_gateway.py`, `registry.py`, `ClaimStore`, `Learner`, `feedback.py`, `ScopeAnchor`, `test_floor.py`, `session_grant`, `ChatRunner`, `VetoLevel`, `cli.py`, `ProposalGateway`, `injection.py`, `floor.py`, `events.py`, `test_sim_tools.py`, `router.py`, `test_triage.py`, `state.py`, `test_predrafts.py`, `test_floor_protection.py`, `Manifest`, `arrivals`, `Claim`, `test_ui_session.py`, `_claim_from_record`, `test_graph_resume.py`, `run_typed`, `Routing`, `run_canonical.py`, `ProposalError`, `runner.py`, `RuleProvider`, `test_loss_matrix.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `Bucket` connect `Bucket` to `Route`, `runner.py`, `Cutoffs`, `Learner`, `test_floor_protection.py`, `ChatRunner`, `router.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `ChatRunner` connect `ChatRunner` to `SeededClock`, `Route`, `runner.py`, `ClaimStore`, `Learner`, `feedback.py`, `graph.py`, `registry.py`, `Claim`, `session.py`, `state.py`, `LaneView`, `Message`, `SimulatedMailbox`, `run_canonical.py`, `router.py`, `run_simulation`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `ChatRunner` (e.g. with `run_scenario()` and `Learner`) actually correct?**
  _`ChatRunner` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 26 INFERRED edges - model-reasoned connections that need verification._