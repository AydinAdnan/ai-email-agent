# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 93 files · ~81,965 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2355 nodes · 6308 edges · 113 communities (98 shown, 15 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 1052 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `adba3333`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- policy.py
- graph.py
- .prepare
- ClaimStore
- Ledger
- feedback.py
- dataset.py
- Bucket
- ScopeAnchor
- floor_check
- test_claim_schema.py
- ChatRunner
- ActionPayload
- Handler
- _server
- test_graph_state.py
- HeldOutReport
- test_floor.py
- injection.py
- test_gateway.py
- Tool
- test_sim.py
- test_sim_tools.py
- Effect
- test_draft_validation.py
- .render
- ProposalError
- state
- app.js
- VetoLevel
- drafts.py
- ReplyTree
- test_predrafts.py
- Posterior
- Learner
- test_replay.py
- Transcript
- mask_for_llm
- masker.py
- Session
- run_typed
- email_tools.py
- claims.py
- schedule
- main
- LaneView
- test_triage.py
- test_graph_resume.py
- retrieve_style
- Routes
- TraceSink
- test_graph.py
- Routing
- OpenAICompatibleProvider
- runner.py
- NotifyUser
- run_canonical.py
- EffectLog
- drafting_for
- AnswerQueue
- SimError
- set_session
- gateway.py
- ask_curve
- test_events.py
- plan_deviation
- validate_cases
- test_freeze.py
- Manifest
- .interrupts
- .predraft
- test_lanes_split_the_dataset_without_overlap
- test_floor_protection.py
- trace.py
- test_unknown_case_id_is_a_lookup_error
- ProposalGateway
- view
- test_development_lane_has_nothing_to_learn_from
- test_lane_view_is_bound_to_its_lane
- test_loop.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- router.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- run_simulation
- SimulatedMailbox
- safety/__init__.py
- Block
- evaluate
- autonomy/state.py
- _background_loop
- interrupting_case_ids
- ActionClass
- cli.py
- Disposition
- test_a_strangers_instructions_fence_every_route_whatever_the_action
- Validation

## God Nodes (most connected - your core abstractions)
1. `Route` - 188 edges
2. `Lane` - 71 edges
3. `Router` - 67 edges
4. `Learner` - 60 edges
5. `Manifest` - 57 edges
6. `ChatRunner` - 53 edges
7. `Case` - 50 edges
8. `Message` - 50 edges
9. `ClaimStore` - 50 edges
10. `ProposalGateway` - 49 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `main()` --uses--> `Lane`  [INFERRED]
  evals/economics.py → src/agent/dataset.py
- `main()` --uses--> `ProposalError`  [INFERRED]
  evals/economics.py → src/agent/gateway.py
- `main()` --uses--> `ScoringError`  [INFERRED]
  src/agent/cli.py → evals/harness.py

## Import Cycles
- None detected.

## Communities (113 total, 15 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.12
Nodes (17): Command, GraphError, GraphOutcome, GraphSession, Any, RuntimeError, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the… (+9 more)

