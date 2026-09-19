# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 95 files · ~90,744 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2530 nodes · 6530 edges · 124 communities (117 shown, 7 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 985 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6d7ad662`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- policy.py
- graph.py
- registry.py
- session_grant
- test_economics.py
- runner.py
- dataset.py
- Bucket
- ScopeAnchor
- test_floor.py
- test_claim_schema.py
- ChatRunner
- FeedbackEvent
- Handler
- write_report
- test_sandbox.py
- CalibrationReport
- scan
- sandbox.py
- test_gateway.py
- Proposal
- build_reply_tree
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- .render
- ProposalError
- agent/state.py
- app.js
- floor.py
- drafts.py
- ReplyTree
- test_predrafts.py
- RoutingRequest
- Learner
- EventStream
- EventValidationError
- mask_for_llm
- PresidioMasker
- test_ui_session.py
- test_sim.py
- ClaimStore
- claims.py
- Case
- RuleProvider
- LaneView
- test_triage.py
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- test_graph.py
- ClaimScope
- OpenAICompatibleProvider
- SimulatedMailbox
- .labels
- run_canonical.py
- EffectLog
- drafting_for
- write_mailbox
- SimError
- .lines_for
- ProposalGateway
- ask_curve
- test_events.py
- plan_deviation
- test_cases.py
- pytest
- main
- ContextPhoneRecognizer
- masker.py
- test_replay.py
- Route
- trace.py
- _judge_run
- RememberedProvider
- Any
- ProposalRequest
- SandboxError
- test_loop.py
- server.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- Block
- router.py
- Router
- rules/graphify.md
- DESIGN.md
- README.md
- CaseReport
- GraphError
- LoopReport
- get_token_map
- ClaimType
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- run_simulation
- _background_loop
- DecisionSource
- IO
- json
- .hook
- test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in
- TraceSink
- Session
- evaluate
- autonomy/state.py
- first_interrupt_of
- strictest_allowed
- cli.py
- EvalReport
- test_benign_workplace_clean_pass

## God Nodes (most connected - your core abstractions)
1. `Route` - 178 edges
2. `Router` - 63 edges
3. `Lane` - 62 edges
4. `Learner` - 60 edges
5. `ChatRunner` - 52 edges
6. `Manifest` - 51 edges
7. `ProposalGateway` - 47 edges
8. `Case` - 47 edges
9. `ActionPayload` - 45 edges
10. `ClaimStore` - 44 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `main()` --uses--> `SandboxError`  [INFERRED]
  src/agent/cli.py → evals/sandbox.py
- `test_a_brief_the_writer_cannot_answer_is_named_not_guessed()` --uses--> `SandboxError`  [INFERRED]
  tests/eval/test_sandbox.py → evals/sandbox.py
- `text_call()` --uses--> `ProposalError`  [INFERRED]
  evals/sandbox.py → src/agent/gateway.py

## Import Cycles
- None detected.

## Communities (124 total, 7 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.18
Nodes (11): Command, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, Carry a thread past its interrupt, or past the point a crash cut it off at. (+3 more)

### Community 1 - "policy.py"
Cohesion: 0.14
Nodes (17): mail_risk(), The route chosen, and everything that was ruled out on the way., One line for a transcript or a reason. Deliberately terse: a trace digests a…, What a mail makes likely, from signals the pipeline already computed. An unsure…, Routing, _params_with_case(), Any, quietenable() (+9 more)

### Community 2 - "graph.py"
Cohesion: 0.11
Nodes (38): CompiledStateGraph, GraphState, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _bound() (+30 more)

### Community 3 - "registry.py"
Cohesion: 0.07
Nodes (42): Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest(), _notify_text() (+34 more)

### Community 4 - "session_grant"
Cohesion: 0.12
Nodes (19): Capability, Grant, LearningConsent, datetime, StrEnum, What the agent is able to do. Holding one says nothing about being allowed to., How long what was learned may be kept., What may be learned, for what purpose, kept how long, and until when. (+11 more)

### Community 5 - "test_economics.py"
Cohesion: 0.09
Nodes (30): Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price. (+22 more)

