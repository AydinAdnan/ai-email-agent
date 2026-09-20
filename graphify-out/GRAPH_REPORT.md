# Graph Report - ai-email-agent  (2026-09-20)

## Corpus Check
- 101 files · ~115,423 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2830 nodes · 7093 edges · 153 communities (127 shown, 26 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1013 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9af868d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_floor.py
- SafetyVerdict
- GraphRuntime
- graph.py
- ClaimStore
- message
- feedback.py
- Case
- Bucket
- SimOutcome
- ActionPayload
- test_claim_schema.py
- ChatRunner
- _answer
- Handler
- SandboxOutcome
- test_sandbox.py
- CalibrationReport
- loop_run
- runner.py
- ProposalGateway
- persona_demanded_route
- floor.py
- test_sim_tools.py
- Effect
- validate_draft
- .render
- test_gateway.py
- run_sandbox
- app.js
- named_route
- drafts.py
- test_jev.py
- test_predrafts.py
- Posterior
- Learner
- SeededClock
- test_events.py
- mask_for_llm
- PresidioMasker
- Session
- EmailEvent
- run_scenario
- Claim
- evaluate
- test_sim.py
- SentExample
- GraphSession
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- run_graph
- RememberedProvider
- OpenAICompatibleProvider
- JevRouted
- ScopeAnchor
- Any
- EffectLog
- injection.py
- _claim_from_record
- Routing
- ModelUser
- schedule
- Block
- cli.py
- Block
- test_cases.py
- eval_all
- main
- Cutoffs
- test_loss_matrix.py
- test_replay.py
- Route
- ToolError
- ContextPhoneRecognizer
- Tool
- sandbox.py
- ProposalProvider
- Jev
- test_loop.py
- test_freeze.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- thaw
- test_triage.py
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
- run_simulation
- Validation
- write_report
- BetaStore
- GraphSession
- LaneRecord
- LaneView
- ScopeAnchor
- SimulatedMailbox
- test_eval_run.py
- get_token_map
- ValueError
- Triage
- RuleProvider
- SimpleNamespace
- parametrize
- fixture
- TraceSink
- Queue
- Random
- DecisionSource
- Disposition
- EvalReport
- .start
- server.py
- ScriptedReplies
- ClaimStore
- graph_run
- GraphError
- Message
- pytest
- _server
- ClaimScope
- test_a_provider_that_crashes_fails_closed_without_killing_the_run
- test_every_standing_preference_the_owner_states_is_readable_as_a_rule
- ._run
- FeedbackContext
- Reading
- FeedbackContext
- render
- dependencies_of
- SimError
- reply
- Exception

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
- `test_an_external_send_is_never_silent_or_notified()` --uses--> `ActionPayload`  [INFERRED]
  tests/test_floor_protection.py → src/agent/safety/floor.py
- `test_a_credential_named_by_a_stranger_fences_a_harmless_action()` --uses--> `ActionPayload`  [INFERRED]
  tests/test_floor.py → src/agent/safety/floor.py
- `test_a_local_notification_keeps_the_notify_route()` --uses--> `ActionPayload`  [INFERRED]
  tests/test_floor.py → src/agent/safety/floor.py
- `test_a_strangers_instructions_fence_every_route_whatever_the_action()` --uses--> `ActionPayload`  [INFERRED]
  tests/test_floor.py → src/agent/safety/floor.py

## Import Cycles
- None detected.

## Communities (153 total, 26 thin omitted)

### Community 0 - "test_floor.py"
Cohesion: 0.05
Nodes (47): Scan untrusted email content and headers for prompt injection indicators.…, scan(), parametrize, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify that every tool and parameter boundary resolves to the exact ActionClass., Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters. (+39 more)

### Community 1 - "SafetyVerdict"
Cohesion: 0.20
Nodes (10): Immutable outcome of evaluating a proposed action against the safety floor., SafetyVerdict, The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), _decision(), A decided case carrying the floor's ballot, which is what violations are read…, Assert SafetyVerdict instances are frozen to prevent tampering., test_verdict_immutability() (+2 more)

