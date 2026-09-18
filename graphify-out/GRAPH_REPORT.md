# Graph Report - ai-email-agent  (2026-09-18)

## Corpus Check
- 79 files · ~62,006 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1855 nodes · 4920 edges · 103 communities (95 shown, 8 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 838 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aee3d72f`
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
- floor.py
- Handler
- LoopReport
- graph_run
- schedule
- injection.py
- GraphState
- Case
- test_events.py
- runner.py
- test_sim_tools.py
- email_tools.py
- Session
- FeedbackEvent
- Message
- state.py
- app.js
- events.py
- ManifestError
- preferences.py
- ProposalGateway
- TraceSink
- test_floor_protection.py
- test_replay.py
- build_provider
- mask_for_llm
- PresidioMasker
- Manifest
- run_typed
- test_loop.py
- Claim
- test_triage.py
- ContextPhoneRecognizer
- run_simulation
- .effects
- test_graph_resume.py
- masker.py
- Routes
- safety/__init__.py
- test_sim.py
- ClaimScope
- OpenAICompatibleProvider
- cli.py
- Posterior
- Transcript
- Cutoffs
- replay
- interrupting_case_ids
- run_scenario
- parse_proposal
- view
- EmailEvent
- _feedback
- EffectLog
- _dependencies_first
- main
- first_interrupt_of
- build_parser
- .start
- ProposalError
- ._line
- get_token_map
- Block
- ._run
- timedelta
- _server
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- _order_key
- ScriptedProvider
- Workflow: graphify
- email-autonomy-agent
- router.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- set_session

## God Nodes (most connected - your core abstractions)
1. `Route` - 149 edges
2. `Router` - 59 edges
3. `Learner` - 52 edges
4. `ChatRunner` - 52 edges
5. `Message` - 49 edges
6. `ClaimStore` - 49 edges
7. `Manifest` - 45 edges
8. `Bucket` - 44 edges
9. `Case` - 42 edges
10. `Claim` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Scenario` --uses--> `Route`  [INFERRED]
  evals/run_canonical.py → src/agent/safety/floor.py
- `Transcript` --uses--> `Routing`  [INFERRED]
  evals/run_canonical.py → src/agent/autonomy/router.py
- `Transcript` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py
- `Transcript` --uses--> `Claim`  [INFERRED]
  evals/run_canonical.py → src/agent/memory/claims.py
- `Transcript` --uses--> `Route`  [INFERRED]
  evals/run_canonical.py → src/agent/safety/floor.py

## Import Cycles
- None detected.

## Communities (103 total, 8 thin omitted)

### Community 0 - "SeededClock"
Cohesion: 0.13
Nodes (15): EventStream, datetime, A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., An append-only log of arriving events. There is no update, no delete and no…, SeededClock, An arrival numbered before the last one is out of order, not a new arrival. (+7 more)

### Community 1 - "test_gateway.py"
Cohesion: 0.20
Nodes (13): message(), The model proposal gateway: untrusted output, one repair, then fail closed., A proposer that has to guess a tool name from a dataset id guesses wrong., One vocabulary: the offline stand-in cannot drift from the model's schema., SlowProvider, test_a_credential_request_escalates_even_from_inside(), test_a_persona_rule_leaves_an_ordinary_ask_alone(), test_a_provider_that_never_answers_times_out() (+5 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (36): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), build_graph(), _case() (+28 more)

### Community 3 - "registry.py"
Cohesion: 0.06
Nodes (42): ABC, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _digest(), _notify_text() (+34 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (40): ClaimStore, datetime, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Capability (+32 more)

### Community 5 - "Learner"
Cohesion: 0.11
Nodes (28): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The confirmed rule that refused this arm, or '' when the user has not refused…, FeedbackKind, StrEnum, What the user did after seeing a decision. Values are the dataset's… (+20 more)

### Community 6 - "feedback.py"
Cohesion: 0.10
Nodes (33): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+25 more)

### Community 7 - "dataset.py"
Cohesion: 0.14
Nodes (26): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime, Dataset manifest and the split firewall (Phase 3.2). The dataset is loaded… (+18 more)

### Community 8 - "Bucket"
Cohesion: 0.11
Nodes (24): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.12
Nodes (30): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a… (+22 more)

### Community 10 - "test_floor.py"
Cohesion: 0.06
Nodes (55): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, parametrize, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify that every tool and parameter boundary resolves to the exact ActionClass., FLR-001: Financial transactions in action params must escalate. (+47 more)

### Community 11 - "session_grant"
Cohesion: 0.14
Nodes (24): datetime, ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), What a session carries when a human is present and typing. Consent is granted…, session_grant(), memory() (+16 more)

### Community 12 - "ChatRunner"
Cohesion: 0.07
Nodes (34): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _address() (+26 more)

