# Graph Report - ai-email-agent  (2026-09-20)

## Corpus Check
- 101 files · ~115,423 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2829 nodes · 7092 edges · 164 communities (131 shown, 33 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1013 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62c3da66`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FeedbackEvent
- route_decision
- GraphRuntime
- registry.py
- session_grant
- Ledger
- feedback.py
- Case
- Bucket
- run_simulation
- test_floor.py
- test_claim_schema.py
- ChatRunner
- _answer
- Handler
- sandbox.py
- test_sandbox.py
- HeldOutReport
- loop_run
- runner.py
- test_gateway.py
- Proposal
- floor.py
- test_sim_tools.py
- Effect
- validate_draft
- .render
- ProposalError
- run_sandbox
- app.js
- test_router.py
- drafts.py
- test_jev.py
- test_predrafts.py
- Posterior
- Learner
- EventStream
- dataset.py
- mask_for_llm
- PresidioMasker
- Session
- build_reply_tree
- run_canonical.py
- ClaimStore
- evaluate
- test_sim.py
- SentExample
- GraphSession
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- run_graph
- Triage
- OpenAICompatibleProvider
- JevRouted
- ScopeAnchor
- Any
- EffectLog
- injection.py
- Claim
- graph.py
- ModelUser
- schedule
- .start
- build_parser
- ScoringError
- test_cases.py
- eval_all
- main
- Cutoffs
- SplitViolation
- test_replay.py
- Router
- ToolError
- ContextPhoneRecognizer
- Tool
- SandboxError
- ProposalRequest
- Jev
- test_loop.py
- test_freeze.py
- Workflow: graphify
- Route
- email-autonomy-agent
- ClaimScope
- pytest
- .route
- rules/graphify.md
- DESIGN.md
- README.md
- analysis.md — how the agent actually did
- Claim
- LoopReport
- .labels
- Transcript 1 - a live mailbox, decided end to end
- Judge
- masker.py
- TraceSink
- Validation
- Path
- valid
- GraphSession
- LaneRecord
- LaneView
- ScopeAnchor
- SimulatedMailbox
- test_eval_run.py
- get_token_map
- ValueError
- plan_deviation
- SeededClock
- SimpleNamespace
- parametrize
- fixture
- TraceSink
- Queue
- Random
- DecisionSource
- Disposition
- EvalReport
- replay
- server.py
- ScriptedReplies
- ClaimStore
- graph_run
- GraphError
- Message
- timedelta
- _server
- ClaimScope
- ScriptedTeaching
- run_two_lanes
- .__init__
- Transcript
- FeedbackContext
- rule
- provenance
- Reading
- SafetyCounts
- FeedbackContext
- render
- dependencies_of
- Window
- AnswerQueue
- fill_placeholder_bodies.py
- SimError
- reply
- Exception
- _address
- _bucket_of
- action_vocabulary
- test_stream_refuses_a_duplicate_arrival

## God Nodes (most connected - your core abstractions)
1. `Route` - 164 edges
2. `Router` - 65 edges
3. `Lane` - 57 edges
4. `Learner` - 56 edges
5. `run_sandbox()` - 53 edges
6. `ChatRunner` - 52 edges
7. `ClaimStore` - 52 edges
8. `Manifest` - 46 edges
9. `ActionPayload` - 45 edges
10. `Claim` - 45 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `cold_control()` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py
- `preference_for()` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py
- `Transcript` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py
- `case()` --uses--> `Case`  [INFERRED]
  tests/test_floor_protection.py → src/agent/dataset.py

## Import Cycles
- None detected.

## Communities (164 total, 33 thin omitted)

### Community 0 - "FeedbackEvent"
Cohesion: 0.09
Nodes (25): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, is_learnable() (+17 more)

### Community 1 - "route_decision"
Cohesion: 0.14
Nodes (15): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, email_context_for(), _params_with_case(), Any, Give the action the ids the floor needs to resolve recipients and targets., Everything the router may consider about one arrival, and nothing else., The least autonomous route the floor left open, which is the fail-closed one. (+7 more)

### Community 2 - "GraphRuntime"
Cohesion: 0.11
Nodes (35): CompiledStateGraph, authorize(), _bound(), build_graph(), _case(), consent(), GraphRuntime, hold() (+27 more)

### Community 3 - "registry.py"
Cohesion: 0.06
Nodes (44): Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief(), _digest(), _notify_text() (+36 more)

### Community 4 - "session_grant"
Cohesion: 0.12
Nodes (29): Capability, ConsentRequired, Grant, LearningConsent, datetime, RuntimeError, StrEnum, What the agent is able to do. Holding one says nothing about being allowed to. (+21 more)

### Community 5 - "Ledger"
Cohesion: 0.09
Nodes (31): OpenAICompatibleProvider, SimpleNamespace, Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider() (+23 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (41): FeedbackKind, _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed() (+33 more)

### Community 7 - "Case"
Cohesion: 0.12
Nodes (13): Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., Decision, ProposalPolicy, Decide from the pipeline: mail in, triage, proposal, floor, router, route out., What the simulator does with one arrival., Whether this route has to wait for the user. (+5 more)

### Community 8 - "Bucket"
Cohesion: 0.11
Nodes (24): BetaStore, Bucket, _bucket_from(), Random, Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "run_simulation"
Cohesion: 0.15
Nodes (17): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did., How many times a tool actually ran, counted from the receipts. (+9 more)

### Community 10 - "test_floor.py"
Cohesion: 0.05
Nodes (71): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, parametrize, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify that every tool and parameter boundary resolves to the exact ActionClass., FLR-001: Financial transactions in action params must escalate. (+63 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.13
Nodes (23): ClaimError, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize, Protected attributes are out of memory by construction, not by a filter: the…, One claim as the parser hands it over: a class of mail, and the words that said… (+15 more)

### Community 12 - "ChatRunner"
Cohesion: 0.16
Nodes (11): ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.…, Ask the one bounded question and store the rule only if it is confirmed., Commit the work the user just approved, bound to the prepared digest., What the reply parser may look at: the mail and the decision, never a label., Consume lines typed while the previous decision was live. The settle first,… (+3 more)

### Community 13 - "_answer"
Cohesion: 0.16
Nodes (16): _answer(), JevError, _post(), Any, Route, RuntimeError, Jev could not answer. The caller decides what a missing routing opinion means., Post one request, or hand it to the transport a test supplied. (+8 more)

### Community 14 - "Handler"
Cohesion: 0.13
Nodes (13): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., Point the server at a session, which is what the tests and the page both need., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent. (+5 more)

### Community 15 - "sandbox.py"
Cohesion: 0.06
Nodes (40): datetime, as_dict(), _banner(), _blocks(), _judge_run(), _judged(), Judgement, _learning_section() (+32 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.09
Nodes (41): FakeModel, Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, One stand-in for the endpoint: it writes mail, answers as the owner, and…, The endpoint that answers everything except the owner's own questions., The whole environment on stand-ins: no key, no network, no judge., The mail is written once. A second reading replays it, its proposals and the…, Each half decides exactly the arrivals it was given, and nothing goes missing. (+33 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.14
Nodes (10): Gate, HeldOutReport, _rate(), A count and its denominator, which is the only honest way to print a rate., A hard gate: a number that has to hold, not a curve that has to trend., The sealed lane: the only place accuracy is measured, and the hard gates., The plan's hard gates, each stated with the count and its denominator. An empty…, The hard gates as data, so a build can fail on them without reading prose. (+2 more)

### Community 18 - "loop_run"
Cohesion: 0.19
Nodes (17): LoopReport, Namespace, _keep_rules(), loop_run(), _open_store(), IO, Say what the reader is looking at, since labels change the calibration., The run's memory: the rules already kept, and the file they live in. (+9 more)

### Community 19 - "runner.py"
Cohesion: 0.13
Nodes (35): argparse, asyncio, collections_abc, dataclasses, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, cost_dict(), The two-lane scorer: what the agent did, counted where it happened. The report…, The cost table as data, under the deflection rate that justifies the cheap… (+27 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.08
Nodes (36): ProposalGateway, The offline provider: proposes from triage, no network, deterministic. It is a…, Turns provider text into a validated proposal, with one repair attempt., RuleProvider, BrokenProvider, message(), quiet_but_wrong(), The model proposal gateway: untrusted output, one repair, then fail closed. (+28 more)

### Community 21 - "Proposal"
Cohesion: 0.11
Nodes (27): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule(), Proposal (+19 more)

### Community 22 - "floor.py"
Cohesion: 0.09
Nodes (41): ActionClass, classify_action(), EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement() (+33 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.16
Nodes (25): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+17 more)

### Community 24 - "Effect"
Cohesion: 0.19
Nodes (10): ArchiveEmail, Draft, _email_id(), Any, Files a message out of the inbox., A private draft. Preparation, not sending., Read-only: returns the message it was pointed at., ReadEmail (+2 more)

### Community 25 - "validate_draft"
Cohesion: 0.13
Nodes (32): parametrize, DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the… (+24 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (11): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+3 more)

### Community 27 - "ProposalError"
Cohesion: 0.12
Nodes (22): main(), Run the lanes, then print what they cost., build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes…, proposing_provider() (+14 more)

### Community 28 - "run_sandbox"
Cohesion: 0.07
Nodes (30): LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a graph run, including the floor's ballot and who authorised each commit., Count a run's floor violations and unauthorized commits. The floor's ballot is…, record_from_graph(), safety_counts(), CachingProvider, _case_blocks() (+22 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "test_router.py"
Cohesion: 0.15
Nodes (20): named_route(), The route the user's own rules name for this mail, if any. Two sources count: a…, case(), _hints(), A model in the shape of the provider protocol, answering from a script., The plan's check: the floor is not weighed against a preference, it is applied…, A model's own route is not a preference: it has to wait for the posterior., An untrusted proposal is the thing the router tests, so it cannot buy silence. (+12 more)

### Community 31 - "drafts.py"
Cohesion: 0.10
Nodes (29): Case, carried_instruction(), draft_reply(), drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+21 more)

### Community 32 - "test_jev.py"
Cohesion: 0.22
Nodes (20): answer(), FakeJev, hybrid(), message(), The Jev hybrid: Jev decides the route, the model does the work, the floor still…, A wrapped model, the model's own script, and the ledger both of them write into., Drive the wrapper the way the gateway does, and hand back what it answered., No work to prepare, so the text model is not called at all. (+12 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (22): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+14 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.13
Nodes (25): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The confirmed rule that refused this arm, or '' when the user has not refused…, FeedbackKind, StrEnum, What the user did after seeing a decision. Values are the dataset's… (+17 more)

### Community 36 - "EventStream"
Cohesion: 0.12
Nodes (13): EventStream, _json_default(), Any, A stable hash of the replay log., An append-only log of arriving events. There is no update, no delete and no…, Every appended event, in arrival order., The canonical JSONL replay log: header line, then one line per arrival., An arrival numbered before the last one is out of order, not a new arrival. (+5 more)

### Community 37 - "dataset.py"
Cohesion: 0.05
Nodes (68): enum, _attachment(), _case_from_mail_row(), event_from_row(), _message(), Any, datetime, Dataset manifest and the split firewall (Phase 3.2). The dataset is loaded… (+60 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Session"
Cohesion: 0.13
Nodes (20): importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one… (+12 more)

### Community 41 - "build_reply_tree"
Cohesion: 0.21
Nodes (15): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, Reconstruct one case's thread, bounded by the reply-tree caps., thread_tree_for(), message(), A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected(), test_cycle_is_walked_once() (+7 more)

### Community 42 - "run_canonical.py"
Cohesion: 0.12
Nodes (21): cold_control(), main(), preference_for(), The four reference cases, run end to end and printed as transcripts. Each case…, The scoped preference a confirmed rule would leave behind for this sender.…, What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it. (+13 more)

### Community 43 - "ClaimStore"
Cohesion: 0.06
Nodes (31): Grant, ProposalProvider, _answered_cases(), IO, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Each arrival a rule answered, mapped to the arrival whose mail taught that rule., run_loop(), _bears_on() (+23 more)

### Community 44 - "evaluate"
Cohesion: 0.22
Nodes (13): evaluate(), _frozen(), Any, LaneView, Path, ProposalProvider, TraceSink, Teach, freeze, and score the sealed lane exactly once. (+5 more)

### Community 45 - "test_sim.py"
Cohesion: 0.06
Nodes (73): arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, first_interrupt_of(), interrupting_case_ids(), labelled_routes() (+65 more)

### Community 46 - "SentExample"
Cohesion: 0.19
Nodes (10): examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over., The consented sent examples a case carries, if the mailbox offered any. Not the…, SentExample (+2 more)

### Community 47 - "GraphSession"
Cohesion: 0.18
Nodes (11): Command, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, Carry a thread past its interrupt, or past the point a crash cut it off at. (+3 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.20
Nodes (17): approval_for(), Flaky, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, A provider that answers differently the second time it is asked about a mail., The yes a reviewer would send back for the work they were shown., session() (+9 more)

### Community 49 - "retrieve_style"
Cohesion: 0.14
Nodes (22): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., What the kept examples cost, in the same rough unit as the cap., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example() (+14 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.06
Nodes (48): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, _case_from_row(), LaneView, Manifest, ManifestError, ValueError, Build one case, naming the case on anything the row gets wrong. A bare… (+40 more)

### Community 52 - "run_graph"
Cohesion: 0.21
Nodes (14): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+6 more)

### Community 53 - "Triage"
Cohesion: 0.08
Nodes (27): Proposal, _domain(), proposal_from(), Message, ProposalRequest, What the user's own words amount to for this mail, if anything., The claim's route, with whatever work the inner provider chose for the mail. An…, One claim as a proposal, or None when the claim names no route. (+19 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.11
Nodes (15): Ledger, _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured. (+7 more)

### Community 55 - "JevRouted"
Cohesion: 0.22
Nodes (7): ProposalRequest, JevRouted, Jev decides how much autonomy the mail gets; the model decides what the work…, The pair's name, so a run says where a proposal could have come from., Whichever models answered, named the way a run names them., Compose one proposal: the route from Jev, the work from the model., The model's own answer, kept whole, with the reason it was needed named.

### Community 56 - "ScopeAnchor"
Cohesion: 0.10
Nodes (37): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means. (+29 more)

### Community 57 - "Any"
Cohesion: 0.13
Nodes (14): Arrival, _by_id(), Any, The arrivals of the half the agent had never seen, in delivery order., The arrivals one record decided, in the order it decided them., One generated mail, with the brief and the writer's own opinion that produced…, The mail in the loader's own shape. It carries no labels, because it has none., What the run keeps beside the row: which brief wrote it, and what it expected. (+6 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "injection.py"
Cohesion: 0.07
Nodes (33): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+25 more)

### Community 60 - "Claim"
Cohesion: 0.14
Nodes (16): _action_words(), Claim, _claim_from_record(), claim_id_for(), _claim_record(), Any, Route, The claim in plain words: what to do, where it applies, from when. (+8 more)

### Community 61 - "graph.py"
Cohesion: 0.09
Nodes (29): hashlib, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, The route chosen, and everything that was ruled out on the way., The chosen route's expected loss, in handoffs., One line for a transcript or a reason. Deliberately terse: a trace digests a… (+21 more)

### Community 62 - "ModelUser"
Cohesion: 0.15
Nodes (15): Decision, ModelUser, _note(), Message, A run that takes a while should say what it is doing, rather than look hung., The person whose mailbox this is, played by a model that is not the proposer.…, Keep the owner's answer for an arrival, the way the run will read it back., Read back what the owner said, and say how many answers that covers. (+7 more)

### Community 63 - "schedule"
Cohesion: 0.14
Nodes (24): _dependencies_first(), RuntimeError, Raised when a case names a dependency no window can deliver before it., Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., Keep the drawn order, moving a case after anything it says it waits for.…, release_order(), schedule() (+16 more)

### Community 64 - ".start"
Cohesion: 0.14
Nodes (11): AbstractEventLoop, _background_loop(), Block, classify(), Any, Load the lane and begin the run. A failure here is the caller's to report., Append one block, with the number the page polls from., One event loop for the process, running on its own thread. HTTP handlers arrive… (+3 more)

### Community 65 - "build_parser"
Cohesion: 0.18
Nodes (13): ArgumentParser, build_parser(), _default_provider(), The provider a run proposes with when the flag is absent. Read here rather than…, The provider the sandbox proposes with when the flag is absent. The sandbox…, The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags() (+5 more)

### Community 66 - "ScoringError"
Cohesion: 0.11
Nodes (15): ask_curve(), Block, CalibrationReport, RuntimeError, Raised when a run cannot be scored as asked, rather than scored wrongly., One block of a lane, in delivery order, and how much of it asked for the user., The interruption curve: how many cases each block of the lane needed the user…, Refuse a record whose counts cannot add up to what the run processed. (+7 more)

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (63): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+55 more)

### Community 68 - "eval_all"
Cohesion: 0.16
Nodes (13): DecisionSource, ProposalGateway, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., eval_all(), _policy(), _proposing(), _provider_for() (+5 more)

### Community 69 - "main"
Cohesion: 0.20
Nodes (10): data_validate(), main(), Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard., Print what a case set holds and everything wrong with it., Entry point for the ``wajo`` console script., sandbox_run_command(), CaptureFixture, MonkeyPatch (+2 more)

### Community 70 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 71 - "SplitViolation"
Cohesion: 0.13
Nodes (12): RuntimeError, Raised when code reaches across the learning/held-out firewall., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., SplitViolation, The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read., The separation is symmetric: a lane view only sees its own rows. (+4 more)

### Community 72 - "test_replay.py"
Cohesion: 0.09
Nodes (21): fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, Counts per split and per lane, with the dataset's real sizes., A replay can name the exact dataset it ran against., Ground truth has to be reachable by scoring and out of reach of a decision., Every case lands in exactly one lane., An id that is in no lane is not a firewall breach, just a miss., The sealed lane holds the whole adversarial split plus the ordinary gold set. (+13 more)

### Community 73 - "Router"
Cohesion: 0.10
Nodes (41): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., approve() (+33 more)

### Community 74 - "ToolError"
Cohesion: 0.16
Nodes (9): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A send that validates like a real one and never leaves the mailbox. Recipients…, A message to the user's own assistant, never to anyone else., SendEmail, ValueError, Raised when a tool is asked for something it cannot do. (+1 more)

### Community 75 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 76 - "Tool"
Cohesion: 0.15
Nodes (9): ABC, CreateDraft, LabelEmail, Writes a private draft. Reversible, and never a send., Applies one label to one message., One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit. (+1 more)

### Community 77 - "SandboxError"
Cohesion: 0.09
Nodes (24): arrival_from_record(), drawn_briefs(), generator_prompt(), load_mailbox(), parse_generated(), Route, RuntimeError, How many arrivals took each of the four routes. (+16 more)

### Community 78 - "ProposalRequest"
Cohesion: 0.22
Nodes (5): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…

### Community 79 - "Jev"
Cohesion: 0.18
Nodes (9): Jev, ProposalProvider, The route question, asked over HTTP and metered like every other call., The hybrid, as a run selects it: Jev in front of whatever provider it was given., route_by_jev(), The text model, answering from a script so nothing reaches a network., ScriptedModel, test_the_hybrid_needs_a_key_to_route() (+1 more)

### Community 80 - "test_loop.py"
Cohesion: 0.18
Nodes (17): asked(), _drained(), loop(), Queue, A named case still waits for the second line, so an unanswered echo stores…, Nothing hangs on a prompt the script never feeds: it is told a line that does…, Calibrating on the same mail twice asks once: the rule answers the second time., test_a_decision_the_script_does_not_answer_is_passed_on() (+9 more)

### Community 81 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 83 - "Route"
Cohesion: 0.08
Nodes (64): calibration_report(), dispositions(), held_out_report(), Count routes into the three dispositions, refusing a route nobody defined., Read a chat run: its per-case routes, what it asked, and what the user typed., Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both…, record_from_chat() (+56 more)

### Community 87 - "ClaimScope"
Cohesion: 0.15
Nodes (18): _entries(), freeze(), load(), Any, Path, Freezing what a run learned, so the next one starts where it stopped. Three…, Write the frozen state, naming the file in the failure rather than raising…, Read a frozen state back, or say what about it could not be read. (+10 more)

### Community 88 - "pytest"
Cohesion: 0.05
Nodes (51): fixture, pytest, Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records. (+43 more)

### Community 98 - ".route"
Cohesion: 0.17
Nodes (9): JevAnswer, Message, One typed decision, with the distribution behind it., What the choice carried, for the proposal schema's own confidence field. The…, One line a rationale can carry: the answer, the spread, and how long it took., One choice, off the event loop, metered with whatever the endpoint reported., Count the call, its tokens, and the price the response states for itself., The mail, plus what pre-triage already knows and the model is told as well. (+1 more)

### Community 100 - "DESIGN.md"
Cohesion: 0.13
Nodes (13): Deliberately not built, Learning is posteriors plus scoped rules, One arrival, one route, and the route names the work, Replay and the split firewall, Scoring is expected loss in one unit, State and traces carry ids, never mail, The eval is deepeval GEval, and it never carries a gate, The floor masks the ballot before anything is scored (+5 more)

### Community 102 - "analysis.md — how the agent actually did"
Cohesion: 0.15
Nodes (12): analysis.md — how the agent actually did, how to reproduce, no LLM vs LLM only vs Jev + LLM, run a — 15 arrivals, 7 to learn on, 7 cold, run a vs run b, run b — 40 arrivals, 20 to learn on, 19 cold, the four states, in plain words, the short version (+4 more)

### Community 104 - "LoopReport"
Cohesion: 0.14
Nodes (8): LoopReport, Decisions that would still wait for a human, with the rules in front., Decisions the same lane waits on with nothing remembered, or 0 with no control., Arrivals a rule sent somewhere else than the lane would have gone on its own., Of those, the arrivals that came after the mail their rule was taught on. This…, Asking the rules took off the user, measured against the lane with no rules.…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions the chat pass waited on. Not a baseline: a rule takes effect from the…

### Community 105 - ".labels"
Cohesion: 0.50
Nodes (3): CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only.

### Community 106 - "Transcript 1 - a live mailbox, decided end to end"
Cohesion: 0.15
Nodes (12): 1. The console, verbatim, 2. The four states, and what each one actually does, 3. How well it did, on the half it had never seen, 4. Arrival by arrival, against the brief, 5. Analysis, 6. What this run cannot tell you, 7. Charts, Calibration — the half that teaches (+4 more)

### Community 107 - "Judge"
Cohesion: 0.25
Nodes (5): Judge, Ask one question about one case. A judge that fails says so and scores nothing., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI.

### Community 108 - "masker.py"
Cohesion: 0.20
Nodes (9): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, _clean_person_name(), _create_analyzer(), PII Masking with Microsoft Presidio (Phase 2). Provides a warm singleton…, Build the Presidio analyzer, preferring the large spaCy model. (+1 more)

### Community 109 - "TraceSink"
Cohesion: 0.07
Nodes (44): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+36 more)

### Community 111 - "Path"
Cohesion: 0.19
Nodes (12): charts(), _digest(), Path, Keep a run's transcript, naming the file in the error rather than failing mute., The hash of a file the run produced, so an artifact names what it was made from., Keep the mailbox itself, so a report can be read next to the mail that produced…, The three pictures: what it decided, how often it asked, and how it matched., Write the recording, one answer per line, so a re-run can read it back. (+4 more)

### Community 112 - "valid"
Cohesion: 0.23
Nodes (12): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., parametrize, The net under the gate: a proposal from some other path still cannot land…, The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses(), test_a_valid_answer_parses(), test_an_action_nothing_implements_resolves_to_itself() (+4 more)

### Community 117 - "SimulatedMailbox"
Cohesion: 0.13
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 118 - "test_eval_run.py"
Cohesion: 0.19
Nodes (19): load_script(), Read a transcript, naming what is wrong with it rather than failing on a…, Manifest, evaluate(), mini_manifest(), mini_script(), Path, The eval run: teach the learning lane, freeze it, then score the sealed lane… (+11 more)

### Community 119 - "get_token_map"
Cohesion: 0.22
Nodes (9): forget_thread(), get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., Drop a thread's token registry and reverse map., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded() (+1 more)

### Community 121 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 122 - "SeededClock"
Cohesion: 0.22
Nodes (7): datetime, A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., SeededClock, Same seed, same time; different seed, different start., test_clock_is_deterministic_for_a_seed()

### Community 130 - "Disposition"
Cohesion: 0.29
Nodes (3): Disposition, How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to.

### Community 131 - "EvalReport"
Cohesion: 0.24
Nodes (5): EvalReport, Any, Path, Both lanes, kept apart: one disposition count over everything, two assessments., Write the report as JSON, naming the file in the error rather than failing mute.

### Community 132 - "replay"
Cohesion: 0.20
Nodes (10): Replay events through a fresh seeded stream., replay(), The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival., The log's order is the dataset's sequence order, not file order., test_a_different_seed_changes_the_log(), test_log_is_canonical_jsonl_with_a_header() (+2 more)

### Community 133 - "server.py"
Cohesion: 0.25
Nodes (8): dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, ThreadingHTTPServer, webbrowser

### Community 134 - "ScriptedReplies"
Cohesion: 0.25
Nodes (5): InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., ScriptedReplies

### Community 136 - "graph_run"
Cohesion: 0.33
Nodes (7): graph_run(), GraphSession, Walk a fixture through the decision graph and say what each arrival ended in., Answer one held decision with a yes and say what that committed., _resume_note(), The deliverable flow: calibrate once, then run autonomously in a later process., test_a_rule_kept_by_calibration_is_in_force_in_the_next_run()

### Community 137 - "GraphError"
Cohesion: 0.33
Nodes (7): _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still…, The graph cannot continue, naming the case it stopped on.

### Community 138 - "Message"
Cohesion: 0.12
Nodes (19): Message, One email message, in a thread, in one direction., _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order. (+11 more)

### Community 139 - "timedelta"
Cohesion: 0.29
Nodes (7): Nothing reads the wall clock, so time is frozen until the simulation moves it., A custom epoch and tick are honoured; a non-positive advance is refused., The seed offsets within the first minute, so replays stay plausible., test_clock_can_be_configured_but_not_moved_backwards(), test_clock_starts_at_the_dataset_epoch_and_only_moves_on_advance(), test_seed_offsets_the_start_but_keeps_the_epoch(), timedelta

### Community 140 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 142 - "ScriptedTeaching"
Cohesion: 0.33
Nodes (3): The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., ScriptedTeaching

### Community 143 - "run_two_lanes"
Cohesion: 0.40
Nodes (5): main(), LaneView, Walk both lanes with nobody at the keyboard, and score what they did. Input is…, Run both lanes and print the report, so the scorer can be read before it is…, run_two_lanes()

### Community 144 - ".__init__"
Cohesion: 0.40
Nodes (3): GraphOutcome, What a lane through the graph did., How many times a tool actually ran, counted from the receipts.

### Community 147 - "rule"
Cohesion: 0.40
Nodes (5): A rule the user confirmed is on the ballot on their word, not on the…, A confirmed rule, the way the parser hands one over., rule(), test_a_confirmed_preference_enables_a_later_archive_before_trust_is_earned(), test_a_refused_arm_leaves_the_ballot_and_is_named_on_the_receipt()

### Community 148 - "provenance"
Cohesion: 0.50
Nodes (4): git_sha(), provenance(), The commit the run came from, so an artifact can be traced to the code that…, What produced a report: the code, the versions and the models, not only the…

### Community 152 - "render"
Cohesion: 0.50
Nodes (4): main(), What the run did, in the order a reader wants it: provenance, then the numbers., The eval run as a command, for anyone who would rather not go through the CLI., render()

### Community 153 - "dependencies_of"
Cohesion: 0.50
Nodes (4): dependencies_of(), Any, The ids a case says must arrive before it, from…, _row_of()

### Community 154 - "Window"
Cohesion: 0.50
Nodes (3): One released window: its cases in delivery order, and the seed that ordered it., The window's case ids in the order they will arrive., Window

### Community 157 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

## Knowledge Gaps
- **47 isolated node(s):** `What it measures at`, `One arrival, one route, and the route names the work`, `The floor masks the ballot before anything is scored`, `Scoring is expected loss in one unit`, `The model proposes, the code decides` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `FeedbackEvent`, `route_decision`, `registry.py`, `Case`, `test_floor.py`, `test_claim_schema.py`, `ChatRunner`, `runner.py`, `test_gateway.py`, `Proposal`, `floor.py`, `rule`, `test_sim_tools.py`, `test_router.py`, `test_jev.py`, `test_predrafts.py`, `Learner`, `dataset.py`, `Session`, `run_canonical.py`, `test_sim.py`, `test_graph_resume.py`, `Manifest`, `injection.py`, `graph.py`, `test_cases.py`, `Router`, `test_freeze.py`, `pytest`, `TraceSink`, `valid`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `ClaimStore` connect `ClaimStore` to `eval_all`, `session_grant`, `Session`, `run_simulation`, `run_canonical.py`, `test_claim_schema.py`, `evaluate`, `ChatRunner`, `test_loop.py`, `loop_run`, `runner.py`, `Triage`, `ScopeAnchor`, `run_sandbox`, `test_router.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `ChatRunner` connect `ChatRunner` to `FeedbackEvent`, `GraphRuntime`, `registry.py`, `session_grant`, `feedback.py`, `Case`, `run_simulation`, `Message`, `runner.py`, `Window`, `Learner`, `EventStream`, `Session`, `run_canonical.py`, `ClaimStore`, `Manifest`, `Claim`, `.start`, `Router`, `Route`, `TraceSink`, `SimulatedMailbox`, `SeededClock`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 137 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 137 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 29 INFERRED edges - model-reasoned connections that need verification._