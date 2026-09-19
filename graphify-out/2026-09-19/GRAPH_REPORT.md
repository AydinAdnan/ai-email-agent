# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 98 files · ~94,904 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2659 nodes · 6703 edges · 136 communities (122 shown, 14 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 986 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `359d21f3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- Case
- graph.py
- registry.py
- ClaimStore
- test_economics.py
- feedback.py
- _case_from_mail_row
- Bucket
- ReplyTree
- test_floor.py
- test_claim_schema.py
- ChatRunner
- hybrid
- Handler
- sandbox.py
- test_sandbox.py
- harness.py
- graph_run
- runner.py
- test_gateway.py
- persona_demanded_route
- floor.py
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- .render
- ProposalError
- agent/state.py
- app.js
- _answer
- draft_reply
- .claim_for
- test_predrafts.py
- Posterior
- Learner
- EventStream
- test_events.py
- mask_for_llm
- PresidioMasker
- test_ui_session.py
- test_sim.py
- _redacted
- Claim
- schedule
- valid
- .route
- SplitViolation
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- run_graph
- _provider_for
- OpenAICompatibleProvider
- SimulatedMailbox
- ScopeAnchor
- run_scenario
- EffectLog
- injection.py
- parse_generated
- Message
- .lines_for
- test_triage.py
- FeedbackEvent
- _feedback
- _row_problems
- validate_cases
- test_freeze.py
- TraceSink
- ContextPhoneRecognizer
- masker.py
- test_replay.py
- Route
- test_graph_state.py
- build_reply_tree
- tools/__init__.py
- Any
- ProposalRequest
- SandboxError
- test_loop.py
- server.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- autonomy/state.py
- router.py
- named_route
- rules/graphify.md
- DESIGN.md
- README.md
- GraphOutcome
- GraphError
- LoopReport
- .get_instance
- EventValidationError
- Judge
- run_simulation
- GraphSession
- DecisionSource
- run_sandbox
- InterruptHook
- ScriptedReplies
- _claim_from_record
- TraceSink
- EmailEvent
- Session
- test_eval_run.py
- Cutoffs
- evaluate
- plan_deviation
- SenderIdentity
- JevRouted
- Jev
- run_loop
- reply
- offline_provider
- message_digest
- strictest_allowed
- ScoringError
- SimError
- tool_for_action
- ClaimStore
- IO
- ProposalProvider

## God Nodes (most connected - your core abstractions)
1. `Route` - 175 edges
2. `Router` - 62 edges
3. `Lane` - 61 edges
4. `Learner` - 58 edges
5. `ChatRunner` - 52 edges
6. `Manifest` - 50 edges
7. `Case` - 47 edges
8. `ActionPayload` - 45 edges
9. `Bucket` - 44 edges
10. `ProposalGateway` - 43 edges

