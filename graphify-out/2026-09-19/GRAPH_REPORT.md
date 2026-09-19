# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 95 files · ~89,296 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2501 nodes · 6484 edges · 119 communities (111 shown, 8 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 994 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `217c814b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- Case
- graph.py
- registry.py
- consent.py
- ProposalGateway
- feedback.py
- dataset.py
- Bucket
- ScopeAnchor
- ActionPayload
- test_claim_schema.py
- ChatRunner
- EmailContext
- Handler
- sandbox.py
- test_sandbox.py
- CalibrationReport
- test_floor.py
- injection.py
- test_gateway.py
- gateway.py
- test_sim.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- .render
- ProposalError
- runner.py
- app.js
- VetoLevel
- drafts.py
- ReplyTree
- test_predrafts.py
- Posterior
- Learner
- SeededClock
- events.py
- mask_for_llm
- PresidioMasker
- test_ui_session.py
- run_typed
- ClaimStore
- floor.py
- schedule
- main
- LaneView
- test_triage.py
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- test_graph.py
- preferences.py
- OpenAICompatibleProvider
- SimulatedMailbox
- ManifestError
- policy.py
- EffectLog
- drafting_for
- schedule.py
- SimError
- ModelUser
- Message
- Block
- test_events.py
- plan_deviation
- test_cases.py
- test_freeze.py
- graph_run
- ContextPhoneRecognizer
- masker.py
- test_replay.py
- test_floor_protection.py
- trace.py
- Judge
- RememberedProvider
- view
- run_graph
- SplitViolation
- test_loop.py
- EmailEvent
- Workflow: graphify
- Lane
- email-autonomy-agent
- test_a_usage_object_that_arrives_as_a_mapping_reads_the_same
- router.py
- Route
- rules/graphify.md
- DESIGN.md
- README.md
- stranger_mail
- GraphError
- LoopReport
- get_token_map
- ClaimType
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- run_simulation
- _bucket_of
- DecisionSource
- session.py
- evaluate
- autonomy/state.py
- interrupting_case_ids
- safety/__init__.py
- cli.py
- EvalReport
- test_a_strangers_instructions_fence_every_route_whatever_the_action

## God Nodes (most connected - your core abstractions)
1. `Route` - 178 edges
2. `Router` - 62 edges
3. `Learner` - 60 edges
4. `Lane` - 59 edges
5. `ChatRunner` - 52 edges
6. `Manifest` - 51 edges
7. `ProposalGateway` - 48 edges
8. `Case` - 47 edges
9. `ActionPayload` - 45 edges
10. `ClaimStore` - 44 edges

## Surprising Connections (you probably didn't know these)
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `main()` --uses--> `ScoringError`  [INFERRED]
  src/agent/cli.py → evals/harness.py
- `test_a_record_that_decided_fewer_cases_than_it_processed_is_refused()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py
- `test_a_report_cannot_be_written_where_it_cannot_be_read()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py

## Import Cycles
- None detected.

## Communities (119 total, 8 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.16
Nodes (13): Command, Answer one held decision with a yes and say what that committed., _resume_note(), GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human. (+5 more)

### Community 1 - "Case"
Cohesion: 0.11
Nodes (20): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., Every case in one lane, in sequence order. (+12 more)

### Community 2 - "graph.py"
Cohesion: 0.11
Nodes (38): CompiledStateGraph, GraphState, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _bound() (+30 more)

### Community 3 - "registry.py"
Cohesion: 0.08
Nodes (29): ABC, _brief(), _digest(), _notify_text(), _params_brief(), Any, datetime, The tool registry and the prepare/authorize/commit contract (Phase 3.3). Every… (+21 more)

### Community 4 - "consent.py"
Cohesion: 0.13
Nodes (23): Capability, ConsentRequired, LearningConsent, datetime, RuntimeError, StrEnum, What the agent is able to do. Holding one says nothing about being allowed to., How long what was learned may be kept. (+15 more)

### Community 5 - "ProposalGateway"
Cohesion: 0.10
Nodes (27): pytest, ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., provider() (+19 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (40): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+32 more)

### Community 7 - "dataset.py"
Cohesion: 0.13
Nodes (28): _attachment(), _case_from_mail_row(), _case_from_row(), DatasetProblem, event_from_row(), _message(), Any, datetime (+20 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): Random, The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.12
Nodes (30): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a… (+22 more)