### Community 2 - "GraphRuntime"
Cohesion: 0.09
Nodes (38): CompiledStateGraph, authorize(), _bound(), build_graph(), _case(), consent(), GraphRuntime, hold() (+30 more)

### Community 3 - "graph.py"
Cohesion: 0.05
Nodes (64): langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, GraphOutcome, The decision graph: one arrival walked from ingest to receipt, checkpointed per…, What a lane through the graph did., How many times a tool actually ran, counted from the receipts. (+56 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (45): _answered_cases(), IO, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Each arrival a rule answered, mapped to the arrival whose mail taught that rule., run_loop(), ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory. (+37 more)

### Community 5 - "message"
Cohesion: 0.10
Nodes (32): OpenAICompatibleProvider, SimpleNamespace, Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider() (+24 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (46): FeedbackKind, _action_for(), _claim_reading(), _clean_label(), confirm_claim(), confirm_words(), _decision_reading(), FeedbackContext (+38 more)

### Community 7 - "Case"
Cohesion: 0.11
Nodes (22): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., Every case in one lane, in sequence order., _persona_refused(), Proposal (+14 more)

### Community 8 - "Bucket"
Cohesion: 0.13
Nodes (11): The confirmed rule that refused this arm, or '' when the user has not refused…, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a…, The bucket a stored level key stands for, for reporting., The context a posterior is kept for: the mail's shape, and the work proposed. (+3 more)

### Community 9 - "SimOutcome"
Cohesion: 0.33
Nodes (4): What one simulator run did., Feedback a learner would accept, which is nothing until Commit 3.6., How many times a tool actually ran, counted from the receipts., SimOutcome

### Community 10 - "ActionPayload"
Cohesion: 0.07
Nodes (56): ActionPayload, EmailContext, _eval_injection_tripwires(), _eval_irreversible_external(), _eval_permanent_deletion(), _eval_plan_deviation(), _eval_unknown_tool(), floor_check() (+48 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.14
Nodes (23): ClaimError, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize, Protected attributes are out of memory by construction, not by a filter: the…, One claim as the parser hands it over: a class of mail, and the words that said… (+15 more)

### Community 12 - "ChatRunner"
Cohesion: 0.12
Nodes (17): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., The draft this ask shows, or None when it shows none., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew. (+9 more)

### Community 13 - "_answer"
Cohesion: 0.17
Nodes (14): _answer(), JevError, _post(), Any, Route, RuntimeError, Jev could not answer. The caller decides what a missing routing opinion means., Post one request, or hand it to the transport a test supplied. (+6 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (10): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., Hand a typed line to the run that is waiting for one. (+2 more)

### Community 15 - "SandboxOutcome"
Cohesion: 0.09
Nodes (18): _learning_section(), _markdown(), _rate(), Everything one sandbox run produced, in the shape the report and charts read., The route an arrival took, whichever half decided it., Arrivals the pipeline routed the way the brief (or the writer) said it should.…, Hostile arrivals, and how many of them escalated. The one graded property., The judge's mean score for one question, or None when it answered nothing. (+10 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.07
Nodes (47): _by_id(), RuntimeError, Raised when the environment cannot be built or read., The arrivals one record decided, in the order it decided them., SandboxError, FakeModel, Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its… (+39 more)

### Community 17 - "CalibrationReport"
Cohesion: 0.11
Nodes (13): CalibrationReport, Gate, HeldOutReport, _rate(), A count and its denominator, which is the only honest way to print a rate., The lane the user sat in front of: what they typed, and what it cost them., Lines the user typed: answers to a prompt, and corrections after one., A hard gate: a number that has to hold, not a curve that has to trend. (+5 more)

### Community 18 - "loop_run"
Cohesion: 0.18
Nodes (19): LoopReport, Namespace, data_validate(), _keep_rules(), loop_run(), _open_store(), IO, Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard. (+11 more)

### Community 19 - "runner.py"
Cohesion: 0.12
Nodes (32): asyncio, collections_abc, dataclasses, enum, The four reference cases, run end to end and printed as transcripts. Each case…, hashlib, json, os (+24 more)

### Community 20 - "ProposalGateway"
Cohesion: 0.14
Nodes (17): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., quiet_but_wrong(), A provider that would happily label suspicious mail and move on., The rules belong to the mail, so a model never gets to propose a quiet route…, A small model copies the example it was shown, so the example carries no value., No folder for this mail means a blocked step at the registry, not a made-up one., The floor wins over a confident proposal, which is the whole contract. (+9 more)

### Community 21 - "persona_demanded_route"
Cohesion: 0.13
Nodes (22): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), persona_rule(), Message, Route (+14 more)

### Community 22 - "floor.py"
Cohesion: 0.11
Nodes (27): ActionClass, classify_action(), _eval_credential_security(), _eval_mass_send(), _eval_money_movement(), _extract_recipients(), _has_credential_intent(), _has_financial_intent() (+19 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.16
Nodes (25): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+17 more)

### Community 24 - "Effect"
Cohesion: 0.14
Nodes (14): ArchiveEmail, CreateDraft, Draft, _email_id(), Notification, Any, Files a message out of the inbox., Writes a private draft. Reversible, and never a send. (+6 more)

### Community 25 - "validate_draft"
Cohesion: 0.13
Nodes (32): parametrize, DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the… (+24 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (11): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+3 more)

### Community 27 - "test_gateway.py"
Cohesion: 0.09
Nodes (34): build_provider(), parse_proposal(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Validate one provider answer. Anything unexpected is an error, not a default., Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client() (+26 more)

### Community 28 - "run_sandbox"
Cohesion: 0.08
Nodes (23): cost_dict(), Read a graph run, including the floor's ballot and who authorised each commit., The cost table as data, under the deflection rate that justifies the cheap…, record_from_graph(), CachingProvider, _control_pass(), ProposalCache, GraphSession (+15 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "named_route"
Cohesion: 0.32
Nodes (8): named_route(), The route the user's own rules name for this mail, if any. Two sources count: a…, case(), _hints(), An untrusted proposal is the thing the router tests, so it cannot buy silence., The memory layer answers from a claim, and that is a preference like the rules…, test_the_persona_names_the_route_a_model_may_not_exceed(), test_the_remembered_provider_names_the_users_own_route()

### Community 31 - "drafts.py"
Cohesion: 0.10
Nodes (29): Case, carried_instruction(), draft_reply(), drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+21 more)

### Community 32 - "test_jev.py"
Cohesion: 0.22
Nodes (20): answer(), FakeJev, hybrid(), message(), The Jev hybrid: Jev decides the route, the model does the work, the floor still…, A wrapped model, the model's own script, and the ledger both of them write into., Drive the wrapper the way the gateway does, and hand back what it answered., No work to prepare, so the text model is not called at all. (+12 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.12
Nodes (24): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, End to end through the real contract: prepare, authorize, commit one draft., A reply the user cannot trust is worse than a mail handed back. (+16 more)

### Community 34 - "Posterior"
Cohesion: 0.17
Nodes (7): Posterior, Random, One Thompson sample: the number an arm is compared with., One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback., What is believed about this bucket, through the chain when it has no history.

### Community 35 - "Learner"
Cohesion: 0.08
Nodes (44): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+36 more)

### Community 36 - "SeededClock"
Cohesion: 0.08
Nodes (21): EventStream, _json_default(), Any, datetime, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time. (+13 more)

### Community 37 - "test_events.py"
Cohesion: 0.06
Nodes (50): DuplicateEventError, EventValidationError, OutOfOrderEventError, ValueError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., Raised when a stream is not in ascending sequence order. (+42 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "Session"
Cohesion: 0.13
Nodes (21): Point the server at a session, which is what the tests and the page both need., set_session(), importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable… (+13 more)

### Community 41 - "EmailEvent"
Cohesion: 0.07
Nodes (39): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), ManifestError, _message(), Any, datetime (+31 more)

### Community 42 - "run_scenario"
Cohesion: 0.12
Nodes (17): main(), preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it… (+9 more)

### Community 43 - "Claim"
Cohesion: 0.10
Nodes (18): _action_words(), _bears_on(), Claim, _moment(), datetime, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The rules that have gone stale: in force, but nobody has restated them in a… (+10 more)

### Community 44 - "evaluate"
Cohesion: 0.22
Nodes (13): evaluate(), _frozen(), Any, LaneView, Path, ProposalProvider, TraceSink, Teach, freeze, and score the sealed lane exactly once. (+5 more)

### Community 45 - "test_sim.py"
Cohesion: 0.05
Nodes (84): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, Reconstruct one case's thread, bounded by the reply-tree caps., thread_tree_for(), arrivals(), block_of(), dataset_routes(), decision_sources() (+76 more)

### Community 46 - "SentExample"
Cohesion: 0.17
Nodes (12): examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over., The consented sent examples a case carries, if the mailbox offered any. Not the…, SentExample (+4 more)

### Community 47 - "GraphSession"
Cohesion: 0.18
Nodes (11): Command, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, Carry a thread past its interrupt, or past the point a crash cut it off at. (+3 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.11
Nodes (25): approval_for(), Crash, Crashing, Flaky, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide. (+17 more)

### Community 49 - "retrieve_style"
Cohesion: 0.14
Nodes (22): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., What the kept examples cost, in the same rough unit as the cap., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example() (+14 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.06
Nodes (34): main(), Run the lanes, then print what they cost., one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, LaneView, Manifest, RuntimeError, Raised when code reaches across the learning/held-out firewall. (+26 more)

### Community 52 - "run_graph"
Cohesion: 0.21
Nodes (14): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+6 more)

### Community 53 - "RememberedProvider"
Cohesion: 0.13
Nodes (15): Proposal, _domain(), proposal_from(), Message, ProposalProvider, ProposalRequest, What the user's own words amount to for this mail, if anything., The claim's route, with whatever work the inner provider chose for the mail. An… (+7 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (14): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+6 more)

### Community 55 - "JevRouted"
Cohesion: 0.19
Nodes (9): ProposalRequest, JevRouted, Jev decides how much autonomy the mail gets; the model decides what the work…, The pair's name, so a run says where a proposal could have come from., Whichever models answered, named the way a run names them., Compose one proposal: the route from Jev, the work from the model., The model's own answer, kept whole, with the reason it was needed named., One proposal in the schema the gateway parses, so the floor reads it like any… (+1 more)

### Community 56 - "ScopeAnchor"
Cohesion: 0.11
Nodes (33): datetime, ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to…, A person saying "promotions" names a class, and the class words are the ones… (+25 more)

### Community 57 - "Any"
Cohesion: 0.09
Nodes (20): Arrival, arrival_from_record(), as_dict(), load_mailbox(), Any, Route, The arrivals of the half the agent had never seen, in delivery order., How many arrivals took each of the four routes. (+12 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "injection.py"
Cohesion: 0.08
Nodes (26): base64, FloorRule, Representation of an audited, immutable safety floor rule., Safety module: floor guardrails, action taxonomy, and injection tripwires., _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate() (+18 more)

### Community 60 - "_claim_from_record"
Cohesion: 0.14
Nodes (13): Grant, _claim_from_record(), claim_id_for(), _claim_record(), Any, Path, Route, Take up the claims already in the store's file, when consent allows their use. (+5 more)

### Community 61 - "Routing"
Cohesion: 0.25
Nodes (5): What the router considered, which every canonical run keeps., The route chosen, and everything that was ruled out on the way., The chosen route's expected loss, in handoffs., One line for a transcript or a reason. Deliberately terse: a trace digests a…, Routing

### Community 62 - "ModelUser"
Cohesion: 0.18
Nodes (12): Decision, ModelUser, Message, The person whose mailbox this is, played by a model that is not the proposer.…, Keep the owner's answer for an arrival, the way the run will read it back., The preference this mail's class calls for, said once and not repeated., What the reply parser may look at: the mail and the decision, never a label., The lines to hand the waiting decision: the reply, and a confirmation if… (+4 more)

### Community 63 - "schedule"
Cohesion: 0.14
Nodes (23): _dependencies_first(), RuntimeError, Raised when a case names a dependency no window can deliver before it., Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them., Keep the drawn order, moving a case after anything it says it waits for.…, release_order(), schedule() (+15 more)

### Community 64 - "Block"
Cohesion: 0.22
Nodes (7): Block, classify(), Any, Append one block, with the number the page polls from., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 65 - "cli.py"
Cohesion: 0.20
Nodes (13): ArgumentParser, build_parser(), _default_provider(), Command-line entry point. ``wajo sim run`` replays a fixture as a chat:…, The provider a run proposes with when the flag is absent. Read here rather than…, The provider the sandbox proposes with when the flag is absent. The sandbox…, The flags both replay paths take: which mail, which lane, who proposes, a trace., Say what the reader is looking at, since labels change the calibration. (+5 more)

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (61): CaseReport, DatasetProblem, Path, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender… (+53 more)

### Community 68 - "eval_all"
Cohesion: 0.13
Nodes (16): DecisionSource, ProposalGateway, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., eval_all(), _policy(), _proposing(), _provider_for() (+8 more)

### Community 69 - "main"
Cohesion: 0.33
Nodes (6): main(), Entry point for the ``wajo`` console script., CaptureFixture, MonkeyPatch, test_the_cli_keeps_the_held_out_lane_shut(), test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in()

### Community 70 - "Cutoffs"
Cohesion: 0.15
Nodes (8): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore

### Community 71 - "test_loss_matrix.py"
Cohesion: 0.15
Nodes (22): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+14 more)

### Community 72 - "test_replay.py"
Cohesion: 0.05
Nodes (45): Replay events through a fresh seeded stream., replay(), manifest(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival. (+37 more)

### Community 73 - "Route"
Cohesion: 0.08
Nodes (59): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route, email_context_for() (+51 more)

### Community 74 - "ToolError"
Cohesion: 0.20
Nodes (7): NotifyUser, Tells the user what happened. Local to the assistant, so the floor treats it as…, A send that validates like a real one and never leaves the mailbox. Recipients…, SendEmail, ValueError, Raised when a tool is asked for something it cannot do., ToolError

### Community 75 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 76 - "Tool"
Cohesion: 0.10
Nodes (19): ABC, _brief(), _notify_text(), _params_brief(), Any, One capability. Small on purpose: check refuses, apply acts., Refuse parameters this tool cannot act on. Called at prepare time., Do the work and say what changed. Only ever called by a commit. (+11 more)

### Community 77 - "sandbox.py"
Cohesion: 0.09
Nodes (35): _banner(), _blocks(), _case_blocks(), drawn_briefs(), generator_prompt(), _judge_run(), _judged(), Judgement (+27 more)

### Community 78 - "ProposalProvider"
Cohesion: 0.11
Nodes (13): Ledger, Protocol, ProposalProvider, ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., A source of untrusted proposal text., Return raw proposal text for one request. (+5 more)

### Community 79 - "Jev"
Cohesion: 0.14
Nodes (13): Jev, proposing_provider(), ProposalProvider, The route question, asked over HTTP and metered like every other call., An endpoint and the recipe riding on it: ``openrouter+jev`` -> ``(openrouter,…, The proposer one name asks for: an endpoint, or an endpoint with Jev routing…, The hybrid, as a run selects it: Jev in front of whatever provider it was given., route_by_jev() (+5 more)

### Community 80 - "test_loop.py"
Cohesion: 0.18
Nodes (17): asked(), _drained(), loop(), Queue, A named case still waits for the second line, so an unanswered echo stores…, Nothing hangs on a prompt the script never feeds: it is told a line that does…, Calibrating on the same mail twice asks once: the rule answers the second time., test_a_decision_the_script_does_not_answer_is_passed_on() (+9 more)

### Community 81 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 83 - "Lane"
Cohesion: 0.05
Nodes (84): argparse, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, ask_curve(), calibration_report(), dispositions(), git_sha(), held_out_report(), LaneRecord (+76 more)

### Community 87 - "thaw"
Cohesion: 0.21
Nodes (13): _entries(), freeze(), load(), Any, Path, Write the frozen state, naming the file in the failure rather than raising…, Read a frozen state back, or say what about it could not be read., Everything a run earned, as a JSON-serializable payload. (+5 more)

### Community 88 - "test_triage.py"
Cohesion: 0.11
Nodes (23): fixture, amount_in(), The largest amount mentioned in a text, as a float., guesses(), manifest(), message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request. (+15 more)

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
Cohesion: 0.14
Nodes (13): 1. The console, verbatim, 2. The four states, and what each one actually does, 3. How well it did, on the half it had never seen, 4. Arrival by arrival, against the ground truth, 5. The decision the teaching changed, 6. Before and after - what was broken and what the fixes did, 7. What this run cannot tell you, 8. Charts (+5 more)

### Community 107 - "Judge"
Cohesion: 0.25
Nodes (5): Judge, Ask one question about one case. A judge that fails says so and scores nothing., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI.

### Community 108 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 109 - "run_simulation"
Cohesion: 0.06
Nodes (45): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+37 more)

### Community 111 - "write_report"
Cohesion: 0.13
Nodes (17): charts(), _digest(), main(), Path, Keep a run's transcript, naming the file in the error rather than failing mute., The hash of a file the run produced, so an artifact names what it was made from., Keep the mailbox itself, so a report can be read next to the mail that produced…, The three pictures: what it decided, how often it asked, and how it matched. (+9 more)

### Community 112 - "BetaStore"
Cohesion: 0.22
Nodes (12): BetaStore, Per-context Beta posteriors, resolved through a backoff chain. Every level…, _draws(), A mail with no intent cannot be counted at, or read from, the intent level., test_a_bucket_missing_part_of_its_key_never_reads_a_level_it_cannot_be_keyed_by(), test_a_bucket_with_no_history_resolves_through_backoff_to_global_counts(), test_a_draw_is_a_sample_of_the_posterior_and_repeats_with_its_seed(), test_a_revert_is_a_weight_the_callers_decide_on() (+4 more)

### Community 117 - "SimulatedMailbox"
Cohesion: 0.20
Nodes (6): build_registry(), LabelEmail, Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., Applies one label to one message., SimulatedMailbox

### Community 118 - "test_eval_run.py"
Cohesion: 0.14
Nodes (22): load_script(), The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, ScriptedTeaching, Manifest, evaluate(), mini_manifest() (+14 more)

### Community 119 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 121 - "Triage"
Cohesion: 0.16
Nodes (14): _first_intent(), _machine_sender(), _marketing_sender(), Message, What can be said about a message before any model is called., The mailbox's own domain, taken from where the message was addressed., Infer intent and relationship class from the mail, deterministically., The intent this mail's words point at, with the sender's shape as the tiebreak.… (+6 more)

### Community 122 - "RuleProvider"
Cohesion: 0.18
Nodes (9): The offline provider: proposes from triage, no network, deterministic. It is a…, RuleProvider, The noun decides: 'the Redis sharding key' is a field, and escalating it is…, test_a_credential_request_escalates_even_from_inside(), test_a_key_that_names_a_data_structure_is_not_a_credential(), test_a_receipt_above_the_threshold_is_notified(), test_the_rule_provider_never_proposes_an_action_with_an_escalation(), A gateway that keeps what the provider was allowed to see. (+1 more)

### Community 130 - "Disposition"
Cohesion: 0.33
Nodes (3): Disposition, How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to.

### Community 131 - "EvalReport"
Cohesion: 0.16
Nodes (7): EvalReport, Any, Path, The two numbers that say nothing unsafe ran, counted from the run's own…, Both lanes, kept apart: one disposition count over everything, two assessments., Write the report as JSON, naming the file in the error rather than failing mute., SafetyCounts

### Community 132 - ".start"
Cohesion: 0.25
Nodes (5): AbstractEventLoop, _background_loop(), Load the lane and begin the run. A failure here is the caller's to report., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

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
Cohesion: 0.25
Nodes (9): _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still…, The graph cannot continue, naming the case it stopped on., Authorization (+1 more)

### Community 138 - "Message"
Cohesion: 0.09
Nodes (26): main(), LaneView, Walk both lanes with nobody at the keyboard, and score what they did. Input is…, Run both lanes and print the report, so the scorer can be read before it is…, run_two_lanes(), Message, One email message, in a thread, in one direction., _order_key() (+18 more)

### Community 139 - "pytest"
Cohesion: 0.29
Nodes (6): pytest, offline_provider(), fixture, MonkeyPatch, Environment the suite runs under. ``main`` loads .env so a command can be run…, Every test proposes from the offline rules unless it asks for something else.

### Community 140 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 142 - "test_a_provider_that_crashes_fails_closed_without_killing_the_run"
Cohesion: 0.40
Nodes (4): BrokenProvider, A provider that fails the way a network client does., A transport error is a failed proposal, not an exception out of the session., test_a_provider_that_crashes_fails_closed_without_killing_the_run()

### Community 143 - "test_every_standing_preference_the_owner_states_is_readable_as_a_rule"
Cohesion: 0.50
Nodes (4): _context(), The decision a standing preference is stated in front of., The card is only worth having if the pipeline's own parser reads it as a rule.…, test_every_standing_preference_the_owner_states_is_readable_as_a_rule()

### Community 145 - "._run"
Cohesion: 0.17
Nodes (5): AnswerQueue, Path, The line queue the run reads from, which is also what "waiting" means. The run…, The runner's output, collected as blocks instead of printed., Transcript

### Community 152 - "render"
Cohesion: 0.50
Nodes (4): main(), What the run did, in the order a reader wants it: provenance, then the numbers., The eval run as a command, for anyone who would rather not go through the CLI., render()

### Community 153 - "dependencies_of"
Cohesion: 0.50
Nodes (4): dependencies_of(), Any, The ids a case says must arrive before it, from…, _row_of()

### Community 157 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

## Knowledge Gaps
- **48 isolated node(s):** `1. The console, verbatim`, `2. The four states, and what each one actually does`, `The floor - learning cannot weaken it`, `Calibration - the half that teaches`, `Did the learning buy anything` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `test_floor.py`, `SafetyVerdict`, `GraphRuntime`, `graph.py`, `Case`, `GraphError`, `ActionPayload`, `test_claim_schema.py`, `ChatRunner`, `runner.py`, `ProposalGateway`, `floor.py`, `test_sim_tools.py`, `test_gateway.py`, `named_route`, `test_jev.py`, `test_predrafts.py`, `Learner`, `test_events.py`, `Session`, `run_scenario`, `Claim`, `test_sim.py`, `test_graph_resume.py`, `Manifest`, `injection.py`, `Routing`, `test_loss_matrix.py`, `Tool`, `test_freeze.py`, `Lane`, `RuleProvider`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `Block`, `Learner`, `ClaimStore`, `.start`, `Case`, `SimOutcome`, `ChatRunner`, `Handler`, `ProposalProvider`, `._run`, `runner.py`, `Lane`, `RememberedProvider`, `Manifest`, `ProposalGateway`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `LoopReport` connect `LoopReport` to `graph.py`, `Learner`, `ClaimStore`, `SimOutcome`, `Claim`, `test_loop.py`, `runner.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 137 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 137 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 29 INFERRED edges - model-reasoned connections that need verification._