### Community 1 - "policy.py"
Cohesion: 0.11
Nodes (27): mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., email_context_for(), floor_verdict_for(), GoldPolicy (+19 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (43): CompiledStateGraph, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _authorized_settled(), _bound(), build_graph() (+35 more)

### Community 3 - ".prepare"
Cohesion: 0.14
Nodes (15): _brief(), _digest(), _notify_text(), _params_brief(), Any, Work out the steps for a decision, validating every one, mutating nothing., A step that validated, or a recorded complaint about why it could not., Every step carries the ids, so one receipt can name the case it came from. (+7 more)

### Community 4 - "ClaimStore"
Cohesion: 0.07
Nodes (45): _open_store(), The run's memory: the rules already kept, and the file they live in., ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., How many claims are in memory. (+37 more)

### Community 5 - "Ledger"
Cohesion: 0.09
Nodes (30): Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price. (+22 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (43): _action_for(), _claim_reading(), _clean_label(), confirm_words(), _decision_reading(), FeedbackContext, _from_context(), _narrowed() (+35 more)

### Community 7 - "dataset.py"
Cohesion: 0.06
Nodes (48): _attachment(), _case_from_mail_row(), _case_from_row(), CaseLabels, event_from_row(), ManifestError, _message(), Any (+40 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.13
Nodes (30): confirm_claim(), Read the user's answer to the scope echo: the claim to store, or None for no., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to… (+22 more)

### Community 10 - "floor_check"
Cohesion: 0.09
Nodes (24): floor_check(), Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-002: Credential or authentication modification must escalate., A single external recipient is an external send, not a mass send., A reversible action leaves the full arm set for the learned policy., An external send cannot be silent or notified: ask or escalate only., A deferred external send is fenced exactly like an immediate one. (+16 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.15
Nodes (22): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize, One claim as the parser hands it over: a class of mail, and the words that said… (+14 more)

### Community 12 - "ChatRunner"
Cohesion: 0.16
Nodes (14): Decision, What the simulator does with one arrival., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.…, Ask the one bounded question and store the rule only if it is confirmed. (+6 more)

### Community 13 - "ActionPayload"
Cohesion: 0.11
Nodes (26): ActionPayload, EmailContext, _eval_injection_tripwires(), _eval_irreversible_external(), _eval_permanent_deletion(), _eval_unknown_tool(), Standardized representation of a candidate tool action., Email metadata and body context passed into safety evaluations.… (+18 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 16 - "test_graph_state.py"
Cohesion: 0.22
Nodes (13): message(), Path, The body and subject are inputs to the decision, and must not reach the file., No line may contain these words, in a key or in a value., Error handling at the boundary: a path that is not a file names itself., The run that dies is the one worth tracing, so lines are flushed as written., test_a_long_text_is_a_digest_and_a_short_one_is_not(), test_a_secret_shaped_field_is_never_written() (+5 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.08
Nodes (21): CalibrationReport, EvalReport, Gate, HeldOutReport, Any, Path, _rate(), A count and its denominator, which is the only honest way to print a rate. (+13 more)

### Community 18 - "test_floor.py"
Cohesion: 0.07
Nodes (32): _check_zero_width_chars(), Detect presence of invisible zero-width characters used for steganography., Scan untrusted email content and headers for prompt injection indicators.…, scan(), Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-005: Mass sends (>5 recipients) must require human approval (ASK)., Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing. (+24 more)

### Community 19 - "injection.py"
Cohesion: 0.20
Nodes (11): base64, re, _check_authority_claims(), _check_base64_injection(), _decode_base64_candidate(), _names_its_own_domain(), Prompt injection tripwires and plan-deviation verification. Zero LLM dependence…, Return the decoded text of a base64 candidate, or None when it is not valid… (+3 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.06
Nodes (51): parse_proposal(), The offline provider: proposes from triage, no network, deterministic. It is a…, Validate one provider answer. Anything unexpected is an error, not a default., RuleProvider, A table that hid the rules provider would show a run spending nothing and doing…, test_the_offline_provider_is_counted_and_costs_nothing(), BrokenProvider, message() (+43 more)

### Community 21 - "Tool"
Cohesion: 0.20
Nodes (7): ABC, ArchiveEmail, Files a message out of the inbox., One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit., Tool

### Community 22 - "test_sim.py"
Cohesion: 0.15
Nodes (23): build_reply_tree(), _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…, Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message() (+15 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "Effect"
Cohesion: 0.16
Nodes (13): CreateDraft, _email_id(), LabelEmail, Any, Writes a private draft. Reversible, and never a send., A send that validates like a real one and never leaves the mailbox. Recipients…, Applies one label to one message., SendEmail (+5 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.13
Nodes (32): DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the… (+24 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (10): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+2 more)

### Community 27 - "ProposalError"
Cohesion: 0.14
Nodes (17): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions (+9 more)

### Community 28 - "state"
Cohesion: 0.11
Nodes (26): One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields(), message_digest(), _plain(), prepared_fields(), Any, The router's decision, as traceable fields: bounded, scalar, and re-readable. (+18 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "VetoLevel"
Cohesion: 0.20
Nodes (10): _mask_routes(), Veto severity level returned by floor_check. When veto is True, router directly…, Drop every route the floor forbade, so the learner never sees them as options., VetoLevel, FLR-003: Unrecognized tool calls must be escalated., FLR-004: Irreversible external sends must require human approval (ASK)., FLR-006: Permanent deletion of mailbox items cannot occur autonomously., test_flr_003_unrecognized_tool() (+2 more)

### Community 31 - "drafts.py"
Cohesion: 0.10
Nodes (25): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Picked, Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, One example that fits the budget, and why it was the one kept. (+17 more)

### Community 32 - "ReplyTree"
Cohesion: 0.14
Nodes (15): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _body_lines(), _prior_lines(), Reconstruct one case's thread, bounded by the reply-tree caps., The arriving mail the way an inbox shows it. Sender, recipients, subject, body… (+7 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.12
Nodes (24): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back. (+16 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.07
Nodes (50): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+42 more)

### Community 36 - "test_replay.py"
Cohesion: 0.04
Nodes (59): hashlib, json, pytest, EventStream, _json_default(), Any, datetime, Seeded clock and append-only event stream (Phase 3.2). Replay has to be… (+51 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.10
Nodes (27): PII masking and anonymization package., forget_thread(), get_token_map(), mask_for_llm(), Access or initialize the singleton PresidioMasker., Sanitize subject and body before any model call. Returns masked text only., Retrieve the current token to original value map for a thread., Drop a thread's token registry and reverse map. (+19 more)

### Community 39 - "masker.py"
Cohesion: 0.07
Nodes (28): AnalyzerEngine, EntityRecognizer, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, RecognizerResult, _build_custom_recognizers(), _clean_person_name() (+20 more)

### Community 40 - "Session"
Cohesion: 0.13
Nodes (20): importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one… (+12 more)

### Community 41 - "run_typed"
Cohesion: 0.11
Nodes (30): arrivals(), block_of(), dataset_routes(), labelled_routes(), DecisionSource, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints. (+22 more)

### Community 42 - "email_tools.py"
Cohesion: 0.22
Nodes (7): action_vocabulary(), Draft, The simulated email tools (Phase 3.3). Six tools over one in-memory mailbox:…, What a proposer may ask for, and what each action needs, as prompt lines., A private draft. Preparation, not sending., Read-only: returns the message it was pointed at., ReadEmail

### Community 43 - "claims.py"
Cohesion: 0.13
Nodes (19): _action_words(), _bears_on(), Claim, _claim_from_record(), claim_id_for(), _claim_record(), Any, datetime (+11 more)

### Community 44 - "schedule"
Cohesion: 0.12
Nodes (27): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them. (+19 more)

### Community 45 - "main"
Cohesion: 0.15
Nodes (17): data_validate(), main(), Print what a case set holds and everything wrong with it., Entry point for the ``wajo`` console script., The plan's exit gate: `wajo data validate <path>` prints and returns a status., test_the_command_exits_zero_on_the_case_set_and_nonzero_on_a_broken_one(), CaptureFixture, MonkeyPatch (+9 more)

### Community 46 - "LaneView"
Cohesion: 0.08
Nodes (16): LaneView, RuntimeError, Raised when code reaches across the learning/held-out firewall., Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner. (+8 more)

### Community 47 - "test_triage.py"
Cohesion: 0.14
Nodes (17): guesses(), manifest(), message(), fixture, Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+9 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.23
Nodes (15): approval_for(), The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, The yes a reviewer would send back for the work they were shown., session(), test_a_crash_before_the_work_ran_leaves_the_decision_waiting(), test_a_decision_that_moved_between_asking_and_answering_is_refused() (+7 more)

### Community 49 - "retrieve_style"
Cohesion: 0.18
Nodes (19): estimate_tokens(), A rough token count for a budget decision, not for a bill., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from., One sent reply, from the mailbox's own history., A reply the user sent this person beats an older one to anybody else. (+11 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "TraceSink"
Cohesion: 0.25
Nodes (6): Append-only JSONL trace, one line per decision, flushed as it is written., Close the file. Safe to call twice, which an except-block may do., TraceSink, Path, On a real run: one line per arrival, and no mail text in any of them., test_a_traced_run_writes_the_decision_and_never_the_mail()

### Community 52 - "test_graph.py"
Cohesion: 0.18
Nodes (19): langgraph_checkpoint_memory, Walk a lane through the graph, one decision per checkpoint thread., run_graph(), CaptureFixture, MonkeyPatch, Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime() (+11 more)

### Community 53 - "Routing"
Cohesion: 0.25
Nodes (5): What the router considered, which every canonical run keeps., The route chosen, and everything that was ruled out on the way., The chosen route's expected loss, in handoffs., One line for a transcript or a reason. Deliberately terse: a trace digests a…, Routing

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (13): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+5 more)

### Community 55 - "runner.py"
Cohesion: 0.07
Nodes (44): collections_abc, dataclasses, enum, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, Safety Floor — Pure-function deterministic guardrails. FLOOR_VERSION = "1.0"…, Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, _address(), Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).… (+36 more)

### Community 56 - "NotifyUser"
Cohesion: 0.29
Nodes (4): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else.

### Community 57 - "run_canonical.py"
Cohesion: 0.12
Nodes (22): cold_control(), main(), one_case_view(), preference_for(), The four reference cases, run end to end and printed as transcripts. Each case…, The scoped preference a confirmed rule would leave behind for this sender.…, What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input… (+14 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "drafting_for"
Cohesion: 0.17
Nodes (12): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+4 more)

### Community 61 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

### Community 63 - "gateway.py"
Cohesion: 0.06
Nodes (53): os, _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one., What the user's own words amount to for this mail, if anything., The claim's route, with whatever work the inner provider chose for the mail. An…, _with_inner_action() (+45 more)

### Community 64 - "ask_curve"
Cohesion: 0.25
Nodes (6): ask_curve(), Block, The interruption curve: how many cases each block of the lane needed the user…, One block of a lane, in delivery order, and how much of it asked for the user., Blocks are the stream's own order, and four cases at block 12 is one block of…, test_the_curve_blocks_the_lane_in_delivery_order_and_the_last_block_may_be_short()

### Community 65 - "test_events.py"
Cohesion: 0.08
Nodes (36): DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., Raised when a stream is not in ascending sequence order. (+28 more)

### Community 66 - "plan_deviation"
Cohesion: 0.18
Nodes (11): _eval_plan_deviation(), FLR-INJ-002: Actions deviating from pre-committed plan must be escalated., plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips. (+3 more)

### Community 67 - "validate_cases"
Cohesion: 0.06
Nodes (56): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+48 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.23
Nodes (11): Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named(), test_a_frozen_run_rebuilds_its_posteriors_cutoffs_and_refusals() (+3 more)

### Community 69 - "Manifest"
Cohesion: 0.07
Nodes (44): main(), Run the lanes, then print what they cost., main(), Run both lanes and print the report, so the scorer can be read before it is…, Namespace, The pair's name, so a run says where a proposal could have come from., eval_all(), graph_run() (+36 more)

### Community 73 - "test_floor_protection.py"
Cohesion: 0.12
Nodes (33): approve(), ask_again(), bucket_for(), case(), feedback(), one_case_view(), The floor's second hard requirement, as an executable proof. No posterior, no…, Count `count` approved-then-undone decisions, each worth three rejections. (+25 more)

### Community 74 - "trace.py"
Cohesion: 0.16
Nodes (20): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+12 more)

### Community 76 - "ProposalGateway"
Cohesion: 0.08
Nodes (22): Protocol, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, _proposing(), The pipeline's proposer: a rule already confirmed answers before the provider…, ProposalGateway (+14 more)

### Community 77 - "view"
Cohesion: 0.20
Nodes (11): ExplodingPolicy, The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case., Fixture case ids in the order the windows deliver them., scheduled_case_ids(), test_a_failing_policy_names_the_case_it_stopped_on(), test_an_arrival_shows_the_mail_a_production_inbox_shows(), test_arrivals_come_in_the_windowed_order_the_seed_recorded() (+3 more)

### Community 80 - "test_loop.py"
Cohesion: 0.09
Nodes (27): ArgumentParser, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over… (+19 more)

### Community 83 - "Lane"
Cohesion: 0.08
Nodes (59): calibration_report(), dispositions(), held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both… (+51 more)

### Community 88 - "router.py"
Cohesion: 0.17
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "Route"
Cohesion: 0.11
Nodes (37): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+29 more)

### Community 108 - "run_simulation"
Cohesion: 0.11
Nodes (20): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, close_input(), Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did. (+12 more)

### Community 112 - "SimulatedMailbox"
Cohesion: 0.15
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 116 - "safety/__init__.py"
Cohesion: 0.14
Nodes (13): FloorRule, Representation of an audited, immutable safety floor rule., Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, Safety module: floor guardrails, action taxonomy, and injection tripwires., InjectionScanResult, Outcome of scanning text and metadata for prompt injection signals., The least autonomous route the floor left open, which is the fail-closed one. (+5 more)

### Community 117 - "Block"
Cohesion: 0.20
Nodes (7): Block, classify(), Any, Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 118 - "evaluate"
Cohesion: 0.10
Nodes (31): RuntimeError, Refuse a record whose counts cannot add up to what the run processed., Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, evaluate(), _frozen(), load_script(), Any (+23 more)

### Community 119 - "autonomy/state.py"
Cohesion: 0.10
Nodes (23): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+15 more)

### Community 120 - "_background_loop"
Cohesion: 0.29
Nodes (5): AbstractEventLoop, _background_loop(), Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 122 - "interrupting_case_ids"
Cohesion: 0.18
Nodes (13): first_interrupt_of(), gold_route(), interrupting_case_ids(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., Fixture cases whose gold route asks the user, in delivery order. (+5 more)

### Community 124 - "ActionClass"
Cohesion: 0.11
Nodes (24): ActionClass, classify_action(), _eval_credential_security(), _eval_mass_send(), _eval_money_movement(), _extract_recipients(), _has_credential_intent(), _has_financial_intent() (+16 more)

### Community 125 - "cli.py"
Cohesion: 0.12
Nodes (23): argparse, asyncio, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The two-lane scorer: what the agent did, counted where it happened. The report…, Read a graph run, including the floor's ballot and who authorised each commit., record_from_graph(), main() (+15 more)

### Community 130 - "Disposition"
Cohesion: 0.29
Nodes (3): Disposition, How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to.

### Community 135 - "test_a_strangers_instructions_fence_every_route_whatever_the_action"
Cohesion: 0.22
Nodes (9): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., The mail fences, not the proposed action: a harmless label still collapses to…, test_a_strangers_instructions_fence_every_route_whatever_the_action(), test_benign_workplace_clean_pass(), test_classify_action_matrix() (+1 more)

## Knowledge Gaps
- **14 isolated node(s):** `ROUTES`, `CHOICES`, `email-autonomy-agent`, `graphify`, `Steps` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `policy.py`, `.prepare`, `Ledger`, `feedback.py`, `dataset.py`, `test_a_strangers_instructions_fence_every_route_whatever_the_action`, `ScopeAnchor`, `floor_check`, `test_claim_schema.py`, `ChatRunner`, `ActionPayload`, `test_floor.py`, `test_gateway.py`, `test_sim.py`, `test_sim_tools.py`, `state`, `VetoLevel`, `test_predrafts.py`, `Learner`, `Session`, `run_typed`, `claims.py`, `Routing`, `runner.py`, `run_canonical.py`, `gateway.py`, `test_freeze.py`, `Manifest`, `test_floor_protection.py`, `ProposalGateway`, `Lane`, `router.py`, `safety/__init__.py`, `interrupting_case_ids`, `ActionClass`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Lane` connect `Lane` to `policy.py`, `ClaimStore`, `dataset.py`, `HeldOutReport`, `test_draft_validation.py`, `test_predrafts.py`, `Learner`, `test_replay.py`, `Session`, `LaneView`, `test_graph_resume.py`, `test_graph.py`, `run_canonical.py`, `Manifest`, `test_lanes_split_the_dataset_without_overlap`, `test_floor_protection.py`, `test_unknown_case_id_is_a_lookup_error`, `ProposalGateway`, `view`, `test_development_lane_has_nothing_to_learn_from`, `test_lane_view_is_bound_to_its_lane`, `test_loop.py`, `Route`, `evaluate`, `cli.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `ProposalGateway` connect `ProposalGateway` to `GraphSession`, `policy.py`, `graph.py`, `Route`, `Ledger`, `Session`, `HeldOutReport`, `Lane`, `test_graph.py`, `test_gateway.py`, `evaluate`, `run_canonical.py`, `ProposalError`, `cli.py`, `gateway.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 155 inferred relationships involving `Route` (e.g. with `dispositions()` and `held_out_report()`) actually correct?**
  _`Route` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 58 inferred relationships involving `Lane` (e.g. with `main()` and `CalibrationReport`) actually correct?**
  _`Lane` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 30 INFERRED edges - model-reasoned connections that need verification._