## Surprising Connections (you probably didn't know these)
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_cli_refuses_to_open_the_sealed_lane()` --calls--> `main()`  [EXTRACTED]
  tests/test_sim.py → src/agent/cli.py
- `test_cli_requires_a_subcommand()` --calls--> `main()`  [EXTRACTED]
  tests/test_sim.py → src/agent/cli.py
- `message()` --calls--> `Message`  [INFERRED]
  tests/test_jev.py → src/agent/events.py

## Import Cycles
- None detected.

## Communities (136 total, 14 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.18
Nodes (11): Command, GraphSession, Any, What resuming a held decision did, or why the answer could not be used., One lane, one compiled graph, one checkpoint thread per decision. Holding the…, Walk the lane, holding at every decision that needs a human., Answer a held decision, or refuse the answer because the work has moved. A…, Carry a thread past its interrupt, or past the point a crash cut it off at. (+3 more)

### Community 1 - "Case"
Cohesion: 0.09
Nodes (27): cold_control(), What the same arrival gets with no preference in force and no trust behind it.…, mail_risk(), What a mail makes likely, from signals the pipeline already computed. An unsure…, Case, CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, One dataset row: its lane, its canonical event, its labels and the raw record. (+19 more)

### Community 2 - "graph.py"
Cohesion: 0.11
Nodes (38): CompiledStateGraph, GraphState, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), _bound() (+30 more)

### Community 3 - "registry.py"
Cohesion: 0.08
Nodes (31): ABC, _brief(), _digest(), _notify_text(), _params_brief(), PreparedAction, Any, datetime (+23 more)

### Community 4 - "ClaimStore"
Cohesion: 0.08
Nodes (41): ClaimStore, datetime, The one claims table, and the only way into it. Closed by default: a store with…, How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Capability, ConsentRequired, Grant (+33 more)

### Community 5 - "test_economics.py"
Cohesion: 0.09
Nodes (30): Ledger, The priced cost. Unpriced rows are excluded, and named by ``unpriced``., A process's spend: every provider call, and every arrival it never had to ask…, One case reached the proposal stage. A deflected one was settled without a call., MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price. (+22 more)

### Community 6 - "feedback.py"
Cohesion: 0.07
Nodes (40): _action_for(), _claim_reading(), _clean_label(), _decision_reading(), FeedbackContext, _from_context(), _narrowed(), _nothing() (+32 more)

### Community 7 - "_case_from_mail_row"
Cohesion: 0.19
Nodes (16): _attachment(), _case_from_mail_row(), event_from_row(), _message(), Any, datetime, Canonicalize one dataset row into an EmailEvent., Turn one plain mail row into a case the simulator can walk. Missing ids are… (+8 more)

### Community 8 - "Bucket"
Cohesion: 0.10
Nodes (24): Random, BetaStore, Bucket, _bucket_from(), Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first., The most specific contexts counted about, most evidential first. This is what a… (+16 more)

### Community 9 - "ReplyTree"
Cohesion: 0.14
Nodes (16): A reconstructed thread: its roots, plus every message's children by parent id.…, ReplyTree, _address(), _body_lines(), _prior_lines(), Reconstruct one case's thread, bounded by the reply-tree caps., The arriving mail the way an inbox shows it. Sender, recipients, subject, body…, One compact field for the labelled view: reconstructed messages and depth. (+8 more)

### Community 10 - "test_floor.py"
Cohesion: 0.05
Nodes (73): ActionPayload, floor_check(), Standardized representation of a candidate tool action., Evaluate a proposed action against the deterministic safety floor. Returns the…, parametrize, Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, Verify that every tool and parameter boundary resolves to the exact ActionClass., FLR-001: Financial transactions in action params must escalate. (+65 more)

### Community 11 - "test_claim_schema.py"
Cohesion: 0.14
Nodes (24): ClaimError, ValueError, Raised when a claim is underspecified, or about something never stored., _require_text(), memory(), preference(), parametrize, Protected attributes are out of memory by construction, not by a filter: the… (+16 more)

### Community 12 - "ChatRunner"
Cohesion: 0.12
Nodes (17): Decision, What the simulator does with one arrival., Whether this route has to wait for the user., _bucket_of(), ChatRunner, Drive a lane through the chat loop: arrivals on one task, input on another., Deliver every case in the lane, window by window, in the order the seed drew., Prepare the decision's steps, authorize them, and commit what may run.… (+9 more)

### Community 13 - "hybrid"
Cohesion: 0.16
Nodes (19): Exception, JevRouted, answer(), FakeJev, hybrid(), A wrapped model, the model's own script, and the ledger both of them write into., Drive the wrapper the way the gateway does, and hand back what it answered., No work to prepare, so the text model is not called at all. (+11 more)

### Community 14 - "Handler"
Cohesion: 0.11
Nodes (16): AbstractEventLoop, BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., Point the server at a session, which is what the tests and the page both need., The page, its assets, and the four calls it makes back. (+8 more)

### Community 15 - "sandbox.py"
Cohesion: 0.10
Nodes (28): as_dict(), charts(), main(), _markdown(), Path, _rate(), A live mailbox: fresh mail every run, through the real pipeline, judged from…, Keep the mailbox itself, so a report can be read next to the mail that produced… (+20 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.13
Nodes (29): _by_id(), The arrivals one record decided, in the order it decided them., Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its…, The whole environment on stand-ins: no key, no network, no judge., Each half decides exactly the arrivals it was given, and nothing goes missing., The model user is what makes the calibration half teach: it has to be asked., Nothing hostile is committed on its own, and the count says so with its… (+21 more)

### Community 17 - "harness.py"
Cohesion: 0.06
Nodes (31): CalibrationReport, EvalReport, Gate, HeldOutReport, main(), Any, LaneView, Path (+23 more)

### Community 18 - "graph_run"
Cohesion: 0.12
Nodes (26): ClaimStore, DecisionSource, GraphSession, Namespace, ProposalGateway, ProposalProvider, graph_run(), _keep_rules() (+18 more)

### Community 19 - "runner.py"
Cohesion: 0.16
Nodes (30): argparse, asyncio, collections_abc, dataclasses, enum, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The four reference cases, run end to end and printed as transcripts. Each case…, The evaluation run: teach the learning lane, freeze it, score the sealed lane… (+22 more)

### Community 20 - "test_gateway.py"
Cohesion: 0.08
Nodes (41): ProposalGateway, The offline provider: proposes from triage, no network, deterministic. It is a…, Turns provider text into a validated proposal, with one repair attempt., RuleProvider, A table that hid the rules provider would show a run spending nothing and doing…, test_the_offline_provider_is_counted_and_costs_nothing(), BrokenProvider, message() (+33 more)

### Community 21 - "persona_demanded_route"
Cohesion: 0.15
Nodes (19): _label_derived(), label_for(), _mail_rules(), _persona_checked(), persona_demanded_route(), persona_rule(), Message, Route (+11 more)

### Community 22 - "floor.py"
Cohesion: 0.08
Nodes (47): ActionClass, classify_action(), EmailContext, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement() (+39 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.09
Nodes (26): action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser (+18 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.09
Nodes (39): DraftCode, _flatten(), Predraft, StrEnum, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., Why a draft may not be shown, as a code a test and a transcript can name., Whether a draft may be shown, and the first reason it may not. (+31 more)

### Community 26 - ".render"
Cohesion: 0.12
Nodes (10): _money(), _percent(), Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for., One row: what one stage spent with one model., The estimated cost, or None when this model has no published rate. A call that… (+2 more)

### Community 27 - "ProposalError"
Cohesion: 0.15
Nodes (18): main(), Run the lanes, then print what they cost., build_provider(), ProposalError, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client() (+10 more)

### Community 28 - "agent/state.py"
Cohesion: 0.13
Nodes (18): The chosen route's expected loss, in handoffs., Drafting, A draft, what it read, and whether it may be shown., draft_fields(), hint_fields(), _plain(), prepared_fields(), Any (+10 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "_answer"
Cohesion: 0.15
Nodes (17): Any, Route, RuntimeError, _answer(), JevError, _post(), Post one request, or hand it to the transport a test supplied., The one question, with the four routes as its criteria in the house policy's… (+9 more)

### Community 31 - "draft_reply"
Cohesion: 0.14
Nodes (14): draft_reply(), FactSource, _first_name(), open_questions(), One thing the draft says, and where it came from. ``label`` and ``origin`` are…, The subject a reply carries, without stacking a second Re: on it., Who the reply greets: the display name's first word, else the address's local…, How the user signs off: their own address is the only name the mailbox holds. (+6 more)

### Community 32 - ".claim_for"
Cohesion: 0.21
Nodes (10): Claim, Proposal, _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one., The confirmed claim that bears on this mail and names a route, if one does., What the user's own words amount to for this mail, if anything. (+2 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.17
Nodes (13): Streaming inbox simulator: arrival schedule, chat loop and reply-tree…, One released window: its cases in delivery order, and the seed that ordered it., The window's case ids in the order they will arrive., Window, drafting(), Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, An ask that arrives with nothing prepared is the gap this phase closes., The answer belongs to the user, so the draft quotes the ask and marks the gap. (+5 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "Learner"
Cohesion: 0.12
Nodes (30): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The confirmed rule that refused this arm, or '' when the user has not refused…, FeedbackKind, What the user did after seeing a decision. Values are the dataset's…, feedback() (+22 more)

### Community 36 - "EventStream"
Cohesion: 0.16
Nodes (9): EventStream, _json_default(), Any, A stable hash of the replay log., An append-only log of arriving events. There is no update, no delete and no…, Every appended event, in arrival order., The canonical JSONL replay log: header line, then one line per arrival., Each arrival is stamped by the clock, one tick apart. (+1 more)

### Community 37 - "test_events.py"
Cohesion: 0.12
Nodes (27): OutOfOrderEventError, Reject a stream that repeats a case or message, or drifts out of order. Order…, Raised when a stream is not in ascending sequence order., validate_stream(), _event(), _load_dataset(), Unit tests for the canonical events (Phase 3.1). Covers: - Identity and…, A replayed stream can refuse a shape it does not understand. (+19 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.12
Nodes (22): get_token_map(), mask_for_llm(), Sanitize subject and body before any model call. Returns masked text only., Retrieve the current token to original value map for a thread., test_the_provider_is_shown_the_masked_mail_and_the_floor_is_not(), Unit tests for Presidio PII Masker (Phase 2)., The masking API hands back masked text only; the reverse map is opt-in., Retention is explicit: a forgotten thread keeps no raw values in memory. (+14 more)

### Community 39 - "PresidioMasker"
Cohesion: 0.16
Nodes (10): PresidioMasker, Warm singleton wrapper around Presidio Analyzer and Per-Thread Registry., Return a thread's registries, evicting the oldest thread past the cap., Drop a thread's tokens and reverse map; returns whether it existed., Count distinct tokens already handed out for one entity type., Deduplicate person names: match aliases, first names, and full names to one…, Assign or retrieve a consistent <TYPE_N> token for an entity value within a…, Mask PII entities in text with consistent <TYPE_N> tokens. (+2 more)

### Community 40 - "test_ui_session.py"
Cohesion: 0.10
Nodes (24): importlib_util, _call(), Any, Path, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET. (+16 more)

### Community 41 - "test_sim.py"
Cohesion: 0.07
Nodes (61): arrivals(), block_of(), dataset_routes(), decision_sources(), ExplodingPolicy, first_interrupt_of(), interrupting_case_ids(), labelled_routes() (+53 more)

### Community 42 - "_redacted"
Cohesion: 0.16
Nodes (16): _bounded(), _fingerprint(), Any, datetime, RuntimeError, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file., A stand-in a trace can carry: the digest, the size, and what kind of thing it… (+8 more)

### Community 43 - "Claim"
Cohesion: 0.16
Nodes (12): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, _action_words(), _bears_on(), Claim, The claim in plain words: what to do, where it applies, from when., Whether this is the claim in force, rather than one a correction replaced., The claims in force that bear on one mail, narrowest first. A claim with no… (+4 more)

### Community 44 - "schedule"
Cohesion: 0.12
Nodes (27): _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one., Every case in the order the windows will deliver them. (+19 more)

### Community 45 - "valid"
Cohesion: 0.23
Nodes (12): parse_proposal(), Validate one provider answer. Anything unexpected is an error, not a default., parametrize, The net under the gate: a proposal from some other path still cannot land…, The dataset's own unactionable ids must parse, and the floor must judge them., test_a_fenced_answer_parses(), test_a_valid_answer_parses(), test_an_action_nothing_implements_resolves_to_itself() (+4 more)

### Community 46 - ".route"
Cohesion: 0.17
Nodes (9): Message, JevAnswer, One typed decision, with the distribution behind it., What the choice carried, for the proposal schema's own confidence field. The…, One line a rationale can carry: the answer, the spread, and how long it took., One choice, off the event loop, metered with whatever the endpoint reported., Count the call, its tokens, and the price the response states for itself., The mail, plus what pre-triage already knows and the model is told as well. (+1 more)

### Community 47 - "SplitViolation"
Cohesion: 0.22
Nodes (9): RuntimeError, Raised when code reaches across the learning/held-out firewall., SplitViolation, The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read., The separation is symmetric: a lane view only sees its own rows., Held-out and development code cannot update the learner., test_a_held_out_view_cannot_open_a_calibration_case(), test_a_learning_read_of_a_held_out_case_is_a_split_violation() (+1 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.13
Nodes (23): approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The plan's crash matrix: whether the work ran or not, a resume applies it once. (+15 more)

### Community 49 - "retrieve_style"
Cohesion: 0.06
Nodes (42): estimate_tokens(), examples_from_row(), Picked, Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, A rough token count for a budget decision, not for a bill., One example that fits the budget, and why it was the one kept., What style the draft may borrow, and how the archive was narrowed to it. (+34 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.05
Nodes (44): one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, main(), The eval run as a command, for anyone who would rather not go through the CLI., _case_from_row(), LaneView, Manifest, ManifestError (+36 more)

### Community 52 - "run_graph"
Cohesion: 0.13
Nodes (21): Router, SimulatedMailbox, LaneView, TraceSink, Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts. (+13 more)

### Community 53 - "_provider_for"
Cohesion: 0.14
Nodes (17): ArgumentParser, build_parser(), _default_provider(), _provider_for(), The provider a run proposes with when the flag is absent. Read here rather than…, The proposer one name asks for: an endpoint, or an endpoint with Jev routing it., The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar. (+9 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.11
Nodes (15): Ledger, _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured. (+7 more)

### Community 55 - "SimulatedMailbox"
Cohesion: 0.18
Nodes (6): build_registry(), Every simulated tool, over one mailbox., Everything a commit can change, and nothing a prepare can., SimulatedMailbox, End to end through the real contract: prepare, authorize, commit one draft., test_the_approved_draft_is_the_draft_that_is_committed()

### Community 56 - "ScopeAnchor"
Cohesion: 0.11
Nodes (33): confirm_claim(), confirm_words(), Read the user's answer to the scope echo: the claim to store, or None for no., Whether a line confirms (True), refuses (False), or says something else (None)., ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means. (+25 more)

### Community 57 - "run_scenario"
Cohesion: 0.10
Nodes (19): main(), Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One reference case: the mail, what it is here to show, and the route it…, One canonical run: the pipeline's own output, plus what it decided and…, What the router considered, which every canonical run keeps. (+11 more)

### Community 58 - "EffectLog"
Cohesion: 0.20
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "injection.py"
Cohesion: 0.08
Nodes (30): base64, _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), InjectionScanResult, _names_its_own_domain(), Prompt injection tripwires and plan-deviation verification. Zero LLM dependence… (+22 more)

### Community 60 - "parse_generated"
Cohesion: 0.14
Nodes (13): _case_blocks(), generator_prompt(), parse_generated(), _preview(), Route, One situation to write a mail about, and how a careful assistant would treat it., The request for one arrival. Everything fresh about it comes from this frame., Read one generated mail, naming what is wrong rather than guessing a field. (+5 more)

### Community 61 - "Message"
Cohesion: 0.12
Nodes (18): Message, One email message, in a thread, in one direction., The direct replies to one message, in expansion order., Depth-first order over the reconstructed thread, asked-for root first., _first_intent(), _marketing_sender(), What can be said about a message before any model is called., The mailbox's own domain, taken from where the message was addressed. (+10 more)

### Community 62 - ".lines_for"
Cohesion: 0.29
Nodes (8): Decision, ModelUser, Message, The person whose mailbox this is, played by a model that is not the proposer.…, What the reply parser may look at: the mail and the decision, never a label., The lines to hand the waiting decision: the reply, and a confirmation if…, Whether the draft on the table may be saved. Nothing is approved by default., FeedbackContext

### Community 63 - "test_triage.py"
Cohesion: 0.14
Nodes (16): amount_in(), The largest amount mentioned in a text, as a float., message(), Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request(), test_a_known_sender_wins_over_every_marker() (+8 more)

### Community 64 - "FeedbackEvent"
Cohesion: 0.13
Nodes (14): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, is_learnable() (+6 more)

### Community 65 - "_feedback"
Cohesion: 0.24
Nodes (10): _feedback(), parametrize, Empty ids and malformed fields fail at construction, not at use., Each kind survives construction with explicit_for_learning intact., Silence is not approval": a non-decision claiming the learning flag fails., An explicit decision that disclaims learning is a bug, not a preference., test_every_feedback_kind_round_trips_with_its_flag(), test_explicit_decisions_must_be_flagged_learnable() (+2 more)

### Community 66 - "_row_problems"
Cohesion: 0.22
Nodes (10): DatasetProblem, One thing the case set gets wrong, named so it can be found and fixed., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender…, Check one row's fields and enums. Returns its problems and its warnings., The cross-row checks: ids and ordering, and nothing landing in two lanes., _row_problems(), _scenario() (+2 more)

### Community 67 - "validate_cases"
Cohesion: 0.06
Nodes (50): CaseReport, Path, What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Check a case set's counts, enums and splits before anything is asked to run it.…, validate_cases(), _codes(), _extra() (+42 more)

### Community 68 - "test_freeze.py"
Cohesion: 0.22
Nodes (12): event(), Path, The freeze: a learned run has to survive a process, and a bad payload has to be…, A learner and a router that have counted a few real readings., The restored learner has to answer the routing question, not just hold the…, taught(), test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(), test_a_file_that_cannot_be_read_is_named() (+4 more)

### Community 69 - "TraceSink"
Cohesion: 0.11
Nodes (21): IO, LoopReport, data_validate(), eval_all(), loop_run(), main(), Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard., Print what a case set holds and everything wrong with it. (+13 more)

### Community 70 - "ContextPhoneRecognizer"
Cohesion: 0.17
Nodes (9): EntityRecognizer, RecognizerResult, _build_custom_recognizers(), ContextPhoneRecognizer, ContextSSNRecognizer, Any, Build custom recognizers for domain entities, regional IDs, and robust phones., Detects phone numbers accurately, extracting only the digit span. (+1 more)

### Community 71 - "masker.py"
Cohesion: 0.15
Nodes (12): AnalyzerEngine, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, PII masking and anonymization package., _clean_person_name(), _create_analyzer(), forget_thread() (+4 more)

### Community 72 - "test_replay.py"
Cohesion: 0.05
Nodes (54): datetime, Replay events through a fresh seeded stream., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time., replay(), SeededClock, manifest() (+46 more)

### Community 73 - "Route"
Cohesion: 0.08
Nodes (60): The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival., Router, RoutingRequest, The four autonomy outcomes a candidate action can be routed to.…, Route (+52 more)

### Community 74 - "test_graph_state.py"
Cohesion: 0.13
Nodes (24): GraphState, One decision, from arrival to receipt. Ids and hashes rather than the mail…, message(), Path, Not just the serde: a compiled graph through a saver hands back the same values., The allowlist is the schema: a new field is traceable, not silently dropped., The body and subject are inputs to the decision, and must not reach the file., No line may contain these words, in a key or in a value. (+16 more)

### Community 75 - "build_reply_tree"
Cohesion: 0.17
Nodes (18): build_reply_tree(), _order_key(), _ordered_roots(), Bounded reply-tree reconstruction (Phase 3.4). Thread history arrives flat and…, Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…, Reconstruct the reply tree for a thread, bounded by depth and node caps.…, message() (+10 more)

### Community 76 - "tools/__init__.py"
Cohesion: 0.14
Nodes (16): Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired, Authorization, AuthorizationRefused, RuntimeError, A user's yes, bound to the work they were shown., Permission for one prepared action to run, and why it was granted. (+8 more)

### Community 77 - "Any"
Cohesion: 0.20
Nodes (8): Arrival, Any, One generated mail, with the brief and the writer's own opinion that produced…, The mail in the loader's own shape. It carries no labels, because it has none., What the run keeps beside the row: which brief wrote it, and what it expected., The runner's interrupt hook: the waiting decision gets its lines from the model., The arrivals of the half the agent had never seen, in delivery order., Queue

### Community 78 - "ProposalRequest"
Cohesion: 0.22
Nodes (6): ProposalRequest, Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Ask once. A provider that fails in any way is a failed proposal, not a crash. A…, A model in the shape of the provider protocol, answering from a script., ScriptedProvider

### Community 79 - "SandboxError"
Cohesion: 0.24
Nodes (6): RuntimeError, Raised when the environment cannot be built or read., SandboxError, FakeModel, One stand-in for the endpoint: it writes mail, answers as the owner, and…, Answer whichever question the prompt asks, in the role whose stage it is.

### Community 80 - "test_loop.py"
Cohesion: 0.16
Nodes (20): asked(), _drained(), loop(), LaneView, Queue, A named case still waits for the second line, so an unanswered echo stores…, Nothing hangs on a prompt the script never feeds: it is told a line that does…, The whole class of recruiter arrivals, in order, and nothing else beside it. (+12 more)

### Community 81 - "server.py"
Cohesion: 0.25
Nodes (8): dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, ThreadingHTTPServer, webbrowser

### Community 83 - "Lane"
Cohesion: 0.08
Nodes (60): calibration_report(), held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both… (+52 more)

### Community 87 - "autonomy/state.py"
Cohesion: 0.23
Nodes (14): _entries(), freeze(), load(), Any, Path, Freezing what a run learned, so the next one starts where it stopped. Three…, Write the frozen state, naming the file in the failure rather than raising…, Read a frozen state back, or say what about it could not be read. (+6 more)

### Community 88 - "router.py"
Cohesion: 0.17
Nodes (21): Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys…, Versioned outcome costs, in handoffs. Changing a number means a new version.…, One route's expected loss, and the workings, which are what a receipt records., The expected loss of one route for one mail. ``risk`` holds the probability of…, Score the routes the floor left available, in the order the floor gave them. (+13 more)

### Community 98 - "named_route"
Cohesion: 0.24
Nodes (10): named_route(), The route the user's own rules name for this mail, if any. Two sources count: a…, case(), _hints(), An untrusted proposal is the thing the router tests, so it cannot buy silence., The memory layer answers from a claim, and that is a preference like the rules…, A confirmed rule, the way the parser hands one over., rule() (+2 more)

### Community 102 - "GraphOutcome"
Cohesion: 0.50
Nodes (3): GraphOutcome, What a lane through the graph did., How many times a tool actually ran, counted from the receipts.

### Community 103 - "GraphError"
Cohesion: 0.25
Nodes (9): Authorization, PreparedAction, _authorized_settled(), commit(), GraphError, RuntimeError, The only node that changes anything, and it only ever sees authorized work., Authorize from the state alone, so a decision approved before a crash still… (+1 more)

### Community 104 - "LoopReport"
Cohesion: 0.14
Nodes (8): LoopReport, Decisions that would still wait for a human, with the rules in front., Decisions the same lane waits on with nothing remembered, or 0 with no control., Arrivals a rule sent somewhere else than the lane would have gone on its own., Of those, the arrivals that came after the mail their rule was taught on. This…, Asking the rules took off the user, measured against the lane with no rules.…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions the chat pass waited on. Not a baseline: a rule takes effect from the…

### Community 105 - ".get_instance"
Cohesion: 0.50
Nodes (3): Access or initialize the singleton PresidioMasker., Verify unmask_text restores original values accurately., test_unmasking()

### Community 106 - "EventValidationError"
Cohesion: 0.18
Nodes (10): Attachment, DuplicateEventError, EventValidationError, ValueError, An attachment as metadata, plus its text when the text is extractable.…, Raised when a canonical event violates the schema., Raised when a stream carries the same case or message twice., _require_text() (+2 more)

### Community 107 - "Judge"
Cohesion: 0.17
Nodes (9): Judge, _judged(), Judgement, One judged case: the score, then the judge's own reason for it., One external opinion, with the reason it gave., An independent model's opinion on the two questions the code cannot answer., Whether a judgement can be asked for at all, and why not when it cannot., One GEval, built once, pointed at the judge model rather than at OpenAI. (+1 more)

### Community 108 - "run_simulation"
Cohesion: 0.12
Nodes (23): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+15 more)

### Community 111 - "run_sandbox"
Cohesion: 0.15
Nodes (21): _banner(), _blocks(), _judge_run(), _note(), GraphSession, IO, Ask the judge about a sample of the second half: the routes, and the drafts.…, A plain-text caller for one model role, or a named failure when it has no… (+13 more)

### Community 113 - "ScriptedReplies"
Cohesion: 0.25
Nodes (5): InterruptHook, Queue, Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end., ScriptedReplies

### Community 114 - "_claim_from_record"
Cohesion: 0.18
Nodes (9): _claim_from_record(), _claim_record(), Any, Path, Take up the claims already in the store's file, when consent allows their use., Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''., One claim as a JSON object, enums and the timestamp written out in full. (+1 more)

### Community 116 - "EmailEvent"
Cohesion: 0.17
Nodes (9): The lane's arriving events, in sequence order., EmailEvent, An email arriving for a case: the unit the graph consumes and replays. Only…, The id of the arriving message., Record one arrival, or refuse it and leave the stream untouched. The whole…, The arriving message and the thread it is attached to must agree., test_event_rejects_a_message_that_does_not_belong_to_its_thread(), The manifest hands out EmailEvents, not raw rows. (+1 more)

### Community 117 - "Session"
Cohesion: 0.07
Nodes (22): ClaimStore, ProposalProvider, The user's own words, consulted before the provider. Wraps another provider:…, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, AnswerQueue (+14 more)

### Community 118 - "test_eval_run.py"
Cohesion: 0.13
Nodes (23): load_script(), Any, Path, The async driver, run to completion., The transcript: what the user says, at the decisions they say it at., The transcript in the chat loop's own form: ``CASE=line;line``., Read a transcript, naming what is wrong with it rather than failing on a…, run_eval() (+15 more)

### Community 119 - "Cutoffs"
Cohesion: 0.15
Nodes (9): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+1 more)

### Community 120 - "evaluate"
Cohesion: 0.22
Nodes (8): evaluate(), _frozen(), Teach, freeze, and score the sealed lane exactly once., Freeze the learned state, turning the writer's ValueError into a scoring…, Protocol, ProposalProvider, A source of untrusted proposal text., Return raw proposal text for one request.

### Community 121 - "plan_deviation"
Cohesion: 0.22
Nodes (9): plan_deviation(), Any, Verify that a proposed tool action conforms to the pre-committed triage plan.…, When tool is in pre-committed plan, deviation is False., When tool is NOT in pre-committed plan, deviation is True., When email body smuggles a recipient absent from the plan, plan deviation trips., test_plan_deviation_allowed_tool(), test_plan_deviation_smuggled_recipient() (+1 more)

### Community 122 - "SenderIdentity"
Cohesion: 0.25
Nodes (7): Who an email claims to come from, and whether that claim is verified.…, SenderIdentity, History cannot smuggle a message that belongs to a different thread., History ids are unique, even though the dataset reuses them across cases., test_thread_rejects_a_message_from_another_thread(), test_thread_rejects_duplicate_message_ids(), message()

### Community 123 - "JevRouted"
Cohesion: 0.22
Nodes (7): ProposalRequest, JevRouted, Jev decides how much autonomy the mail gets; the model decides what the work…, The pair's name, so a run says where a proposal could have come from., Whichever models answered, named the way a run names them., Compose one proposal: the route from Jev, the work from the model., The model's own answer, kept whole, with the reason it was needed named.

### Community 124 - "Jev"
Cohesion: 0.18
Nodes (9): Jev, ProposalProvider, The route question, asked over HTTP and metered like every other call., The hybrid, as a run selects it: Jev in front of whatever provider it was given., route_by_jev(), The text model, answering from a script so nothing reaches a network., ScriptedModel, test_the_hybrid_needs_a_key_to_route() (+1 more)

### Community 125 - "run_loop"
Cohesion: 0.28
Nodes (9): _answered_cases(), ClaimStore, IO, LaneView, ProposalProvider, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Each arrival a rule answered, mapped to the arrival whose mail taught that rule., run_loop() (+1 more)

### Community 127 - "offline_provider"
Cohesion: 0.33
Nodes (5): fixture, MonkeyPatch, offline_provider(), Environment the suite runs under. ``main`` loads .env so a command can be run…, Every test proposes from the offline rules unless it asks for something else.

### Community 128 - "message_digest"
Cohesion: 0.33
Nodes (6): digest_of(), message_digest(), A short stable digest of a text, for a field that must not hold the text., Identify a message by content, so a trace can name the mail it read., Keep the domain, drop the person: a local part becomes a digest., _scrub()

### Community 129 - "strictest_allowed"
Cohesion: 0.67
Nodes (3): The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), test_strictest_allowed_is_the_least_autonomous_route()

### Community 130 - "ScoringError"
Cohesion: 0.08
Nodes (19): ask_curve(), Block, Disposition, dispositions(), RuntimeError, The interruption curve: how many cases each block of the lane needed the user…, Refuse a record whose counts cannot add up to what the run processed., Raised when a run cannot be scored as asked, rather than scored wrongly. (+11 more)

### Community 131 - "SimError"
Cohesion: 0.67
Nodes (3): RuntimeError, Raised when a run cannot continue, naming the case it stopped on., SimError

## Knowledge Gaps
- **14 isolated node(s):** `Design: Key Decisions & Trade-offs`, `Email Autonomy Agent`, `CHOICES`, `ROUTES`, `Silence is not approval` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `Case`, `strictest_allowed`, `registry.py`, `ScoringError`, `test_economics.py`, `feedback.py`, `Bucket`, `test_floor.py`, `test_claim_schema.py`, `ChatRunner`, `runner.py`, `test_gateway.py`, `floor.py`, `test_sim_tools.py`, `test_draft_validation.py`, `Learner`, `test_ui_session.py`, `test_sim.py`, `Claim`, `valid`, `Manifest`, `SimulatedMailbox`, `ScopeAnchor`, `run_scenario`, `Message`, `FeedbackEvent`, `_row_problems`, `test_freeze.py`, `test_graph_state.py`, `tools/__init__.py`, `Lane`, `router.py`, `named_route`, `_claim_from_record`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `Case`, `Learner`, `ClaimStore`, `test_ui_session.py`, `ChatRunner`, `Handler`, `Lane`, `runner.py`, `Manifest`, `test_gateway.py`, `evaluate`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `Ledger` connect `test_economics.py` to `.render`, `runner.py`, `Jev`, `test_gateway.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 145 inferred relationships involving `Route` (e.g. with `preference_for()` and `Scenario`) actually correct?**
  _`Route` has 145 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `Lane` (e.g. with `main()` and `one_case_view()`) actually correct?**
  _`Lane` has 52 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 32 INFERRED edges - model-reasoned connections that need verification._