### Community 10 - "ActionPayload"
Cohesion: 0.10
Nodes (30): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated., FLR-005: Mass sends (>5 recipients) must require human approval (ASK). (+22 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.14
Nodes (22): ClaimError, ValueError, Write every claim to the store's file, one JSON object per line. The whole…, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize (+14 more)

### Community 12 - "ChatRunner"
Cohesion: 0.16
Nodes (11): ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.…, Ask the one bounded question and store the rule only if it is confirmed., Commit the work the user just approved, bound to the prepared digest., What the reply parser may look at: the mail and the decision, never a label., Consume lines typed while the previous decision was live. The settle first,… (+3 more)

### Community 13 - "EmailContext"
Cohesion: 0.17
Nodes (12): EmailContext, Email metadata and body context passed into safety evaluations.…, FLR-001: Money requests in email body cannot trigger non-reversible actions., Load tests/adversarial_cases.yaml and verify 100% are vetoed with ESCALATE., An injection tripwire collapses the arm set to ESCALATE before learning runs., floor_check must read the domain carried by the email, not a fixed default., An honest vendor signing as its own security team must not be vetoed., test_a_vendor_naming_its_own_domain_is_not_an_authority_spoof() (+4 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (11): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., Point the server at a session, which is what the tests and the page both need., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent. (+3 more)

### Community 15 - "sandbox.py"
Cohesion: 0.06
Nodes (52): Count a run's floor violations and unauthorized commits. The floor's ballot is…, safety_counts(), Arrival, as_dict(), charts(), generator_prompt(), main(), _markdown() (+44 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.09
Nodes (35): dispositions(), Count routes into the three dispositions, refusing a route nobody defined., _by_id(), parse_generated(), RuntimeError, Raised when the environment cannot be built or read., Read one generated mail, naming what is wrong rather than guessing a field., The arrivals one record decided, in the order it decided them. (+27 more)

### Community 17 - "CalibrationReport"
Cohesion: 0.09
Nodes (15): CalibrationReport, Gate, HeldOutReport, Any, _rate(), A count and its denominator, which is the only honest way to print a rate., The lane the user sat in front of: what they typed, and what it cost them., Lines the user typed: answers to a prompt, and corrections after one. (+7 more)

### Community 18 - "test_floor.py"
Cohesion: 0.09
Nodes (26): Scan untrusted email content and headers for prompt injection indicators.…, scan(), Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles. (+18 more)

### Community 19 - "injection.py"
Cohesion: 0.15
Nodes (14): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, _names_its_own_domain(), Prompt injection tripwires and plan-deviation verification. Zero LLM dependence… (+6 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.08
Nodes (43): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., message(), parametrize, quiet_but_wrong(), The model proposal gateway: untrusted output, one repair, then fail closed., The noun decides: 'the Redis sharding key' is a field, and escalating it is…, The ask shape decides too: 'consider changing your password' is advice. (+35 more)

### Community 21 - "gateway.py"
Cohesion: 0.11
Nodes (26): os, _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule() (+18 more)

### Community 22 - "test_sim.py"
Cohesion: 0.19
Nodes (19): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., Sender, subject and body are inputs in production; labels are only answers.… (+11 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.09
Nodes (26): action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser (+18 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.12
Nodes (33): DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the… (+25 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (10): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+2 more)

### Community 27 - "ProposalError"
Cohesion: 0.14
Nodes (17): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions (+9 more)

### Community 28 - "runner.py"
Cohesion: 0.09
Nodes (37): The chosen route's expected loss, in handoffs., Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).…, One line per decision, and one per reply: ids, hashes, bounded records., Read stdin without blocking the event loop., _stdin_lines(), draft_fields(), GraphState, hint_fields() (+29 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "VetoLevel"
Cohesion: 0.11
Nodes (25): ActionClass, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_permanent_deletion(), _eval_plan_deviation(), _eval_unknown_tool() (+17 more)

### Community 31 - "drafts.py"
Cohesion: 0.09
Nodes (25): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap. (+17 more)

### Community 32 - "ReplyTree"
Cohesion: 0.12
Nodes (17): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _address(), _body_lines(), _prior_lines(), Reconstruct one case's thread, bounded by the reply-tree caps. (+9 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (22): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+14 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.08
Nodes (44): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+36 more)

### Community 36 - "SeededClock"
Cohesion: 0.08
Nodes (26): EventStream, _json_default(), Any, datetime, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time. (+18 more)

### Community 37 - "events.py"
Cohesion: 0.11
Nodes (20): enum, Attachment, DuplicateEventError, EventValidationError, ValueError, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema. (+12 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "test_ui_session.py"
Cohesion: 0.10
Nodes (24): importlib_util, _call(), Any, Path, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET. (+16 more)

### Community 41 - "run_typed"
Cohesion: 0.11
Nodes (29): arrivals(), block_of(), dataset_routes(), labelled_routes(), DecisionSource, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints. (+21 more)

### Community 42 - "ClaimStore"
Cohesion: 0.11
Nodes (20): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Grant, A capability and the consent that travels with it, separate objects on purpose.… (+12 more)

### Community 43 - "floor.py"
Cohesion: 0.11
Nodes (21): re, _action_words(), _bears_on(), Claim, _claim_from_record(), _claim_record(), Any, datetime (+13 more)

### Community 44 - "schedule"
Cohesion: 0.20
Nodes (18): Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., release_order(), schedule(), fake(), lane(), SimpleNamespace, Phase 3.5: windowed-random arrival scheduling. (+10 more)

### Community 45 - "main"
Cohesion: 0.19
Nodes (14): main(), Entry point for the ``wajo`` console script., test_the_cli_keeps_the_held_out_lane_shut(), CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., test_a_broken_input_stream_ends_the_run_instead_of_hanging() (+6 more)

### Community 46 - "LaneView"
Cohesion: 0.13
Nodes (7): LaneView, Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach.

### Community 47 - "test_triage.py"
Cohesion: 0.18
Nodes (13): message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker(), test_an_ambiguous_message_asks_for_a_model(), test_an_unverified_authority_claim_is_spoofing() (+5 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.12
Nodes (23): approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The plan's crash matrix: whether the work ran or not, a resume applies it once. (+15 more)

### Community 49 - "retrieve_style"
Cohesion: 0.16
Nodes (21): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from. (+13 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.16
Nodes (19): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Manifest, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows., Counts per split and per lane, for the validator's output., view(), view() (+11 more)

### Community 52 - "test_graph.py"
Cohesion: 0.21
Nodes (15): CaptureFixture, MonkeyPatch, Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+7 more)

### Community 53 - "preferences.py"
Cohesion: 0.16
Nodes (14): _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one., What the user's own words amount to for this mail, if anything., The claim's route, with whatever work the inner provider chose for the mail. An…, _with_inner_action(), Proposal (+6 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (14): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+6 more)

### Community 55 - "SimulatedMailbox"
Cohesion: 0.11
Nodes (19): build_registry(), Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization (+11 more)

### Community 56 - "ManifestError"
Cohesion: 0.15
Nodes (15): CaseLabels, ManifestError, ValueError, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only., Build a manifest from parsed rows, rejecting duplicate case ids and splits., Raised when the dataset itself violates the manifest schema., A bare KeyError says nothing about which of the cases is malformed. (+7 more)

### Community 57 - "policy.py"
Cohesion: 0.12
Nodes (20): dataclasses, main(), The four reference cases, run end to end and printed as transcripts. Each case…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it… (+12 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "drafting_for"
Cohesion: 0.15
Nodes (14): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+6 more)

### Community 60 - "schedule.py"
Cohesion: 0.15
Nodes (14): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, _dependencies_first(), dependencies_of(), Any, RuntimeError, Windowed-random arrival scheduling (plan Commit 3.5). A lane replayed in…, Raised when a case names a dependency no window can deliver before it., One released window: its cases in delivery order, and the seed that ordered it. (+6 more)

### Community 61 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

### Community 62 - "ModelUser"
Cohesion: 0.22
Nodes (10): Decision, ModelUser, Message, The person whose mailbox this is, played by a model that is not the proposer.…, What the reply parser may look at: the mail and the decision, never a label., The lines to hand the waiting decision: the reply, and a confirmation if…, Whether the draft on the table may be saved. Nothing is approved by default., The runner's interrupt hook: the waiting decision gets its lines from the model. (+2 more)

### Community 63 - "Message"
Cohesion: 0.09
Nodes (27): Message, One email message, in a thread, in one direction., The offline provider: proposes from triage, no network, deterministic. It is a…, RuleProvider, _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root… (+19 more)

### Community 65 - "test_events.py"
Cohesion: 0.09
Nodes (37): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _feedback(), _load_dataset(), parametrize (+29 more)

### Community 66 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 67 - "test_cases.py"
Cohesion: 0.07
Nodes (55): data_validate(), Print what a case set holds and everything wrong with it., CaseReport, Path, What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Check a case set's counts, enums and splits before anything is asked to run it.…, validate_cases() (+47 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.23
Nodes (11): Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named(), test_a_frozen_run_rebuilds_its_posteriors_cutoffs_and_refusals() (+3 more)

### Community 69 - "graph_run"
Cohesion: 0.14
Nodes (25): ClaimStore, DecisionSource, Namespace, The pair's name, so a run says where a proposal could have come from., eval_all(), graph_run(), _keep_rules(), loop_run() (+17 more)

### Community 70 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "test_replay.py"
Cohesion: 0.06
Nodes (37): hashlib, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, Replay events through a fresh seeded stream., replay(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact. (+29 more)

### Community 73 - "test_floor_protection.py"
Cohesion: 0.15
Nodes (27): floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., approve(), ask_again(), bucket_for(), case(), one_case_view(), The floor's second hard requirement, as an executable proof. No posterior, no… (+19 more)

### Community 74 - "trace.py"
Cohesion: 0.08
Nodes (38): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+30 more)

### Community 75 - "Judge"
Cohesion: 0.18
Nodes (9): Judge, _judge_run(), Judgement, One external opinion, with the reason it gave., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI., Ask one question about one case. A judge that fails says so and scores nothing. (+1 more)

### Community 76 - "RememberedProvider"
Cohesion: 0.12
Nodes (17): Protocol, The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, _proposing(), The pipeline's proposer: a rule already confirmed answers before the provider…, ProposalProvider (+9 more)

### Community 77 - "view"
Cohesion: 0.15
Nodes (14): ExplodingPolicy, Path, The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case., Fixture case ids in the order the windows deliver them., On a real run: one line per arrival, and no mail text in any of them., scheduled_case_ids(), test_a_failing_policy_names_the_case_it_stopped_on() (+6 more)

### Community 78 - "run_graph"
Cohesion: 0.24
Nodes (10): Router, SimulatedMailbox, GraphOutcome, LaneView, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., What a lane through the graph did., How many times a tool actually ran, counted from the receipts. (+2 more)

### Community 79 - "SplitViolation"
Cohesion: 0.18
Nodes (9): RuntimeError, Raised when code reaches across the learning/held-out firewall., SplitViolation, The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read., The separation is symmetric: a lane view only sees its own rows., Held-out and development code cannot update the learner., test_a_held_out_view_cannot_open_a_calibration_case(), test_a_learning_read_of_a_held_out_case_is_a_split_violation() (+1 more)

### Community 80 - "test_loop.py"
Cohesion: 0.09
Nodes (27): ArgumentParser, build_parser(), The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags(), InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over… (+19 more)

### Community 81 - "EmailEvent"
Cohesion: 0.20
Nodes (7): EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The manifest hands out EmailEvents, not raw rows., test_events_are_canonical_events()

### Community 83 - "Lane"
Cohesion: 0.08
Nodes (62): ask_curve(), calibration_report(), held_out_report(), LaneRecord, The interruption curve: how many cases each block of the lane needed the user…, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Score the calibration lane: the dispositions, the typings and the ask curve. (+54 more)

### Community 87 - "test_a_usage_object_that_arrives_as_a_mapping_reads_the_same"
Cohesion: 0.27
Nodes (8): MeteredCompletions, SimpleNamespace, A proxy that hands back plain JSON must price the same as the SDK's own object., A model endpoint that reports usage, so the meter has something to read., A response with no usage at all, which is what a proxy sometimes returns., silent_completions(), test_a_response_without_usage_is_a_call_that_reported_no_tokens(), test_a_usage_object_that_arrives_as_a_mapping_reads_the_same()

### Community 88 - "router.py"
Cohesion: 0.14
Nodes (24): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+16 more)

### Community 98 - "Route"
Cohesion: 0.10
Nodes (39): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+31 more)

### Community 102 - "stranger_mail"
Cohesion: 0.20
Nodes (10): A mail whose sender the mailbox cannot vouch for., Mailbox housekeeping commissioned by a stranger is the same shape, subject…, Please reply with the numbers' from a colleague is a request, and is left alone., A spoofed invoice is refused on the mail, however reversible the proposed…, A credential harvest is refused on the mail, not on whatever action was…, stranger_mail(), test_a_credential_named_by_a_stranger_fences_a_harmless_action(), test_a_strangers_system_housekeeping_fences_too() (+2 more)

### Community 103 - "GraphError"
Cohesion: 0.25
Nodes (9): Authorization, PreparedAction, _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still… (+1 more)

### Community 104 - "LoopReport"
Cohesion: 0.25
Nodes (5): LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 105 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 106 - "ClaimType"
Cohesion: 0.40
Nodes (5): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence.

### Community 107 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 108 - "run_simulation"
Cohesion: 0.17
Nodes (13): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did., Feedback a learner would accept, which is nothing until Commit 3.6. (+5 more)

### Community 117 - "session.py"
Cohesion: 0.09
Nodes (22): AbstractEventLoop, ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, router, route out., AnswerQueue, _background_loop(), Block, classify(), Path (+14 more)

### Community 118 - "evaluate"
Cohesion: 0.09
Nodes (33): main(), Run the lanes, then print what they cost., RuntimeError, Refuse a record whose counts cannot add up to what the run processed., Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, evaluate(), _frozen() (+25 more)

### Community 119 - "autonomy/state.py"
Cohesion: 0.10
Nodes (23): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+15 more)

### Community 122 - "interrupting_case_ids"
Cohesion: 0.20
Nodes (12): first_interrupt_of(), interrupting_case_ids(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., Fixture cases whose gold route asks the user, in delivery order., test_a_correction_typed_at_a_prompt_binds_to_that_decision() (+4 more)

### Community 124 - "safety/__init__.py"
Cohesion: 0.09
Nodes (24): classify_action(), _eval_money_movement(), _extract_recipients(), FloorRule, _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any (+16 more)

### Community 125 - "cli.py"
Cohesion: 0.11
Nodes (27): argparse, asyncio, collections_abc, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The two-lane scorer: what the agent did, counted where it happened. The report…, Read a graph run, including the floor's ballot and who authorised each commit., Join the two lanes into the report, refusing a pair that cannot be one run. (+19 more)

### Community 130 - "EvalReport"
Cohesion: 0.11
Nodes (12): Disposition, EvalReport, main(), LaneView, Path, Both lanes, kept apart: one disposition count over everything, two assessments., How a lane's cases were handled, mutually exclusive by construction., Write the report as JSON, naming the file in the error rather than failing mute. (+4 more)

### Community 135 - "test_a_strangers_instructions_fence_every_route_whatever_the_action"
Cohesion: 0.22
Nodes (9): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., The mail fences, not the proposed action: a harmless label still collapses to…, test_a_strangers_instructions_fence_every_route_whatever_the_action(), test_benign_workplace_clean_pass(), test_classify_action_matrix() (+1 more)

## Knowledge Gaps
- **14 isolated node(s):** `email-autonomy-agent`, `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `Case`, `registry.py`, `ProposalGateway`, `feedback.py`, `dataset.py`, `test_a_strangers_instructions_fence_every_route_whatever_the_action`, `ScopeAnchor`, `ActionPayload`, `test_claim_schema.py`, `ChatRunner`, `EmailContext`, `test_sandbox.py`, `test_floor.py`, `test_gateway.py`, `test_sim.py`, `test_sim_tools.py`, `runner.py`, `VetoLevel`, `test_predrafts.py`, `Learner`, `events.py`, `test_ui_session.py`, `run_typed`, `ClaimStore`, `floor.py`, `Manifest`, `preferences.py`, `SimulatedMailbox`, `policy.py`, `Message`, `test_freeze.py`, `test_floor_protection.py`, `RememberedProvider`, `Lane`, `router.py`, `stranger_mail`, `ClaimType`, `interrupting_case_ids`, `safety/__init__.py`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `PresidioMasker` connect `PresidioMasker` to `get_token_map`, `ContextPhoneRecognizer`, `masker.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `Learner` connect `Learner` to `Route`, `test_freeze.py`, `graph_run`, `feedback.py`, `Bucket`, `LoopReport`, `test_floor_protection.py`, `floor.py`, `RememberedProvider`, `ChatRunner`, `run_simulation`, `sandbox.py`, `session.py`, `evaluate`, `autonomy/state.py`, `router.py`, `policy.py`, `runner.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 147 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 147 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 50 INFERRED edges - model-reasoned connections that need verification._