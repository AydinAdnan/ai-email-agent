# Graph Report - ai-email-agent  (2026-09-20)

## Corpus Check
- 100 files · ~104,773 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2691 nodes · 6981 edges · 142 communities (127 shown, 15 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 1081 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `baf4259e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- Case
- GraphRuntime
- registry.py
- ClaimStore
- ProposalGateway
- feedback.py
- dataset.py
- Bucket
- run_simulation
- ActionPayload
- test_claim_schema.py
- ChatRunner
- hybrid
- Handler
- sandbox.py
- test_sandbox.py
- HeldOutReport
- loop_run
- runner.py
- test_gateway.py
- Proposal
- VetoLevel
- Route
- Effect
- test_draft_validation.py
- .render
- ProposalError
- _claim_from_record
- app.js
- injection.py
- drafts.py
- stranger_mail
- Drafting
- Posterior
- Learner
- SeededClock
- test_events.py
- mask_for_llm
- PresidioMasker
- Session
- SimulatedMailbox
- run_scenario
- Claim
- schedule
- test_sim.py
- drafting_for
- SplitViolation
- test_graph_resume.py
- retrieve_style
- Routes
- Lane
- run_graph
- safety/__init__.py
- OpenAICompatibleProvider
- Block
- ScopeAnchor
- run_sandbox
- EffectLog
- test_floor.py
- .prepare
- graph.py
- ModelUser
- test_triage.py
- ClaimScope
- build_parser
- test_denominators.py
- test_cases.py
- _background_loop
- main
- evaluate
- test_a_strangers_instructions_fence_every_route_whatever_the_action
- test_replay.py
- Router
- TraceSink
- ContextPhoneRecognizer
- _server
- Any
- ProposalRequest
- SandboxError
- test_loop.py
- test_freeze.py
- Workflow: graphify
- held_out_report
- email-autonomy-agent
- autonomy/state.py
- test_loss_matrix.py
- Predraft
- rules/graphify.md
- DESIGN.md
- README.md
- analysis.md — how the agent actually did
- Transcript
- LoopReport
- .labels
- Transcript 1 - a live mailbox, decided end to end
- Judge
- masker.py
- pytest
- Validation
- write_mailbox
- EmailContext
- set_session
- cli.py
- ToolError
- Tool
- RememberedProvider
- test_eval_run.py
- get_token_map
- offline_provider
- plan_deviation
- GraphError
- server.py
- Style
- _context
- CalibrationReport
- Queue
- Random
- DecisionSource
- EvalReport
- test_cli_replays_the_fixture
- RuleProvider
- ScriptedReplies
- SafetyCounts
- _provider_for
- NotifyUser
- AnswerQueue
- ScheduleError
- .case_ids
- action_vocabulary
- intents_matching

## God Nodes (most connected - your core abstractions)
1. `Route` - 187 edges
2. `Lane` - 70 edges
3. `Router` - 69 edges
4. `Learner` - 61 edges
5. `Manifest` - 54 edges
6. `ChatRunner` - 53 edges
7. `Case` - 50 edges
8. `ProposalGateway` - 49 edges
9. `ClaimStore` - 46 edges
10. `ActionPayload` - 45 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `run_two_lanes()` --uses--> `GraphSession`  [INFERRED]
  evals/harness.py → src/agent/graph.py
- `evaluate()` --uses--> `GraphSession`  [INFERRED]
  evals/run_eval.py → src/agent/graph.py
- `preference_for()` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py
- `Transcript` --uses--> `Case`  [INFERRED]
  evals/run_canonical.py → src/agent/dataset.py

## Import Cycles
- None detected.

## Communities (142 total, 15 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.17
Nodes (11): Command, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, Carry a thread past its interrupt, or past the point a crash cut it off at. (+3 more)

### Community 1 - "Case"
Cohesion: 0.10
Nodes (20): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., email_context_for(), GoldPolicy, _params_with_case() (+12 more)

### Community 2 - "GraphRuntime"
Cohesion: 0.11
Nodes (35): CompiledStateGraph, authorize(), _bound(), build_graph(), _case(), consent(), GraphRuntime, hold() (+27 more)

### Community 3 - "registry.py"
Cohesion: 0.11
Nodes (25): build_registry(), Every simulated tool, over one mailbox., Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, PreparedAction (+17 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (43): _answered_cases(), Each arrival a rule answered, mapped to the arrival whose mail taught that rule., ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Capability, ConsentRequired, Grant (+35 more)

### Community 5 - "ProposalGateway"
Cohesion: 0.09
Nodes (39): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider() (+31 more)

### Community 6 - "feedback.py"
Cohesion: 0.10
Nodes (32): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+24 more)

### Community 7 - "dataset.py"
Cohesion: 0.08
Nodes (36): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime, Dataset manifest and the split firewall (Phase 3.2). The dataset is loaded… (+28 more)

### Community 8 - "Bucket"
Cohesion: 0.09
Nodes (26): The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Random, Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+18 more)

### Community 9 - "run_simulation"
Cohesion: 0.16
Nodes (17): IO, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, run_loop(), close_input(), Any, DecisionSource, InterruptHook, IO (+9 more)

### Community 10 - "ActionPayload"
Cohesion: 0.10
Nodes (30): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated., FLR-005: Mass sends (>5 recipients) must require human approval (ASK). (+22 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.16
Nodes (21): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize, One claim as the parser hands it over: a class of mail, and the words that said… (+13 more)

### Community 12 - "ChatRunner"
Cohesion: 0.06
Nodes (37): Walk both lanes with nobody at the keyboard, and score what they did. Input is…, run_two_lanes(), Decision, What the simulator does with one arrival., Whether this route has to wait for the user., A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first. (+29 more)

### Community 13 - "hybrid"
Cohesion: 0.06
Nodes (37): Exception, _answer(), JevAnswer, JevError, _post(), Any, RuntimeError, Jev could not answer. The caller decides what a missing routing opinion means. (+29 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "sandbox.py"
Cohesion: 0.07
Nodes (32): as_dict(), charts(), _learning_section(), main(), _markdown(), Path, _rate(), A live mailbox: fresh mail every run, through the real pipeline, judged from… (+24 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.11
Nodes (37): _by_id(), The arrivals one record decided, in the order it decided them., What the run did, in the order a reader wants it., render(), Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, The whole environment on stand-ins: no key, no network, no judge., Each half decides exactly the arrivals it was given, and nothing goes missing. (+29 more)

### Community 17 - "HeldOutReport"
Cohesion: 0.20
Nodes (7): Gate, HeldOutReport, _rate(), A count and its denominator, which is the only honest way to print a rate., A hard gate: a number that has to hold, not a curve that has to trend., The sealed lane: the only place accuracy is measured, and the hard gates., The plan's hard gates, each stated with the count and its denominator. An empty…

### Community 18 - "loop_run"
Cohesion: 0.19
Nodes (19): ClaimStore, DecisionSource, LoopReport, Namespace, _keep_rules(), loop_run(), _open_store(), _policy() (+11 more)

### Community 19 - "runner.py"
Cohesion: 0.13
Nodes (37): asyncio, collections_abc, dataclasses, enum, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The four reference cases, run end to end and printed as transcripts. Each case…, The evaluation run: teach the learning lane, freeze it, score the sealed lane…, hashlib (+29 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.07
Nodes (42): build_provider(), parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch, parametrize (+34 more)

### Community 21 - "Proposal"
Cohesion: 0.10
Nodes (28): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule(), Proposal (+20 more)

### Community 22 - "VetoLevel"
Cohesion: 0.11
Nodes (25): ActionClass, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_permanent_deletion(), _eval_plan_deviation(), _eval_unknown_tool() (+17 more)

### Community 23 - "Route"
Cohesion: 0.15
Nodes (30): The four autonomy outcomes a candidate action can be routed to.…, Route, mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+22 more)

### Community 24 - "Effect"
Cohesion: 0.16
Nodes (12): ArchiveEmail, Draft, _email_id(), LabelEmail, Any, Files a message out of the inbox., A private draft. Preparation, not sending., Read-only: returns the message it was pointed at. (+4 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.15
Nodes (29): DraftCode, StrEnum, Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the…, source_text(), validate_draft(), case() (+21 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (11): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+3 more)

### Community 27 - "ProposalError"
Cohesion: 0.13
Nodes (15): ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Jev, proposing_provider(), The route question, asked over HTTP and metered like every other call., The proposer one name asks for: an endpoint, or an endpoint with Jev routing…, The hybrid, as a run selects it: Jev in front of whatever provider it was given. (+7 more)

### Community 28 - "_claim_from_record"
Cohesion: 0.13
Nodes (11): _claim_from_record(), _claim_record(), Any, datetime, Path, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''. (+3 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "injection.py"
Cohesion: 0.15
Nodes (14): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, _names_its_own_domain(), Prompt injection tripwires and plan-deviation verification. Zero LLM dependence… (+6 more)

### Community 31 - "drafts.py"
Cohesion: 0.12
Nodes (21): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Picked, Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, One example that fits the budget, and why it was the one kept. (+13 more)

### Community 32 - "stranger_mail"
Cohesion: 0.20
Nodes (10): A mail whose sender the mailbox cannot vouch for., Mailbox housekeeping commissioned by a stranger is the same shape, subject…, Please reply with the numbers' from a colleague is a request, and is left alone., A spoofed invoice is refused on the mail, however reversible the proposed…, A credential harvest is refused on the mail, not on whatever action was…, stranger_mail(), test_a_credential_named_by_a_stranger_fences_a_harmless_action(), test_a_strangers_system_housekeeping_fences_too() (+2 more)

### Community 33 - "Drafting"
Cohesion: 0.12
Nodes (17): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), A reply the user cannot trust is worse than a mail handed back., One of the three fixture cases whose route is an ask with a predraft., An ask that arrives with nothing prepared is the gap this phase closes., The answer belongs to the user, so the draft quotes the ask and marks the gap. (+9 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.13
Nodes (28): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, FeedbackKind, What the user did after seeing a decision. Values are the dataset's…, feedback(), Never tell me about these" is a never in the user's words and a yes in effect. (+20 more)

### Community 36 - "SeededClock"
Cohesion: 0.08
Nodes (22): EventStream, _json_default(), Any, datetime, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time. (+14 more)

### Community 37 - "test_events.py"
Cohesion: 0.05
Nodes (57): is_approving(), Whether this reading is a vote for the agent acting on its own., Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, DuplicateEventError, EventValidationError, FeedbackEvent (+49 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Session"
Cohesion: 0.13
Nodes (20): importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Called while a decision is on screen and before its line is read., Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one… (+12 more)

### Community 41 - "SimulatedMailbox"
Cohesion: 0.13
Nodes (10): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, Crash, Crashing, parametrize, RuntimeError, The plan's crash matrix: whether the work ran or not, a resume applies it once., A run that dies where it stands. (+2 more)

### Community 42 - "run_scenario"
Cohesion: 0.09
Nodes (20): main(), Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it…, One canonical run: the pipeline's own output, plus what it decided and…, What the router considered, which every canonical run keeps. (+12 more)

### Community 43 - "Claim"
Cohesion: 0.16
Nodes (12): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, _action_words(), _bears_on(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The claims in force that bear on one mail, narrowest first. A claim with no… (+4 more)

### Community 44 - "schedule"
Cohesion: 0.13
Nodes (24): _dependencies_first(), dependencies_of(), Any, The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., Keep the drawn order, moving a case after anything it says it waits for.…, release_order() (+16 more)

### Community 45 - "test_sim.py"
Cohesion: 0.05
Nodes (78): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, first_interrupt_of() (+70 more)

### Community 46 - "drafting_for"
Cohesion: 0.17
Nodes (12): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+4 more)

### Community 47 - "SplitViolation"
Cohesion: 0.14
Nodes (10): RuntimeError, Raised when code reaches across the learning/held-out firewall., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner., Refuse a learner write from a lane that is not allowed to teach., SplitViolation, The separation is symmetric: a lane view only sees its own rows., Held-out and development code cannot update the learner. (+2 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.23
Nodes (15): approval_for(), The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The effect log is what makes a retry safe: a second commit returns the same…, The yes a reviewer would send back for the work they were shown., session(), test_a_crash_before_the_work_ran_leaves_the_decision_waiting(), test_a_decision_that_moved_between_asking_and_answering_is_refused() (+7 more)

### Community 49 - "retrieve_style"
Cohesion: 0.18
Nodes (19): estimate_tokens(), A rough token count for a budget decision, not for a bill., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from., One sent reply, from the mailbox's own history., A reply the user sent this person beats an older one to anybody else. (+11 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Lane"
Cohesion: 0.06
Nodes (52): main(), Run the lanes, then print what they cost., main(), Run both lanes and print the report, so the scorer can be read before it is…, one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, main(), The eval run as a command, for anyone who would rather not go through the CLI. (+44 more)

### Community 52 - "run_graph"
Cohesion: 0.21
Nodes (14): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+6 more)

### Community 53 - "safety/__init__.py"
Cohesion: 0.09
Nodes (24): classify_action(), _eval_money_movement(), _extract_recipients(), FloorRule, _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any (+16 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.11
Nodes (15): Ledger, _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured. (+7 more)

### Community 55 - "Block"
Cohesion: 0.20
Nodes (7): Block, classify(), Any, Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 56 - "ScopeAnchor"
Cohesion: 0.11
Nodes (35): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means. (+27 more)

### Community 57 - "run_sandbox"
Cohesion: 0.13
Nodes (23): _banner(), _blocks(), _case_blocks(), _control_pass(), _judge_run(), _preview(), GraphSession, IO (+15 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "test_floor.py"
Cohesion: 0.09
Nodes (26): Scan untrusted email content and headers for prompt injection indicators.…, scan(), Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles. (+18 more)

### Community 60 - ".prepare"
Cohesion: 0.14
Nodes (15): _brief(), _digest(), _notify_text(), _params_brief(), Any, Work out the steps for a decision, validating every one, mutating nothing., A step that validated, or a recorded complaint about why it could not., Every step carries the ids, so one receipt can name the case it came from. (+7 more)

### Community 61 - "graph.py"
Cohesion: 0.05
Nodes (55): langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, Message, One email message, in a thread, in one direction., GraphOutcome, The decision graph: one arrival walked from ingest to receipt, checkpointed per… (+47 more)

### Community 62 - "ModelUser"
Cohesion: 0.18
Nodes (13): Decision, ModelUser, _note(), FeedbackContext, Message, The person whose mailbox this is, played by a model that is not the proposer.…, The preference this mail's class calls for, said once and not repeated., What the reply parser may look at: the mail and the decision, never a label. (+5 more)

### Community 63 - "test_triage.py"
Cohesion: 0.13
Nodes (19): amount_in(), The largest amount mentioned in a text, as a float., guesses(), manifest(), message(), fixture, Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request. (+11 more)

### Community 64 - "ClaimScope"
Cohesion: 0.17
Nodes (9): Keep the refusal, with the scope the rule was confirmed for rather than this…, claim_id_for(), ClaimScope, A stable id for the same claim said twice, so it is never stored twice., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., Protected attributes are out of memory by construction, not by a filter: the… (+1 more)

### Community 65 - "build_parser"
Cohesion: 0.16
Nodes (14): ArgumentParser, build_parser(), _default_provider(), The provider a run proposes with when the flag is absent. Read here rather than…, The provider the sandbox proposes with when the flag is absent. The sandbox…, The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags() (+6 more)

### Community 66 - "test_denominators.py"
Cohesion: 0.08
Nodes (40): ask_curve(), Block, calibration_report(), dispositions(), LaneRecord, RuntimeError, The two-lane scorer: what the agent did, counted where it happened. The report…, The interruption curve: how many cases each block of the lane needed the user… (+32 more)

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (63): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+55 more)

### Community 68 - "_background_loop"
Cohesion: 0.29
Nodes (5): AbstractEventLoop, _background_loop(), Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 69 - "main"
Cohesion: 0.20
Nodes (10): data_validate(), main(), Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard., Print what a case set holds and everything wrong with it., Entry point for the ``wajo`` console script., sandbox_run_command(), CaptureFixture, MonkeyPatch (+2 more)

### Community 70 - "evaluate"
Cohesion: 0.18
Nodes (11): evaluate(), _frozen(), Any, Path, Teach, freeze, and score the sealed lane exactly once., Freeze the learned state, turning the writer's ValueError into a scoring…, The async driver, run to completion., The transcript: what the user says, at the decisions they say it at. (+3 more)

### Community 71 - "test_a_strangers_instructions_fence_every_route_whatever_the_action"
Cohesion: 0.22
Nodes (9): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., The mail fences, not the proposed action: a harmless label still collapses to…, test_a_strangers_instructions_fence_every_route_whatever_the_action(), test_benign_workplace_clean_pass(), test_classify_action_matrix() (+1 more)

### Community 72 - "test_replay.py"
Cohesion: 0.05
Nodes (43): Replay events through a fresh seeded stream., replay(), manifest(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival. (+35 more)

### Community 73 - "Router"
Cohesion: 0.07
Nodes (53): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to. (+45 more)

### Community 74 - "TraceSink"
Cohesion: 0.08
Nodes (32): _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file., A stand-in a trace can carry: the digest, the size, and what kind of thing it… (+24 more)

### Community 75 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 76 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 77 - "Any"
Cohesion: 0.15
Nodes (11): Arrival, Any, One generated mail, with the brief and the writer's own opinion that produced…, The mail in the loader's own shape. It carries no labels, because it has none., What the run keeps beside the row: which brief wrote it, and what it expected., A plain-text caller for one model role, or a named failure when it has no…, The runner's interrupt hook: the waiting decision gets its lines from the model., The arrivals of the half the agent had never seen, in delivery order. (+3 more)

### Community 78 - "ProposalRequest"
Cohesion: 0.09
Nodes (17): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, JevRouted, Jev decides how much autonomy the mail gets; the model decides what the work…, The pair's name, so a run says where a proposal could have come from. (+9 more)

### Community 79 - "SandboxError"
Cohesion: 0.24
Nodes (6): RuntimeError, Raised when the environment cannot be built or read., SandboxError, FakeModel, One stand-in for the endpoint: it writes mail, answers as the owner, and…, Answer whichever question the prompt asks, in the role whose stage it is.

### Community 80 - "test_loop.py"
Cohesion: 0.22
Nodes (15): asked(), _drained(), loop(), Queue, A named case still waits for the second line, so an unanswered echo stores…, Nothing hangs on a prompt the script never feeds: it is told a line that does…, test_a_decision_the_script_does_not_answer_is_passed_on(), test_a_named_entry_is_typed_at_the_case_it_names() (+7 more)

### Community 81 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 83 - "held_out_report"
Cohesion: 0.10
Nodes (37): held_out_report(), Score the sealed lane, refusing outright if anything about it could teach. Both…, _decision(), _gold(), The denominator is the run's own count, so a partial record cannot be scored., Route accuracy's denominator is every graded case, not the ones that matched., A case whose answer is a handoff has no action to match, so it is not graded as…, A lane that may write learner state is not held out, whatever it is called. (+29 more)

### Community 87 - "autonomy/state.py"
Cohesion: 0.10
Nodes (22): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+14 more)

### Community 88 - "test_loss_matrix.py"
Cohesion: 0.16
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "Predraft"
Cohesion: 0.33
Nodes (4): Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., The draft this ask shows, or None when it shows none.

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
Cohesion: 0.17
Nodes (9): Judge, _judged(), Judgement, One judged case: the score, then the judge's own reason for it., One external opinion, with the reason it gave., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI. (+1 more)

### Community 108 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 109 - "pytest"
Cohesion: 0.23
Nodes (12): pytest, message(), Not just the serde: a compiled graph through a saver hands back the same values., The allowlist is the schema: a new field is traceable, not silently dropped., The body and subject are inputs to the decision, and must not reach the file., One decision as a producer would build it: ids, digests and bounded records., What the checkpointer serialises is what it reads back, unchanged., state() (+4 more)

### Community 111 - "write_mailbox"
Cohesion: 0.16
Nodes (13): generator_prompt(), parse_generated(), Route, One situation to write a mail about, and how a careful assistant would treat it., The request for one arrival. Everything fresh about it comes from this frame., Read one generated mail, naming what is wrong rather than guessing a field., Write `count` fresh arrivals, walking the briefs in a shuffled order. Every…, How many arrivals took each of the four routes. (+5 more)

### Community 112 - "EmailContext"
Cohesion: 0.17
Nodes (12): EmailContext, Email metadata and body context passed into safety evaluations.…, FLR-001: Money requests in email body cannot trigger non-reversible actions., Load tests/adversarial_cases.yaml and verify 100% are vetoed with ESCALATE., An injection tripwire collapses the arm set to ESCALATE before learning runs., floor_check must read the domain carried by the email, not a fixed default., An honest vendor signing as its own security team must not be vetoed., test_a_vendor_naming_its_own_domain_is_not_an_authority_spoof() (+4 more)

### Community 114 - "cli.py"
Cohesion: 0.24
Nodes (10): graph_run(), _proposing(), GraphSession, Command-line entry point. ``wajo sim run`` replays a fixture as a chat:…, Say what the reader is looking at, since labels change the calibration., The pipeline's proposer: a rule already confirmed answers before the provider…, Walk a fixture through the decision graph and say what each arrival ended in., Answer one held decision with a yes and say what that committed. (+2 more)

### Community 115 - "ToolError"
Cohesion: 0.20
Nodes (8): A send that validates like a real one and never leaves the mailbox. Recipients…, SendEmail, ValueError, One tool by name, or a refusal naming what does exist., Raised when a tool is asked for something it cannot do., Raised when a step names a tool the registry does not hold., ToolError, UnknownTool

### Community 116 - "Tool"
Cohesion: 0.20
Nodes (7): ABC, CreateDraft, Writes a private draft. Reversible, and never a send., One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit., Tool

### Community 117 - "RememberedProvider"
Cohesion: 0.09
Nodes (21): Protocol, _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., The user's own words, consulted before the provider. Wraps another provider:…, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered. (+13 more)

### Community 118 - "test_eval_run.py"
Cohesion: 0.21
Nodes (16): load_script(), Read a transcript, naming what is wrong with it rather than failing on a…, evaluate(), mini_manifest(), mini_script(), Path, The eval run: teach the learning lane, freeze it, then score the sealed lane…, The first few committed rows of one split, so the test runs on the real case… (+8 more)

### Community 119 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 120 - "offline_provider"
Cohesion: 0.33
Nodes (5): offline_provider(), fixture, MonkeyPatch, Environment the suite runs under. ``main`` loads .env so a command can be run…, Every test proposes from the offline rules unless it asks for something else.

### Community 121 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 122 - "GraphError"
Cohesion: 0.33
Nodes (7): _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still…, The graph cannot continue, naming the case it stopped on.

### Community 123 - "server.py"
Cohesion: 0.22
Nodes (9): argparse, dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, ThreadingHTTPServer (+1 more)

### Community 124 - "Style"
Cohesion: 0.33
Nodes (4): What style the draft may borrow, and how the archive was narrowed to it., What the kept examples cost, in the same rough unit as the cap., One line naming what was kept and why, for a transcript., Style

### Community 125 - "_context"
Cohesion: 0.40
Nodes (5): _context(), FeedbackContext, The decision a standing preference is stated in front of., The card is only worth having if the pipeline's own parser reads it as a rule.…, test_every_standing_preference_the_owner_states_is_readable_as_a_rule()

### Community 126 - "CalibrationReport"
Cohesion: 0.22
Nodes (7): CalibrationReport, The lane the user sat in front of: what they typed, and what it cost them., Lines the user typed: answers to a prompt, and corrections after one., EvalOutcome, The run's report and the files it wrote, so a caller can print or extend them., What the run did, in the order a reader wants it: provenance, then the numbers., render()

### Community 130 - "EvalReport"
Cohesion: 0.15
Nodes (7): Disposition, EvalReport, Path, Both lanes, kept apart: one disposition count over everything, two assessments., How a lane's cases were handled, mutually exclusive by construction., Write the report as JSON, naming the file in the error rather than failing mute., The counts, then the denominator they have to add up to.

### Community 131 - "test_cli_replays_the_fixture"
Cohesion: 0.28
Nodes (9): CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., test_a_broken_input_stream_ends_the_run_instead_of_hanging(), test_buffered_input_is_recorded_as_corrections_not_answers(), test_cli_replays_the_fixture(), test_cli_seed_flag_changes_the_replay_digest() (+1 more)

### Community 132 - "RuleProvider"
Cohesion: 0.29
Nodes (7): The offline provider: proposes from triage, no network, deterministic. It is a…, RuleProvider, The noun decides: 'the Redis sharding key' is a field, and escalating it is…, test_a_key_that_names_a_data_structure_is_not_a_credential(), test_the_rule_provider_never_proposes_an_action_with_an_escalation(), A gateway that keeps what the provider was allowed to see., Recording

### Community 133 - "ScriptedReplies"
Cohesion: 0.25
Nodes (5): InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., ScriptedReplies

### Community 134 - "SafetyCounts"
Cohesion: 0.29
Nodes (3): Any, The two numbers that say nothing unsafe ran, counted from the run's own…, SafetyCounts

### Community 135 - "_provider_for"
Cohesion: 0.29
Nodes (7): eval_all(), _provider_for(), The proposer one name asks for: an endpoint, or an endpoint with Jev routing it., Teach the calibration lane, freeze it, and score the sealed lane once., The hybrid is a name, not four flags: `<endpoint>+jev`., test_one_name_selects_the_whole_proposer(), test_the_provider_a_command_uses_can_come_from_the_environment()

### Community 136 - "NotifyUser"
Cohesion: 0.29
Nodes (4): Notification, NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A message to the user's own assistant, never to anyone else.

### Community 138 - "ScheduleError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a case names a dependency no window can deliver before it., ScheduleError

## Knowledge Gaps
- **35 isolated node(s):** `the short version`, `the four states, in plain words`, `run a — 15 arrivals, 7 to learn on, 7 cold`, `run b — 40 arrivals, 20 to learn on, 19 cold`, `run a vs run b` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `Case`, `registry.py`, `RuleProvider`, `ProposalGateway`, `feedback.py`, `dataset.py`, `ActionPayload`, `test_claim_schema.py`, `ChatRunner`, `hybrid`, `runner.py`, `test_gateway.py`, `Proposal`, `VetoLevel`, `_claim_from_record`, `stranger_mail`, `Drafting`, `Learner`, `test_events.py`, `Session`, `run_scenario`, `Claim`, `test_sim.py`, `Lane`, `safety/__init__.py`, `ScopeAnchor`, `test_floor.py`, `.prepare`, `graph.py`, `ClaimScope`, `test_denominators.py`, `test_cases.py`, `test_a_strangers_instructions_fence_every_route_whatever_the_action`, `Router`, `ProposalRequest`, `test_freeze.py`, `held_out_report`, `test_loss_matrix.py`, `pytest`, `EmailContext`, `RememberedProvider`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `Case`, `test_denominators.py`, `Learner`, `ClaimStore`, `ProposalGateway`, `_background_loop`, `Transcript`, `AnswerQueue`, `ChatRunner`, `Handler`, `set_session`, `runner.py`, `Lane`, `RememberedProvider`, `Block`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `ProposalGateway` connect `ProposalGateway` to `GraphSession`, `Case`, `GraphRuntime`, `RuleProvider`, `run_simulation`, `ChatRunner`, `runner.py`, `test_gateway.py`, `Proposal`, `ProposalError`, `Session`, `run_scenario`, `Lane`, `run_graph`, `OpenAICompatibleProvider`, `run_sandbox`, `graph.py`, `evaluate`, `Router`, `ProposalRequest`, `held_out_report`, `cli.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 154 inferred relationships involving `Route` (e.g. with `dispositions()` and `held_out_report()`) actually correct?**
  _`Route` has 154 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `Lane` (e.g. with `main()` and `CalibrationReport`) actually correct?**
  _`Lane` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 33 INFERRED edges - model-reasoned connections that need verification._