### Community 6 - "runner.py"
Cohesion: 0.08
Nodes (38): FeedbackKind, is_learnable(), What the user did after seeing a decision. Values are the dataset's…, Return whether this kind of feedback may update the learner., _action_for(), _claim_reading(), _clean_label(), _decision_reading() (+30 more)

### Community 7 - "dataset.py"
Cohesion: 0.08
Nodes (43): _attachment(), _case_from_mail_row(), _case_from_row(), DatasetProblem, event_from_row(), _message(), Any, datetime (+35 more)

### Community 8 - "Bucket"
Cohesion: 0.11
Nodes (24): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "ScopeAnchor"
Cohesion: 0.12
Nodes (30): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to…, everything" is ambiguous, so the narrow reading tied to the active item is a… (+22 more)

### Community 10 - "test_floor.py"
Cohesion: 0.06
Nodes (60): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions., FLR-002: Credential or authentication modification must escalate. (+52 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.17
Nodes (21): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., memory(), preference(), parametrize, One claim as the parser hands it over: a class of mail, and the words that said…, A rule kept in one run is in force in the next one, which is a separate process. (+13 more)

### Community 12 - "ChatRunner"
Cohesion: 0.11
Nodes (21): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., _address(), _body_lines(), _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another. (+13 more)

### Community 13 - "FeedbackEvent"
Cohesion: 0.14
Nodes (12): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, What the user did with a decision, and whether it may teach the learner. (+4 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "write_report"
Cohesion: 0.09
Nodes (26): as_dict(), charts(), main(), _markdown(), Path, _rate(), Keep the mailbox itself, so a report can be read next to the mail that produced…, What the run did, in the order a reader wants it. (+18 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.14
Nodes (27): Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, The whole environment on stand-ins: no key, no network, no judge., Each half decides exactly the arrivals it was given, and nothing goes missing., The model user is what makes the calibration half teach: it has to be asked., Nothing hostile is committed on its own, and the count says so with its…, What is written is mail rows, so the split firewall reads them the same way., A mail with a missing field fails loudly instead of being written as something… (+19 more)

### Community 17 - "CalibrationReport"
Cohesion: 0.09
Nodes (15): CalibrationReport, Gate, HeldOutReport, Any, _rate(), A count and its denominator, which is the only honest way to print a rate., The lane the user sat in front of: what they typed, and what it cost them., Lines the user typed: answers to a prompt, and corrections after one. (+7 more)

### Community 18 - "scan"
Cohesion: 0.10
Nodes (20): _check_zero_width_chars(), InjectionScanResult, Detect presence of invisible zero-width characters used for steganography., Scan untrusted email content and headers for prompt injection indicators.…, Outcome of scanning text and metadata for prompt injection signals., scan(), Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing. (+12 more)

### Community 19 - "sandbox.py"
Cohesion: 0.13
Nodes (23): asyncio, base64, collections_abc, dataclasses, A live mailbox: fresh mail every run, through the real pipeline, judged from…, os, re, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,… (+15 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.10
Nodes (27): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., parametrize, quiet_but_wrong(), The model proposal gateway: untrusted output, one repair, then fail closed., A provider that would happily label suspicious mail and move on., The rules belong to the mail, so a model never gets to propose a quiet route…, The net under the gate: a proposal from some other path still cannot land… (+19 more)

### Community 21 - "Proposal"
Cohesion: 0.13
Nodes (24): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule(), Proposal (+16 more)

### Community 22 - "build_reply_tree"
Cohesion: 0.26
Nodes (13): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, message(), A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected(), test_cycle_is_walked_once(), test_depth_cap_stops_the_walk(), test_duplicate_ids_are_kept_once() (+5 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.13
Nodes (29): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+21 more)

### Community 24 - "email_tools.py"
Cohesion: 0.09
Nodes (31): ABC, action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification (+23 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.12
Nodes (33): DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the… (+25 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (10): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+2 more)

### Community 27 - "ProposalError"
Cohesion: 0.16
Nodes (16): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch (+8 more)

### Community 28 - "agent/state.py"
Cohesion: 0.16
Nodes (19): The chosen route's expected loss, in handoffs., One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields(), message_digest(), _plain(), prepared_fields(), Any (+11 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "floor.py"
Cohesion: 0.08
Nodes (47): ActionClass, classify_action(), EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement() (+39 more)

### Community 31 - "drafts.py"
Cohesion: 0.09
Nodes (25): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap. (+17 more)

### Community 32 - "ReplyTree"
Cohesion: 0.15
Nodes (12): A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree, _prior_lines(), Reconstruct one case's thread, bounded by the reply-tree caps., One compact field for the labelled view: reconstructed messages and depth., What the bounded thread reconstruction found, next to the mail. (+4 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.12
Nodes (24): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back. (+16 more)

### Community 34 - "RoutingRequest"
Cohesion: 0.14
Nodes (10): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., RoutingRequest (+2 more)

### Community 35 - "Learner"
Cohesion: 0.13
Nodes (22): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The confirmed rule that refused this arm, or '' when the user has not refused…, feedback(), Never tell me about these" is a never in the user's words and a yes in effect., The wiring, not just the rule: a line confirmed at a prompt moves a posterior. (+14 more)

### Community 36 - "EventStream"
Cohesion: 0.14
Nodes (11): EventStream, _json_default(), Any, A stable hash of the replay log., An append-only log of arriving events. There is no update, no delete and no…, Every appended event, in arrival order., The canonical JSONL replay log: header line, then one line per arrival., Append-only is structural: there is no update, delete or reorder. (+3 more)

### Community 37 - "EventValidationError"
Cohesion: 0.14
Nodes (15): DuplicateEventError, EventValidationError, ValueError, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text(), parametrize, Empty ids and malformed fields fail at construction, not at use. (+7 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "test_ui_session.py"
Cohesion: 0.10
Nodes (24): importlib_util, _call(), Any, Path, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET. (+16 more)

### Community 41 - "test_sim.py"
Cohesion: 0.06
Nodes (63): arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, interrupting_case_ids(), labelled_routes(), CaptureFixture (+55 more)

### Community 42 - "ClaimStore"
Cohesion: 0.13
Nodes (23): ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., ConsentRequired, RuntimeError (+15 more)

### Community 43 - "claims.py"
Cohesion: 0.13
Nodes (16): enum, _action_words(), _bears_on(), Claim, _claim_record(), Any, datetime, The claim in plain words: what to do, where it applies, from when. (+8 more)

### Community 44 - "Case"
Cohesion: 0.08
Nodes (37): Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, GoldPolicy, Choose the dataset's route when the floor still allows it, else escalate. The…, _dependencies_first(), dependencies_of() (+29 more)

### Community 45 - "RuleProvider"
Cohesion: 0.15
Nodes (16): The offline provider: proposes from triage, no network, deterministic. It is a…, RuleProvider, A table that hid the rules provider would show a run spending nothing and doing…, test_the_offline_provider_is_counted_and_costs_nothing(), message(), The noun decides: 'the Redis sharding key' is a field, and escalating it is…, The ask shape decides too: 'consider changing your password' is advice., A proposer that has to guess a tool name from a dataset id guesses wrong. (+8 more)

### Community 46 - "LaneView"
Cohesion: 0.08
Nodes (16): LaneView, RuntimeError, Raised when code reaches across the learning/held-out firewall., Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner. (+8 more)

### Community 47 - "test_triage.py"
Cohesion: 0.14
Nodes (16): amount_in(), The largest amount mentioned in a text, as a float., message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker() (+8 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.23
Nodes (15): approval_for(), The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, The yes a reviewer would send back for the work they were shown., session(), test_a_crash_before_the_work_ran_leaves_the_decision_waiting(), test_a_decision_that_moved_between_asking_and_answering_is_refused() (+7 more)

### Community 49 - "retrieve_style"
Cohesion: 0.16
Nodes (21): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from. (+13 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.08
Nodes (37): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, Manifest, ManifestError, ValueError, Every case in the dataset, sorted by sequence index, with its digest.…, Build a manifest from parsed rows, rejecting duplicate case ids and splits., Build a manifest from plain mail: sender, recipients, subject and body. A… (+29 more)

### Community 52 - "test_graph.py"
Cohesion: 0.17
Nodes (20): Router, SimulatedMailbox, LaneView, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts. (+12 more)

### Community 53 - "ClaimScope"
Cohesion: 0.12
Nodes (15): _from_context(), _narrowed(), The claim with the scope the answer named, or None when it named none., Resolve the scope from nouns first, and only then from the active item., _scope_for(), claim_id_for(), ClaimScope, A stable id for the same claim said twice, so it is never stored twice. (+7 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (14): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+6 more)

### Community 55 - "SimulatedMailbox"
Cohesion: 0.12
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 56 - ".labels"
Cohesion: 0.50
Nodes (3): CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only.

### Community 57 - "run_canonical.py"
Cohesion: 0.14
Nodes (18): cold_control(), main(), The four reference cases, run end to end and printed as transcripts. Each case…, What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route. (+10 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "drafting_for"
Cohesion: 0.17
Nodes (12): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+4 more)

### Community 60 - "write_mailbox"
Cohesion: 0.13
Nodes (15): generator_prompt(), parse_generated(), Route, One situation to write a mail about, and how a careful assistant would treat it., The request for one arrival. Everything fresh about it comes from this frame., Read one generated mail, naming what is wrong rather than guessing a field., A plain-text caller for one model role, or a named failure when it has no…, Write `count` fresh arrivals, cycling the briefs in a shuffled order. A… (+7 more)

### Community 61 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

### Community 62 - ".lines_for"
Cohesion: 0.25
Nodes (10): Decision, ModelUser, _note(), Message, The person whose mailbox this is, played by a model that is not the proposer.…, What the reply parser may look at: the mail and the decision, never a label., The lines to hand the waiting decision: the reply, and a confirmation if…, Whether the draft on the table may be saved. Nothing is approved by default. (+2 more)

### Community 63 - "ProposalGateway"
Cohesion: 0.10
Nodes (26): Message, One email message, in a thread, in one direction., ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., named_route(), ProposalPolicy, The route the user's own rules name for this mail, if any. Two sources count: a…, Decide from the pipeline: mail in, triage, proposal, floor, router, route out. (+18 more)

### Community 64 - "ask_curve"
Cohesion: 0.25
Nodes (6): ask_curve(), Block, The interruption curve: how many cases each block of the lane needed the user…, One block of a lane, in delivery order, and how much of it asked for the user., Blocks are the stream's own order, and four cases at block 12 is one block of…, test_the_curve_blocks_the_lane_in_delivery_order_and_the_last_block_may_be_short()

### Community 65 - "test_events.py"
Cohesion: 0.11
Nodes (28): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), Record one arrival, or refuse it and leave the stream untouched. The whole…, _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and… (+20 more)

### Community 66 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 67 - "test_cases.py"
Cohesion: 0.09
Nodes (48): Path, Check a case set's counts, enums and splits before anything is asked to run it.…, validate_cases(), _codes(), _extra(), Path, The case set's own checks: counts, enums, and nothing in two lanes. ``wajo data…, A thread carries its own history, so a repeat reveals an earlier lane's mail. (+40 more)

### Community 68 - "pytest"
Cohesion: 0.21
Nodes (12): pytest, Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 69 - "main"
Cohesion: 0.08
Nodes (45): ArgumentParser, ClaimStore, DecisionSource, Namespace, The pair's name, so a run says where a proposal could have come from., build_parser(), data_validate(), eval_all() (+37 more)

### Community 70 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "test_replay.py"
Cohesion: 0.05
Nodes (50): datetime, Replay events through a fresh seeded stream., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., replay(), SeededClock, manifest() (+42 more)

### Community 73 - "Route"
Cohesion: 0.09
Nodes (45): The route the run actually chose., The four autonomy outcomes a candidate action can be routed to.…, The least autonomous of these routes, which is the one that wins a…, Route, strictest(), email_context_for(), floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to. (+37 more)

### Community 74 - "trace.py"
Cohesion: 0.07
Nodes (47): digest_of(), GraphState, One decision, from arrival to receipt. Ids and hashes rather than the mail…, A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime (+39 more)

### Community 75 - "_judge_run"
Cohesion: 0.11
Nodes (17): _case_blocks(), Judge, _judge_run(), _judged(), Judgement, _preview(), GraphSession, Ask the judge about a sample of the second half: the routes, and the drafts.… (+9 more)

### Community 76 - "RememberedProvider"
Cohesion: 0.09
Nodes (18): Ledger, Protocol, _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., The user's own words, consulted before the provider. Wraps another provider:…, Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered. (+10 more)

### Community 77 - "Any"
Cohesion: 0.18
Nodes (10): Arrival, _by_id(), Any, One generated mail, with the brief and the writer's own opinion that produced…, The mail in the loader's own shape. It carries no labels, because it has none., What the run keeps beside the row: which brief wrote it, and what it expected., The runner's interrupt hook: the waiting decision gets its lines from the model., The arrivals of the half the agent had never seen, in delivery order. (+2 more)

### Community 78 - "ProposalRequest"
Cohesion: 0.18
Nodes (7): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, A model in the shape of the provider protocol, answering from a script., ScriptedProvider

### Community 79 - "SandboxError"
Cohesion: 0.24
Nodes (6): RuntimeError, Raised when the environment cannot be built or read., SandboxError, FakeModel, One stand-in for the endpoint: it writes mail, answers as the owner, and…, Answer whichever question the prompt asks, in the role whose stage it is.

### Community 80 - "test_loop.py"
Cohesion: 0.18
Nodes (15): Types scripted lines at the decisions that wait for a human. A line handed over…, ScriptedReplies, _drained(), loop(), Queue, Nothing hangs on a prompt the script never feeds: it is told a line that does…, A named case still waits for the second line, so an unanswered echo stores…, test_a_decision_the_script_does_not_answer_is_passed_on() (+7 more)

### Community 81 - "server.py"
Cohesion: 0.22
Nodes (9): main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., Point the server at a session, which is what the tests and the page both need., serve(), set_session(), http_server, ThreadingHTTPServer (+1 more)

### Community 83 - "Lane"
Cohesion: 0.07
Nodes (64): calibration_report(), dispositions(), held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both… (+56 more)

### Community 87 - "Block"
Cohesion: 0.20
Nodes (7): Block, classify(), Any, Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 88 - "router.py"
Cohesion: 0.17
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "Router"
Cohesion: 0.14
Nodes (29): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Router, case(), feedback(), _hints(), Path, The plan's check: the floor is not weighed against a preference, it is applied…, A rule the user confirmed is on the ballot on their word, not on the… (+21 more)

### Community 102 - "CaseReport"
Cohesion: 0.25
Nodes (3): CaseReport, What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails.

### Community 103 - "GraphError"
Cohesion: 0.25
Nodes (9): Authorization, PreparedAction, _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still… (+1 more)

### Community 104 - "LoopReport"
Cohesion: 0.17
Nodes (8): GraphOutcome, What a lane through the graph did., How many times a tool actually ran, counted from the receipts., LoopReport, One lane, walked with a baseline pipeline and with what the user said during it., Decisions that waited for a human, with nothing remembered yet., Decisions that would still wait for a human, with the rules in front., How many decisions the rules took off the user's screen.

### Community 105 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 106 - "ClaimType"
Cohesion: 0.20
Nodes (9): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, _claim_from_record(), ClaimType, Path, StrEnum, Take up the claims already in the store's file, when consent allows their use., What kind of thing the user told us. Each still needs its evidence. (+1 more)

### Community 107 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 108 - "run_simulation"
Cohesion: 0.23
Nodes (12): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+4 more)

### Community 109 - "_background_loop"
Cohesion: 0.29
Nodes (5): AbstractEventLoop, _background_loop(), Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 111 - "IO"
Cohesion: 0.29
Nodes (7): _banner(), _blocks(), IO, The opening block: what is running, and what it is pointed at., Rule off the next step, so a ten-minute run reads as parts, not one wall., Write pre-formatted blocks - a mail and its decision - as they are., _section()

### Community 112 - "json"
Cohesion: 0.50
Nodes (3): hashlib, json, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…

### Community 113 - ".hook"
Cohesion: 0.50
Nodes (3): InterruptHook, Queue, A hook that hands the waiting decision its lines, and closes input at the end.

### Community 114 - "test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in"
Cohesion: 0.67
Nodes (3): CaptureFixture, MonkeyPatch, test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in()

### Community 117 - "Session"
Cohesion: 0.14
Nodes (9): AnswerQueue, One calibration run, driven a line at a time. The run is the one the CLI drives…, Load the lane and begin the run. A failure here is the caller's to report., Called while a decision is on screen and before its line is read., Append one block, with the number the page polls from., The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Session (+1 more)

### Community 118 - "evaluate"
Cohesion: 0.09
Nodes (35): main(), Run the lanes, then print what they cost., RuntimeError, Refuse a record whose counts cannot add up to what the run processed., Raised when a run cannot be scored as asked, rather than scored wrongly., Join the two lanes into the report, refusing a pair that cannot be one run., ScoringError, two_lane_report() (+27 more)

### Community 119 - "autonomy/state.py"
Cohesion: 0.10
Nodes (23): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+15 more)

### Community 122 - "first_interrupt_of"
Cohesion: 0.28
Nodes (9): first_interrupt_of(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing(), test_an_approval_releases_the_prepared_action_and_is_learnable() (+1 more)

### Community 124 - "strictest_allowed"
Cohesion: 0.67
Nodes (3): The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), test_strictest_allowed_is_the_least_autonomous_route()

### Community 125 - "cli.py"
Cohesion: 0.13
Nodes (21): argparse, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The two-lane scorer: what the agent did, counted where it happened. The report…, Read a graph run, including the floor's ballot and who authorised each commit., Count a run's floor violations and unauthorized commits. The floor's ballot is…, record_from_graph(), safety_counts() (+13 more)

### Community 130 - "EvalReport"
Cohesion: 0.11
Nodes (12): Disposition, EvalReport, main(), LaneView, Path, Both lanes, kept apart: one disposition count over everything, two assessments., How a lane's cases were handled, mutually exclusive by construction., Write the report as JSON, naming the file in the error rather than failing mute. (+4 more)

### Community 135 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

## Knowledge Gaps
- **14 isolated node(s):** `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES`, `Silence is not approval` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `policy.py`, `registry.py`, `test_economics.py`, `runner.py`, `dataset.py`, `test_benign_workplace_clean_pass`, `ScopeAnchor`, `test_floor.py`, `test_claim_schema.py`, `ChatRunner`, `FeedbackEvent`, `sandbox.py`, `test_gateway.py`, `test_sim_tools.py`, `floor.py`, `test_predrafts.py`, `RoutingRequest`, `Learner`, `test_ui_session.py`, `test_sim.py`, `claims.py`, `Case`, `RuleProvider`, `Manifest`, `ClaimScope`, `run_canonical.py`, `ProposalGateway`, `test_events.py`, `pytest`, `trace.py`, `RememberedProvider`, `Lane`, `router.py`, `Router`, `ClaimType`, `first_interrupt_of`, `strictest_allowed`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `LaneView` connect `LaneView` to `Router`, `Learner`, `runner.py`, `dataset.py`, `Route`, `RememberedProvider`, `ChatRunner`, `run_simulation`, `test_loop.py`, `sandbox.py`, `Manifest`, `Session`, `evaluate`, `Lane`, `test_graph.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Message` connect `ProposalGateway` to `ReplyTree`, `policy.py`, `test_events.py`, `EventValidationError`, `dataset.py`, `trace.py`, `RememberedProvider`, `RuleProvider`, `test_triage.py`, `sandbox.py`, `build_reply_tree`, `test_sim_tools.py`, `agent/state.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 147 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 147 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 53 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 53 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 32 INFERRED edges - model-reasoned connections that need verification._