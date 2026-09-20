# Graph Report - ai-email-agent  (2026-09-20)

## Corpus Check
- 102 files · ~112,222 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2828 nodes · 7090 edges · 137 communities (112 shown, 25 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1013 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `92931ffc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_triage.py
- policy.py
- graph.py
- registry.py
- ClaimStore
- Ledger
- feedback.py
- dataset.py
- Bucket
- run_simulation
- ActionPayload
- ClaimScope
- ChatRunner
- jev.py
- Handler
- sandbox.py
- test_sandbox.py
- CalibrationReport
- graph_run
- cli.py
- test_gateway.py
- gateway.py
- VetoLevel
- test_sim_tools.py
- email_tools.py
- validate_draft
- main
- ProposalError
- CachingProvider
- app.js
- Route
- drafts.py
- test_jev.py
- test_predrafts.py
- Posterior
- Learner
- SeededClock
- test_events.py
- mask_for_llm
- PresidioMasker
- session.py
- test_sim.py
- run_canonical.py
- Claim
- evaluate
- arrivals
- SentExample
- run_typed
- SimulatedMailbox
- retrieve_style
- Routes
- Manifest
- test_graph.py
- .claim_for
- OpenAICompatibleProvider
- JevRouted
- ScopeAnchor
- Any
- EffectLog
- floor.py
- classify_action
- runner.py
- ModelUser
- sim/__init__.py
- events.py
- build_parser
- ask_curve
- test_cases.py
- docs/DESIGN.md
- main
- interrupting_case_ids
- test_a_strangers_instructions_fence_every_route_whatever_the_action
- test_replay.py
- test_floor_protection.py
- .asked_in
- ContextPhoneRecognizer
- pytest
- write_mailbox
- ProposalRequest
- routing_request
- test_loop.py
- test_freeze.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- autonomy/state.py
- router.py
- ExplodingPolicy
- rules/graphify.md
- DESIGN.md
- README.md
- analysis.md — how the agent actually did
- Claim
- loop.py
- ManifestError
- Transcript 1 - a live mailbox, decided end to end
- Judge
- masker.py
- trace.py
- Validation
- SandboxError
- EmailEvent
- GraphSession
- LaneRecord
- LaneView
- ScopeAnchor
- dataclasses
- ScoringError
- get_token_map
- ValueError
- test_floor.py
- first_interrupt_of
- SimpleNamespace
- parametrize
- fixture
- TraceSink
- Queue
- Random
- DecisionSource
- Disposition
- ClaimStore
- reply_tree.py
- ClaimScope
- FeedbackContext
- Reading
- FeedbackContext

## God Nodes (most connected - your core abstractions)
1. `Route` - 164 edges
2. `Router` - 65 edges
3. `Lane` - 57 edges
4. `Learner` - 56 edges
5. `run_sandbox()` - 53 edges
6. `ClaimStore` - 52 edges
7. `ChatRunner` - 52 edges
8. `Manifest` - 46 edges
9. `Claim` - 45 edges
10. `ActionPayload` - 45 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `main()` --uses--> `ScoringError`  [INFERRED]
  src/agent/cli.py → evals/harness.py
- `test_a_record_that_decided_fewer_cases_than_it_processed_is_refused()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py
- `test_a_report_cannot_be_written_where_it_cannot_be_read()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py
- `test_a_route_the_report_does_not_know_is_refused_rather_than_counted()` --uses--> `ScoringError`  [INFERRED]
  tests/eval/test_denominators.py → evals/harness.py

## Import Cycles
- None detected.

## Communities (137 total, 25 thin omitted)

### Community 0 - "test_triage.py"
Cohesion: 0.13
Nodes (20): fixture, guesses(), manifest(), message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., A machine notice asks the reader nothing, so it is filed rather than answered.…, The other half of the same rule: a fault is something the reader has to know. (+12 more)

### Community 1 - "policy.py"
Cohesion: 0.11
Nodes (26): Protocol, Case, One dataset row: its lane, its canonical event, its labels and the raw record., Whether this case carries the dataset's answer at all., ProposalProvider, A source of untrusted proposal text., email_context_for(), GoldPolicy (+18 more)

### Community 2 - "graph.py"
Cohesion: 0.06
Nodes (57): Command, CompiledStateGraph, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _bound() (+49 more)

### Community 3 - "registry.py"
Cohesion: 0.07
Nodes (43): _authorized_settled(), Authorize from the state alone, so a decision approved before a crash still…, Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, _brief() (+35 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (41): enum, ProposalProvider, ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Capability, ConsentRequired, Grant (+33 more)

### Community 5 - "Ledger"
Cohesion: 0.07
Nodes (38): OpenAICompatibleProvider, SimpleNamespace, Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., Most-spending stage first, so the table reads as a ranking., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that…, A process's spend: every provider call, and every arrival it never had to ask… (+30 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (41): FeedbackKind, _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed() (+33 more)

### Community 7 - "dataset.py"
Cohesion: 0.09
Nodes (40): _attachment(), _case_from_mail_row(), _case_from_row(), DatasetProblem, event_from_row(), _message(), Any, datetime (+32 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (25): The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Random, Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "run_simulation"
Cohesion: 0.12
Nodes (23): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, What one simulator run did., How many times a tool actually ran, counted from the receipts. (+15 more)

### Community 10 - "ActionPayload"
Cohesion: 0.08
Nodes (43): ActionPayload, EmailContext, floor_check(), Standardized representation of a candidate tool action., Email metadata and body context passed into safety evaluations.…, Evaluate a proposed action against the deterministic safety floor. Returns the…, FLR-001: Financial transactions in action params must escalate., FLR-001: Money requests in email body cannot trigger non-reversible actions. (+35 more)

### Community 11 - "ClaimScope"
Cohesion: 0.13
Nodes (23): ClaimScope, Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., memory(), preference(), parametrize, Protected attributes are out of memory by construction, not by a filter: the… (+15 more)

### Community 12 - "ChatRunner"
Cohesion: 0.07
Nodes (35): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., The draft this ask shows, or None when it shows none., A reconstructed thread: its roots, plus every message's children by parent id.…, The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., ReplyTree (+27 more)

### Community 13 - "jev.py"
Cohesion: 0.08
Nodes (28): os, _answer(), JevAnswer, JevError, _post(), Any, Message, Route (+20 more)

### Community 14 - "Handler"
Cohesion: 0.16
Nodes (11): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., Point the server at a session, which is what the tests and the page both need., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent. (+3 more)

### Community 15 - "sandbox.py"
Cohesion: 0.07
Nodes (47): Count a run's floor violations and unauthorized commits. The floor's ballot is…, safety_counts(), as_dict(), _banner(), _blocks(), _control_pass(), _digest(), _judge_run() (+39 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.08
Nodes (45): dispositions(), Count routes into the three dispositions, refusing a route nobody defined., _by_id(), The arrivals one record decided, in the order it decided them., FakeModel, Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, One stand-in for the endpoint: it writes mail, answers as the owner, and… (+37 more)

### Community 17 - "CalibrationReport"
Cohesion: 0.07
Nodes (22): CalibrationReport, EvalReport, Gate, HeldOutReport, Any, Path, _rate(), A count and its denominator, which is the only honest way to print a rate. (+14 more)

### Community 18 - "graph_run"
Cohesion: 0.08
Nodes (42): DecisionSource, LoopReport, Namespace, ProposalGateway, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., data_validate(), eval_all() (+34 more)

### Community 19 - "cli.py"
Cohesion: 0.11
Nodes (28): argparse, asyncio, collections_abc, dotenv, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, cost_dict(), The two-lane scorer: what the agent did, counted where it happened. The report…, The cost table as data, under the deflection rate that justifies the cheap… (+20 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.08
Nodes (42): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., BrokenProvider, message(), parametrize, quiet_but_wrong(), The model proposal gateway: untrusted output, one repair, then fail closed., A provider that fails the way a network client does. (+34 more)

### Community 21 - "gateway.py"
Cohesion: 0.14
Nodes (24): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), _persona_refused(), persona_rule(), Proposal (+16 more)

### Community 22 - "VetoLevel"
Cohesion: 0.10
Nodes (28): ActionClass, _eval_credential_security(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion(), _eval_plan_deviation(), _eval_unknown_tool() (+20 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.13
Nodes (29): build_registry(), Every simulated tool, over one mailbox., mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose. (+21 more)

### Community 24 - "email_tools.py"
Cohesion: 0.09
Nodes (31): ABC, action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification (+23 more)

### Community 25 - "validate_draft"
Cohesion: 0.13
Nodes (32): parametrize, DraftCode, Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether this draft may be shown. Fixed order, and the first refusal is the… (+24 more)

### Community 26 - "main"
Cohesion: 0.25
Nodes (7): main(), Run the lanes, then print what they cost., _money(), _percent(), The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for.

### Community 27 - "ProposalError"
Cohesion: 0.13
Nodes (21): build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes…, Jev, proposing_provider(), ProposalProvider (+13 more)

### Community 28 - "CachingProvider"
Cohesion: 0.12
Nodes (10): CachingProvider, ProposalCache, ProposalProvider, ProposalRequest, Every answer the pipeline's model actually gave, keyed by the mail it answered.…, Keep the first answer for a mail: a repair attempt is not a second opinion., Read a recording back, naming the line that is unreadable., A provider that keeps every answer, against the mail id it answered. (+2 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "Route"
Cohesion: 0.12
Nodes (34): The route the run actually chose., The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+26 more)

### Community 31 - "drafts.py"
Cohesion: 0.10
Nodes (29): Case, carried_instruction(), draft_reply(), drafting_for(), FactSource, _first_name(), _flatten(), open_questions() (+21 more)

### Community 32 - "test_jev.py"
Cohesion: 0.16
Nodes (21): answer(), FakeJev, hybrid(), The Jev hybrid: Jev decides the route, the model does the work, the floor still…, A wrapped model, the model's own script, and the ledger both of them write into., Drive the wrapper the way the gateway does, and hand back what it answered., No work to prepare, so the text model is not called at all., The text model, answering from a script so nothing reaches a network. (+13 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (22): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+14 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.08
Nodes (41): is_approving(), Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Counts what the user said into posteriors, once per event, never from silence.… (+33 more)

### Community 36 - "SeededClock"
Cohesion: 0.08
Nodes (28): hashlib, EventStream, _json_default(), Any, datetime, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, A stable hash of the replay log., A deterministic clock. Time moves because the simulation says so. (+20 more)

### Community 37 - "test_events.py"
Cohesion: 0.10
Nodes (32): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _load_dataset(), parametrize, Unit tests for the canonical events (Phase 3.1). Covers: - Identity and… (+24 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.15
Nodes (17): mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory., Verify common PII entities (email, phone, person, location) are masked., Verify Indian PAN, Aadhaar, and Passport numbers are masked., Verify project codenames and ticket IDs are masked. (+9 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "session.py"
Cohesion: 0.05
Nodes (42): AbstractEventLoop, importlib_util, AnswerQueue, _background_loop(), Block, classify(), Path, One calibration run, driven a line at a time. The run is the one the CLI drives… (+34 more)

### Community 41 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, Reconstruct one case's thread, bounded by the reply-tree caps., thread_tree_for(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 42 - "run_canonical.py"
Cohesion: 0.16
Nodes (17): cold_control(), main(), The four reference cases, run end to end and printed as transcripts. Each case…, What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route. (+9 more)

### Community 43 - "Claim"
Cohesion: 0.07
Nodes (33): Grant, _action_words(), _bears_on(), Claim, _claim_from_record(), claim_id_for(), _claim_record(), ClaimError (+25 more)

### Community 44 - "evaluate"
Cohesion: 0.15
Nodes (17): git_sha(), provenance(), The commit the run came from, so an artifact can be traced to the code that…, What produced a report: the code, the versions and the models, not only the…, evaluate(), _frozen(), Any, LaneView (+9 more)

### Community 45 - "arrivals"
Cohesion: 0.17
Nodes (16): arrivals(), block_of(), labelled_routes(), The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., One arrival's text, from its header up to the next arrival., The eval curve is built from these two, so they have to be the run's own record., Only one of the two has something to release, so only one says approval. (+8 more)

### Community 46 - "SentExample"
Cohesion: 0.19
Nodes (10): examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over., The consented sent examples a case carries, if the mailbox offered any. Not the…, SentExample (+2 more)

### Community 47 - "run_typed"
Cohesion: 0.13
Nodes (15): decision_sources(), DecisionSource, Path, Which decision source produced the routes in a labelled run., Sender, subject and body are inputs in production; labels are only answers.…, On a real run: one line per arrival, and no mail text in any of them., Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines…, run_typed() (+7 more)

### Community 48 - "SimulatedMailbox"
Cohesion: 0.08
Nodes (25): Everything a commit can change, and nothing a prepare can., SimulatedMailbox, approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits. (+17 more)

### Community 49 - "retrieve_style"
Cohesion: 0.14
Nodes (22): estimate_tokens(), Picked, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., What the kept examples cost, in the same rough unit as the cap., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example() (+14 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.07
Nodes (33): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, LaneView, Manifest, Every case in the dataset, sorted by sequence index, with its digest.…, Load the manifest from a JSONL dataset file, or from plain mail rows., Return the lane-bound handle for one lane., Every case in one lane, in sequence order. (+25 more)

### Community 52 - "test_graph.py"
Cohesion: 0.28
Nodes (14): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+6 more)

### Community 53 - ".claim_for"
Cohesion: 0.19
Nodes (11): Proposal, _domain(), proposal_from(), Message, ProposalRequest, What the user's own words amount to for this mail, if anything., The claim's route, with whatever work the inner provider chose for the mail. An…, One claim as a proposal, or None when the claim names no route. (+3 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (14): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+6 more)

### Community 55 - "JevRouted"
Cohesion: 0.19
Nodes (9): ProposalRequest, JevRouted, Jev decides how much autonomy the mail gets; the model decides what the work…, The pair's name, so a run says where a proposal could have come from., Whichever models answered, named the way a run names them., Compose one proposal: the route from Jev, the work from the model., The model's own answer, kept whole, with the reason it was needed named., One proposal in the schema the gateway parses, so the floor reads it like any… (+1 more)

### Community 56 - "ScopeAnchor"
Cohesion: 0.09
Nodes (40): datetime, preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType (+32 more)

### Community 57 - "Any"
Cohesion: 0.13
Nodes (13): Arrival, _case_blocks(), _preview(), Any, The arrivals of the half the agent had never seen, in delivery order., The first of a mail's body, wrapped, for a log that has to stay skimmable., One block per arrival, in the order it was decided: the mail, the state, the…, One generated mail, with the brief and the writer's own opinion that produced… (+5 more)

### Community 58 - "EffectLog"
Cohesion: 0.22
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "floor.py"
Cohesion: 0.10
Nodes (28): base64, re, _eval_injection_tripwires(), FloorRule, Safety Floor — Pure-function deterministic guardrails. FLOOR_VERSION = "1.0"…, Representation of an audited, immutable safety floor rule., FLR-INJ-001: Prompt injection tripwires in email body or metadata must be…, The least autonomous of these routes, which is the one that wins a… (+20 more)

### Community 60 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 61 - "runner.py"
Cohesion: 0.13
Nodes (25): Record the route the router chose, which is what authorization checks., route(), Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).…, One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields(), message_digest(), _plain() (+17 more)

### Community 62 - "ModelUser"
Cohesion: 0.16
Nodes (13): Decision, ModelUser, Message, The person whose mailbox this is, played by a model that is not the proposer.…, Keep the owner's answer for an arrival, the way the run will read it back., The preference this mail's class calls for, said once and not repeated., What the reply parser may look at: the mail and the decision, never a label., The lines to hand the waiting decision: the reply, and a confirmation if… (+5 more)

### Community 63 - "sim/__init__.py"
Cohesion: 0.10
Nodes (32): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, _dependencies_first(), dependencies_of(), Any, RuntimeError, Windowed-random arrival scheduling (plan Commit 3.5). A lane replayed in…, Raised when a case names a dependency no window can deliver before it., One released window: its cases in delivery order, and the seed that ordered it. (+24 more)

### Community 64 - "events.py"
Cohesion: 0.16
Nodes (11): Attachment, DuplicateEventError, EventValidationError, ValueError, Canonical versioned events (Phase 3.1). SenderIdentity, Attachment, Message,…, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice. (+3 more)

### Community 65 - "build_parser"
Cohesion: 0.16
Nodes (14): ArgumentParser, build_parser(), _default_provider(), The provider a run proposes with when the flag is absent. Read here rather than…, The provider the sandbox proposes with when the flag is absent. The sandbox…, The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags() (+6 more)

### Community 66 - "ask_curve"
Cohesion: 0.33
Nodes (4): ask_curve(), Block, One block of a lane, in delivery order, and how much of it asked for the user., The interruption curve: how many cases each block of the lane needed the user…

### Community 67 - "test_cases.py"
Cohesion: 0.07
Nodes (53): CaseReport, Path, What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Check a case set's counts, enums and splits before anything is asked to run it.…, validate_cases(), _codes(), _extra() (+45 more)

### Community 68 - "docs/DESIGN.md"
Cohesion: 0.17
Nodes (10): Deliberately not built, Learning is posteriors plus scoped rules, One arrival, one route, and the route names the work, Replay and the split firewall, Scoring is expected loss in one unit, State and traces carry ids, never mail, The floor masks the ballot before anything is scored, The harness runs the real graph (+2 more)

### Community 69 - "main"
Cohesion: 0.15
Nodes (17): main(), Entry point for the ``wajo`` console script., CaptureFixture, MonkeyPatch, test_the_cli_keeps_the_held_out_lane_shut(), test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in(), CaptureFixture, MonkeyPatch (+9 more)

### Community 70 - "interrupting_case_ids"
Cohesion: 0.20
Nodes (10): dataset_routes(), interrupting_case_ids(), The dataset's route for each arrival, which only the label view prints., The plan's check, against the labels: only ask-first and escalate lines wait., The one error direction that matters: never act on mail the labels fence., Fixture cases whose gold route asks the user, in delivery order., test_a_correction_typed_at_a_prompt_binds_to_that_decision(), test_show_labels_reveals_the_decision_and_the_answer() (+2 more)

### Community 71 - "test_a_strangers_instructions_fence_every_route_whatever_the_action"
Cohesion: 0.22
Nodes (9): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., The mail fences, not the proposed action: a harmless label still collapses to…, test_a_strangers_instructions_fence_every_route_whatever_the_action(), test_benign_workplace_clean_pass(), test_classify_action_matrix() (+1 more)

### Community 72 - "test_replay.py"
Cohesion: 0.06
Nodes (36): Replay events through a fresh seeded stream., replay(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival., The log's order is the dataset's sequence order, not file order. (+28 more)

### Community 73 - "test_floor_protection.py"
Cohesion: 0.12
Nodes (34): floor_verdict_for(), Return the floor verdict, the dataset action id and the tool name it mapped to., approve(), ask_again(), bucket_for(), case(), feedback(), one_case_view() (+26 more)

### Community 74 - ".asked_in"
Cohesion: 0.25
Nodes (4): The arrivals a world asked the user about, in delivery order. ``taught`` is the…, Arrivals the control asked about that the taught run decided on its own., What the mailbox cost with no memory in front of the provider., Per class of mail: arrivals, asks with nothing remembered, asks after learning.…

### Community 75 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 76 - "pytest"
Cohesion: 0.29
Nodes (6): pytest, offline_provider(), fixture, MonkeyPatch, Environment the suite runs under. ``main`` loads .env so a command can be run…, Every test proposes from the offline rules unless it asks for something else.

### Community 77 - "write_mailbox"
Cohesion: 0.15
Nodes (17): drawn_briefs(), generator_prompt(), parse_generated(), How long a model call took, in the unit a reader cares about., One situation to write a mail about, and how a careful assistant would treat it., The brief a saved arrival says wrote it, or a named failure., The request for one arrival. Everything fresh about it comes from this frame., Read one generated mail, naming what is wrong rather than guessing a field. (+9 more)

### Community 78 - "ProposalRequest"
Cohesion: 0.13
Nodes (12): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., fake_client(), FakeCompletions, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request. (+4 more)

### Community 79 - "routing_request"
Cohesion: 0.50
Nodes (4): mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Everything the router may consider about one arrival, and nothing else., routing_request()

### Community 80 - "test_loop.py"
Cohesion: 0.18
Nodes (17): asked(), _drained(), loop(), Queue, A named case still waits for the second line, so an unanswered echo stores…, Nothing hangs on a prompt the script never feeds: it is told a line that does…, The learning claim, measured: one correction about a class, four quieter…, test_a_decision_the_script_does_not_answer_is_passed_on() (+9 more)

### Community 81 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 83 - "Lane"
Cohesion: 0.05
Nodes (75): calibration_report(), held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Refuse a record whose counts cannot add up to what the run processed., Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., Score the calibration lane: the dispositions, the typings and the ask curve. (+67 more)

### Community 87 - "autonomy/state.py"
Cohesion: 0.10
Nodes (23): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+15 more)

### Community 88 - "router.py"
Cohesion: 0.11
Nodes (27): What the router considered, which every canonical run keeps., Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of… (+19 more)

### Community 102 - "analysis.md — how the agent actually did"
Cohesion: 0.15
Nodes (12): analysis.md — how the agent actually did, how to reproduce, no LLM vs LLM only vs Jev + LLM, run a — 15 arrivals, 7 to learn on, 7 cold, run a vs run b, run b — 40 arrivals, 20 to learn on, 19 cold, the four states, in plain words, the short version (+4 more)

### Community 104 - "loop.py"
Cohesion: 0.07
Nodes (21): The user's own words, consulted before the provider. Wraps another provider:…, How many arrivals a confirmed claim answered., RememberedProvider, _answered_cases(), LoopReport, InterruptHook, IO, Queue (+13 more)

### Community 105 - "ManifestError"
Cohesion: 0.12
Nodes (15): CaseLabels, ManifestError, ValueError, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only., Build a manifest from plain mail: sender, recipients, subject and body. A…, Raised when the dataset itself violates the manifest schema., A bare KeyError says nothing about which of the cases is malformed. (+7 more)

### Community 106 - "Transcript 1 - a live mailbox, decided end to end"
Cohesion: 0.15
Nodes (12): 1. The console, verbatim, 2. The four states, and what each one actually does, 3. How well it did, on the half it had never seen, 4. Arrival by arrival, against the brief, 5. Analysis, 6. What this run cannot tell you, 7. Charts, Calibration — the half that teaches (+4 more)

### Community 107 - "Judge"
Cohesion: 0.25
Nodes (5): Judge, Ask one question about one case. A judge that fails says so and scores nothing., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI.

### Community 108 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 109 - "trace.py"
Cohesion: 0.07
Nodes (44): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them. (+36 more)

### Community 111 - "SandboxError"
Cohesion: 0.10
Nodes (21): arrival_from_record(), charts(), load_mailbox(), Path, Route, RuntimeError, How many arrivals took each of the four routes., Keep a run's transcript, naming the file in the error rather than failing mute. (+13 more)

### Community 112 - "EmailEvent"
Cohesion: 0.17
Nodes (8): The lane's arriving events, in sequence order., EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Every appended event, in arrival order., Record one arrival, or refuse it and leave the stream untouched. The whole…, The manifest hands out EmailEvents, not raw rows., test_events_are_canonical_events()

### Community 117 - "dataclasses"
Cohesion: 0.07
Nodes (30): dataclasses, Ledger, ProposalGateway, The offline provider: proposes from triage, no network, deterministic. It is a…, Turns provider text into a validated proposal, with one repair attempt., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, RuleProvider, amount_in() (+22 more)

### Community 118 - "ScoringError"
Cohesion: 0.12
Nodes (25): RuntimeError, Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, load_script(), The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, ScriptedTeaching (+17 more)

### Community 119 - "get_token_map"
Cohesion: 0.29
Nodes (7): get_token_map(), Access or initialize the singleton PresidioMasker., Retrieve the current token to original value map for a thread., The thread registry evicts the oldest entry instead of growing without limit., Verify unmask_text restores original values accurately., test_thread_registry_is_bounded(), test_unmasking()

### Community 121 - "test_floor.py"
Cohesion: 0.05
Nodes (40): Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify scan() catches direct instruction override attacks., Verify scan() catches prompt leakage and fake audit phishing., Verify scan() flags invisible zero-width unicode characters., Verify scan() decodes and flags embedded base64 commands., Verify scan() detects external senders claiming internal sensitive roles., An authority claim we cannot tie to a sender address is unresolved, not trusted., An in-org sender claiming an internal role is not an authority spoof. (+32 more)

### Community 122 - "first_interrupt_of"
Cohesion: 0.24
Nodes (10): first_interrupt_of(), gold_route(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing() (+2 more)

### Community 130 - "Disposition"
Cohesion: 0.15
Nodes (8): Disposition, main(), LaneView, How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to., Walk both lanes with nobody at the keyboard, and score what they did. Input is…, Run both lanes and print the report, so the scorer can be read before it is…, run_two_lanes()

### Community 138 - "reply_tree.py"
Cohesion: 0.40
Nodes (5): _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

## Knowledge Gaps
- **45 isolated node(s):** `One arrival, one route, and the route names the work`, `The floor masks the ballot before anything is scored`, `Scoring is expected loss in one unit`, `The model proposes, the code decides`, `Tools are one contract: prepare, authorize, commit` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `policy.py`, `registry.py`, `dataset.py`, `ActionPayload`, `ClaimScope`, `ChatRunner`, `test_gateway.py`, `VetoLevel`, `test_sim_tools.py`, `test_predrafts.py`, `Learner`, `session.py`, `run_canonical.py`, `arrivals`, `run_typed`, `Manifest`, `ScopeAnchor`, `floor.py`, `classify_action`, `runner.py`, `events.py`, `interrupting_case_ids`, `test_a_strangers_instructions_fence_every_route_whatever_the_action`, `test_floor_protection.py`, `routing_request`, `test_freeze.py`, `Lane`, `router.py`, `trace.py`, `dataclasses`, `test_floor.py`, `first_interrupt_of`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `ChatRunner` connect `ChatRunner` to `policy.py`, `graph.py`, `Learner`, `ClaimStore`, `SeededClock`, `feedback.py`, `registry.py`, `session.py`, `run_simulation`, `run_canonical.py`, `Claim`, `trace.py`, `SimulatedMailbox`, `Manifest`, `runner.py`, `Route`, `sim/__init__.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `Learner` connect `Learner` to `Bucket`, `loop.py`, `run_canonical.py`, `ClaimScope`, `Claim`, `ChatRunner`, `run_simulation`, `session.py`, `test_floor_protection.py`, `test_freeze.py`, `autonomy/state.py`, `router.py`, `runner.py`, `Route`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 137 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 137 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `BetaStore`) actually correct?**
  _`Learner` has 29 INFERRED edges - model-reasoned connections that need verification._