### Community 13 - "floor.py"
Cohesion: 0.11
Nodes (37): ActionClass, classify_action(), EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement() (+29 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (10): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one. (+2 more)

### Community 15 - "LoopReport"
Cohesion: 0.25
Nodes (5): LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 16 - "graph_run"
Cohesion: 0.13
Nodes (26): Namespace, The pair's name, so a run says where a proposal could have come from., graph_run(), _keep_rules(), loop_run(), _open_store(), _policy(), _proposing() (+18 more)

### Community 17 - "schedule"
Cohesion: 0.18
Nodes (19): Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., release_order(), schedule(), fake(), lane(), SimpleNamespace, Phase 3.5: windowed-random arrival scheduling. (+11 more)

### Community 18 - "injection.py"
Cohesion: 0.08
Nodes (28): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, Prompt injection tripwires and plan-deviation verification. Zero LLM dependence…, Scan untrusted email content and headers for prompt injection indicators. (+20 more)

### Community 19 - "GraphState"
Cohesion: 0.11
Nodes (22): Command, _bound(), GraphError, GraphOutcome, GraphSession, Any, RuntimeError, Hand a node its runtime. The graph only ever sees the state. (+14 more)

### Community 20 - "Case"
Cohesion: 0.14
Nodes (20): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Case, Whether this case carries the dataset's answer at all., One dataset row: its lane, its canonical event, its labels and the raw record., Proposal (+12 more)

### Community 21 - "test_events.py"
Cohesion: 0.11
Nodes (29): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, A replayed stream can refuse a shape it does not understand. (+21 more)

### Community 22 - "runner.py"
Cohesion: 0.12
Nodes (30): asyncio, collections_abc, dataclasses, The four reference cases, run end to end and printed as transcripts. Each case…, os, pathlib, re, _persona_checked() (+22 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.08
Nodes (30): action_vocabulary(), ArchiveEmail, build_registry(), CreateDraft, Draft, _email_id(), LabelEmail, Notification (+22 more)

### Community 25 - "Session"
Cohesion: 0.13
Nodes (19): importlib_util, pytest, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one… (+11 more)

### Community 26 - "FeedbackEvent"
Cohesion: 0.14
Nodes (12): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, is_learnable() (+4 more)

### Community 27 - "Message"
Cohesion: 0.09
Nodes (29): Message, One email message, in a thread, in one direction., _label_derived(), label_for(), _mail_rules(), The offline provider: proposes from triage, no network, deterministic. It is a…, The rule proposal, before it is serialised like any other provider's., The folder the pipeline names for this mail, or None when it names none. (+21 more)

### Community 28 - "state.py"
Cohesion: 0.09
Nodes (33): The route chosen, and everything that was ruled out on the way., The chosen route's expected loss, in handoffs., One line for a transcript or a reason. Deliberately terse: a trace digests a…, Routing, Record the route the router chose, which is what authorization checks., route(), One line per decision, and one per reply: ids, hashes, bounded records., digest_of() (+25 more)

### Community 29 - "app.js"
Cohesion: 0.23
Nodes (21): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), poll() (+13 more)

### Community 30 - "events.py"
Cohesion: 0.16
Nodes (12): enum, Attachment, DuplicateEventError, EventValidationError, ValueError, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema. (+4 more)

### Community 31 - "ManifestError"
Cohesion: 0.15
Nodes (15): CaseLabels, ManifestError, ValueError, The dataset's answer for this case, for scoring and debugging only., Build a manifest from parsed rows, rejecting duplicate case ids and splits., Raised when the dataset itself violates the manifest schema., The dataset's ground truth for a case. These are answers: what the case was…, A bare KeyError says nothing about which of the cases is malformed. (+7 more)

### Community 32 - "preferences.py"
Cohesion: 0.10
Nodes (18): Protocol, _domain(), proposal_from(), The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., Answer from a claim where one bears on this mail, otherwise ask the inner one., What the user's own words amount to for this mail, if anything. (+10 more)

### Community 33 - "ProposalGateway"
Cohesion: 0.15
Nodes (14): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., The rules belong to the mail, so a model proposing a quiet route does not win., A small model copies the example it was shown, so the example carries no value., No folder for this mail means a blocked step at the registry, not a made-up one., The floor wins over a confident proposal, which is the whole contract., A provider that answers from a script, so the repair logic is testable., ScriptedProvider (+6 more)

### Community 34 - "TraceSink"
Cohesion: 0.08
Nodes (36): _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file., Keep the domain, drop the person: a local part becomes a digest. (+28 more)

### Community 35 - "test_floor_protection.py"
Cohesion: 0.11
Nodes (34): email_context_for(), floor_verdict_for(), Build the floor's view of a case from its canonical event., Return the floor verdict, the dataset action id and the tool name it mapped to., approve(), ask_again(), bucket_for(), case() (+26 more)

### Community 36 - "test_replay.py"
Cohesion: 0.07
Nodes (35): hashlib, Lane, StrEnum, Every case in one lane, in sequence order., Where a case sits relative to learning., Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:… (+27 more)

### Community 37 - "build_provider"
Cohesion: 0.19
Nodes (13): build_provider(), Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request., The request carries the schema, so a model cannot omit a key or invent an… (+5 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Manifest"
Cohesion: 0.15
Nodes (19): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Manifest, Path, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows., Counts per split and per lane, for the validator's output., view() (+11 more)

### Community 41 - "run_typed"
Cohesion: 0.12
Nodes (27): arrivals(), block_of(), dataset_routes(), labelled_routes(), DecisionSource, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints. (+19 more)

### Community 42 - "test_loop.py"
Cohesion: 0.13
Nodes (21): io, IO, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Types scripted lines at the decisions that wait for a human. A line handed over…, run_loop(), ScriptedReplies, asked(), _drained() (+13 more)

### Community 43 - "Claim"
Cohesion: 0.19
Nodes (10): _action_words(), _bears_on(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The claims in force that bear on one mail, narrowest first. A claim with no…, The work in the user's own terms, from the pipeline's action vocabulary., One thing to remember, with the evidence that justifies it. Required by the… (+2 more)

### Community 44 - "test_triage.py"
Cohesion: 0.16
Nodes (14): message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker(), test_an_ambiguous_message_asks_for_a_model(), test_an_unverified_authority_claim_is_spoofing() (+6 more)

### Community 45 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 46 - "run_simulation"
Cohesion: 0.05
Nodes (44): langgraph_checkpoint_memory, LaneView, RuntimeError, Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner. (+36 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.12
Nodes (23): approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The plan's crash matrix: whether the work ran or not, a resume applies it once. (+15 more)

### Community 49 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 50 - "Routes"
Cohesion: 0.25
Nodes (7): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "safety/__init__.py"
Cohesion: 0.10
Nodes (20): FloorRule, Representation of an audited, immutable safety floor rule., Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, Safety module: floor guardrails, action taxonomy, and injection tripwires., plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.… (+12 more)

### Community 52 - "test_sim.py"
Cohesion: 0.19
Nodes (19): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., Sender, subject and body are inputs in production; labels are only answers.… (+11 more)

### Community 53 - "ClaimScope"
Cohesion: 0.12
Nodes (15): _claim_from_record(), claim_id_for(), _claim_record(), ClaimScope, Any, Path, Write every claim to the store's file, one JSON object per line. The whole…, A stable id for the same claim said twice, so it is never stored twice. (+7 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.15
Nodes (9): Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to., A client for this endpoint. Imported here so offline runs need no SDK. (+1 more)

### Community 55 - "cli.py"
Cohesion: 0.18
Nodes (12): argparse, dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, json (+4 more)

### Community 56 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 57 - "Transcript"
Cohesion: 0.15
Nodes (12): main(), One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One canonical run: the pipeline's own output, plus what it decided and…, What the router considered, which every canonical run keeps., The route the run actually chose., Whether the run landed on the route the dataset says the case deserves. (+4 more)

### Community 58 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 59 - "replay"
Cohesion: 0.17
Nodes (12): Replay events through a fresh seeded stream., replay(), The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival., The log's order is the dataset's sequence order, not file order., A shuffled file replays identically, because order is sequence_index., test_a_different_seed_changes_the_log() (+4 more)

### Community 60 - "interrupting_case_ids"
Cohesion: 0.18
Nodes (10): ExplodingPolicy, interrupting_case_ids(), The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case., Fixture case ids in the order the windows deliver them., Fixture cases whose gold route asks the user, in delivery order., scheduled_case_ids(), test_a_correction_typed_at_a_prompt_binds_to_that_decision() (+2 more)

### Community 61 - "run_scenario"
Cohesion: 0.20
Nodes (10): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One reference case: the mail, what it is here to show, and the route it…, run_scenario(), Scenario, ClaimType, StrEnum (+2 more)

### Community 62 - "parse_proposal"
Cohesion: 0.27
Nodes (10): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., parametrize, The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses(), test_a_valid_answer_parses(), test_an_action_nothing_implements_resolves_to_itself(), test_an_unusable_answer_is_an_error_not_a_default() (+2 more)

### Community 63 - "view"
Cohesion: 0.20
Nodes (10): Reconstruct one case's thread, bounded by the reply-tree caps., thread_tree_for(), Path, If the read fails, the prompts must see end of input, not wait forever., On a real run: one line per arrival, and no mail text in any of them., test_a_broken_input_stream_ends_the_run_instead_of_hanging(), test_a_traced_run_writes_the_decision_and_never_the_mail(), test_every_case_in_the_fixture_is_processed() (+2 more)

### Community 64 - "EmailEvent"
Cohesion: 0.20
Nodes (7): EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The manifest hands out EmailEvents, not raw rows., test_events_are_canonical_events()

### Community 65 - "_feedback"
Cohesion: 0.24
Nodes (10): _feedback(), parametrize, Empty ids and malformed fields fail at construction, not at use., Each kind survives construction with explicit_for_learning intact., Silence is not approval": a non-decision claiming the learning flag fails., An explicit decision that disclaims learning is a bug, not a preference., test_every_feedback_kind_round_trips_with_its_flag(), test_explicit_decisions_must_be_flagged_learnable() (+2 more)

### Community 66 - "EffectLog"
Cohesion: 0.22
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 67 - "_dependencies_first"
Cohesion: 0.22
Nodes (9): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Keep the drawn order, moving a case after anything it says it waits for.…, _row_of() (+1 more)

### Community 68 - "main"
Cohesion: 0.23
Nodes (12): main(), Entry point for the ``wajo`` console script., test_the_cli_keeps_the_held_out_lane_shut(), CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, test_buffered_input_is_recorded_as_corrections_not_answers(), test_cli_refuses_to_open_the_sealed_lane() (+4 more)

### Community 69 - "first_interrupt_of"
Cohesion: 0.28
Nodes (9): first_interrupt_of(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing(), test_an_approval_releases_the_prepared_action_and_is_learnable() (+1 more)

### Community 70 - "build_parser"
Cohesion: 0.33
Nodes (7): ArgumentParser, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), Calibrating on the same mail twice asks once: the rule answers the second time., test_the_simulator_answers_from_a_saved_rule_without_asking()

### Community 71 - ".start"
Cohesion: 0.25
Nodes (5): AbstractEventLoop, _background_loop(), Load the lane and begin the run. A failure here is the caller's to report., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 72 - "ProposalError"
Cohesion: 0.33
Nodes (5): ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Ask the provider, repair once if the answer does not parse, then fail closed., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…

### Community 73 - "._line"
Cohesion: 0.33
Nodes (4): _json_default(), Any, A stable hash of the replay log., The canonical JSONL replay log: header line, then one line per arrival.

### Community 74 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 75 - "Block"
Cohesion: 0.22
Nodes (7): Block, classify(), Any, Append one block, with the number the page polls from., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 76 - "._run"
Cohesion: 0.17
Nodes (5): AnswerQueue, Path, The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Transcript

### Community 77 - "timedelta"
Cohesion: 0.29
Nodes (7): Nothing reads the wall clock, so time is frozen until the simulation moves it., A custom epoch and tick are honoured; a non-positive advance is refused., The seed offsets within the first minute, so replays stay plausible., test_clock_can_be_configured_but_not_moved_backwards(), test_clock_starts_at_the_dataset_epoch_and_only_moves_on_advance(), test_seed_offsets_the_start_but_keeps_the_epoch(), timedelta

### Community 78 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

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
Cohesion: 0.12
Nodes (35): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+27 more)

## Knowledge Gaps
- **13 isolated node(s):** `ROUTES`, `CHOICES`, `email-autonomy-agent`, `graphify`, `Steps` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `test_gateway.py`, `registry.py`, `Learner`, `feedback.py`, `ScopeAnchor`, `test_floor.py`, `session_grant`, `ChatRunner`, `floor.py`, `Case`, `test_events.py`, `runner.py`, `test_sim_tools.py`, `Session`, `FeedbackEvent`, `Message`, `state.py`, `events.py`, `preferences.py`, `ProposalGateway`, `test_floor_protection.py`, `Manifest`, `run_typed`, `Claim`, `run_simulation`, `safety/__init__.py`, `test_sim.py`, `ClaimScope`, `Transcript`, `interrupting_case_ids`, `run_scenario`, `parse_proposal`, `first_interrupt_of`, `router.py`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `preferences.py`, `ProposalGateway`, `test_replay.py`, `Learner`, `set_session`, `ClaimStore`, `Manifest`, `.start`, `Block`, `._run`, `ChatRunner`, `Handler`, `run_simulation`, `Case`, `runner.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Message` connect `Message` to `preferences.py`, `ProposalGateway`, `graph.py`, `test_gateway.py`, `TraceSink`, `dataset.py`, `ProposalError`, `ChatRunner`, `test_triage.py`, `_order_key`, `test_sim.py`, `test_events.py`, `runner.py`, `test_sim_tools.py`, `state.py`, `events.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 120 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 120 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `ChatRunner` (e.g. with `run_scenario()` and `Learner`) actually correct?**
  _`ChatRunner` has 29 INFERRED edges - model-reasoned connections that need verification._