# Graph Report - ai-email-agent  (2026-09-19)

## Corpus Check
- 98 files · ~95,145 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2617 nodes · 7003 edges · 123 communities (109 shown, 14 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 1120 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `359d21f3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GraphSession
- runner.py
- graph.py
- registry.py
- ClaimStore
- test_economics.py
- feedback.py
- SenderIdentity
- Bucket
- view
- test_floor.py
- ClaimScope
- ChatRunner
- test_jev.py
- Handler
- SandboxOutcome
- test_sandbox.py
- CalibrationReport
- graph_run
- cli.py
- ProposalGateway
- _receipt_route
- VetoLevel
- test_sim_tools.py
- email_tools.py
- test_draft_validation.py
- Ledger
- build_provider
- agent/state.py
- app.js
- jev.py
- drafts.py
- ActionPayload
- test_predrafts.py
- Posterior
- FeedbackKind
- SeededClock
- test_events.py
- mask_for_llm
- masker.py
- Session
- run_typed
- trace.py
- claims.py
- pytest
- arrivals
- drafting_for
- LaneView
- test_graph_resume.py
- retrieve_style
- Routes
- Manifest
- test_graph.py
- classify_action
- OpenAICompatibleProvider
- Block
- ScopeAnchor
- interrupting_case_ids
- EffectLog
- scan
- TraceSink
- Message
- ModelUser
- test_triage.py
- .learnable_feedback
- first_interrupt_of
- ask_curve
- test_cases.py
- _background_loop
- main
- ._line
- test_benign_workplace_clean_pass
- test_replay.py
- Router
- test_graph_state.py
- test_sim.py
- _server
- Any
- ProposalError
- SandboxError
- test_loop.py
- server.py
- Workflow: graphify
- Lane
- email-autonomy-agent
- autonomy/state.py
- Route
- Predraft
- rules/graphify.md
- DESIGN.md
- README.md
- datetime
- Transcript
- LoopReport
- .labels
- _order_key
- run_sandbox
- run_simulation
- AnswerQueue
- Validation
- write_mailbox
- BrokenProvider
- set_session
- .save
- _view_note
- _resume_note
- RememberedProvider
- evaluate
- .effects
- safety/__init__.py
- floor_check
- dispositions

## God Nodes (most connected - your core abstractions)
1. `Route` - 202 edges
2. `Lane` - 74 edges
3. `Router` - 68 edges
4. `Learner` - 61 edges
5. `Manifest` - 61 edges
6. `Message` - 61 edges
7. `ClaimStore` - 53 edges
8. `ChatRunner` - 53 edges
9. `ProposalGateway` - 51 edges
10. `Case` - 50 edges

## Surprising Connections (you probably didn't know these)
- `test_every_type_the_plan_names_is_allowed_and_nothing_else()` --uses--> `ClaimType`  [INFERRED]
  tests/memory/test_claim_schema.py → src/agent/memory/claims.py
- `test_the_cost_is_the_published_rate_for_that_sample()` --uses--> `Spend`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_a_model_nobody_prices_is_unpriced_rather_than_free()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_an_empty_run_reports_zero_rather_than_dividing_by_it()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py
- `test_the_deflection_rate_counts_arrivals_not_calls()` --uses--> `Ledger`  [INFERRED]
  tests/eval/test_economics.py → src/agent/usage.py

## Import Cycles
- None detected.

## Communities (123 total, 14 thin omitted)

### Community 0 - "GraphSession"
Cohesion: 0.11
Nodes (22): Command, _bound(), GraphError, GraphOutcome, GraphSession, Any, RuntimeError, Hand a node its runtime. The graph only ever sees the state. (+14 more)

### Community 1 - "runner.py"
Cohesion: 0.04
Nodes (64): cold_control(), main(), What the same arrival gets with no preference in force and no trust behind it.…, Run one reference case through the pipeline, with nobody at the keyboard. Input…, One transcript: the mail, the decision, and the numbering behind it., The four routes side by side, which is the check the plan asks for., Print the four transcripts and fail when one lands on the wrong route., One canonical run: the pipeline's own output, plus what it decided and… (+56 more)

### Community 2 - "graph.py"
Cohesion: 0.10
Nodes (37): CompiledStateGraph, langgraph_checkpoint_memory, langgraph_graph, langgraph_graph_state, langgraph_types, authorize(), build_graph(), _case() (+29 more)

### Community 3 - "registry.py"
Cohesion: 0.05
Nodes (53): ABC, _authorized_settled(), Authorize from the state alone, so a decision approved before a crash still…, build_registry(), Every simulated tool, over one mailbox., Simulated tools and the prepare/authorize/commit contract a real adapter will…, Approval, ApprovalRequired (+45 more)

### Community 4 - "ClaimStore"
Cohesion: 0.09
Nodes (40): _open_store(), The run's memory: the rules already kept, and the file they live in., ClaimStore, The one claims table, and the only way into it. Closed by default: a store with…, Take up the claims already in the store's file, when consent allows their use., How many claims are in memory., Keep a confirmed claim, if there is consent for it. The same claim is kept once., Capability (+32 more)

### Community 5 - "test_economics.py"
Cohesion: 0.12
Nodes (25): MeteredCompletions, provider(), SimpleNamespace, The cost meter: it has to count what was spent, and admit what it cannot price., No call, no tokens, and the deflection is what makes the saving countable., Two tables for one run is how a cost report starts under-reporting., The remembered provider sits between the gateway and the model, and holds no…, A proxy that hands back plain JSON must price the same as the SDK's own object. (+17 more)

### Community 6 - "feedback.py"
Cohesion: 0.08
Nodes (38): What the reply parser may look at: the mail and the decision, never a label., _action_for(), _claim_reading(), _clean_label(), confirm_claim(), confirm_words(), _decision_reading(), FeedbackContext (+30 more)

### Community 7 - "SenderIdentity"
Cohesion: 0.14
Nodes (20): _attachment(), _case_from_mail_row(), _case_from_row(), event_from_row(), _message(), Any, datetime, Canonicalize one dataset row into an EmailEvent. (+12 more)

### Community 8 - "Bucket"
Cohesion: 0.09
Nodes (25): The confirmed rule that refused this arm, or '' when the user has not refused…, BetaStore, Bucket, _bucket_from(), Random, Count one observation, at every level of the bucket's chain., One Thompson sample: the number an arm is compared with., Every level anything has been counted about, most evidential first. (+17 more)

### Community 9 - "view"
Cohesion: 0.20
Nodes (11): ExplodingPolicy, The lane is delivered window by window, not in the dataset's sequence order., A decision source that fails, to check the failure names its case., Fixture case ids in the order the windows deliver them., scheduled_case_ids(), test_a_failing_policy_names_the_case_it_stopped_on(), test_an_arrival_shows_the_mail_a_production_inbox_shows(), test_arrivals_come_in_the_windowed_order_the_seed_recorded() (+3 more)

### Community 10 - "test_floor.py"
Cohesion: 0.07
Nodes (28): Unit tests for the deterministic Safety Floor & Prompt Injection Guardrails…, FLR-002: Credential or authentication modification must escalate., FLR-003: Unrecognized tool calls must be escalated., FLR-005: Mass sends (>5 recipients) must require human approval (ASK)., A single external recipient is an external send, not a mass send., FLR-006: Permanent deletion of mailbox items cannot occur autonomously., A reversible action leaves the full arm set for the learned policy., An external send cannot be silent or notified: ask or escalate only. (+20 more)

### Community 11 - "ClaimScope"
Cohesion: 0.12
Nodes (27): ClaimError, ClaimScope, ValueError, Raised when a claim is underspecified, or about something never stored., Where a claim applies: the axes the learner's buckets are built from., Whether the claim names anything narrower than the whole mailbox., A stable key for the claim's scope, for ids and later comparison., memory() (+19 more)

### Community 12 - "ChatRunner"
Cohesion: 0.09
Nodes (23): is_approving(), Whether this reading is a vote for the agent acting on its own., Keep the refusal, with the scope the rule was confirmed for rather than this…, Whether this reading is a vote for the agent acting on its own. The route a…, Count one explicit decision about one bucket, at most once. False if uncounted., Adapt one bucket's cutoffs from one explicit decision, at most once. Silence…, FeedbackEvent, What the user did with a decision, and whether it may teach the learner. (+15 more)

### Community 13 - "test_jev.py"
Cohesion: 0.07
Nodes (45): ArgumentParser, Exception, build_parser(), _default_provider(), The provider a run proposes with when the flag is absent. Read here rather than…, The flags both replay paths take: which mail, which lane, who proposes, a trace., The CLI's argument grammar., _replay_flags() (+37 more)

### Community 14 - "Handler"
Cohesion: 0.22
Nodes (8): BaseHTTPRequestHandler, WAJO Calibration UI, Handler, Any, Silence the per-request log: the page polls, and the terminal stays readable., The page, its assets, and the four calls it makes back., Begin a run from the form the page sent., What the page's side panel shows: what the run did and what it now knows.

### Community 15 - "SandboxOutcome"
Cohesion: 0.10
Nodes (22): as_dict(), charts(), main(), _markdown(), Path, Keep the mailbox itself, so a report can be read next to the mail that produced…, The machine-readable run, for the charts and for anyone reading it later., The three pictures: what it decided, how often it asked, and how it matched. (+14 more)

### Community 16 - "test_sandbox.py"
Cohesion: 0.12
Nodes (31): _by_id(), _rate(), What the run did, in the order a reader wants it., The arrivals one record decided, in the order it decided them., render(), _score(), Path, The live mailbox: fresh mail, a model owner, the real pipeline, and its… (+23 more)

### Community 17 - "CalibrationReport"
Cohesion: 0.07
Nodes (23): CalibrationReport, EvalReport, Gate, HeldOutReport, Any, Path, _rate(), A count and its denominator, which is the only honest way to print a rate. (+15 more)

### Community 18 - "graph_run"
Cohesion: 0.14
Nodes (26): Namespace, eval_all(), graph_run(), _keep_rules(), loop_run(), _policy(), _proposing(), _provider_for() (+18 more)

### Community 19 - "cli.py"
Cohesion: 0.14
Nodes (34): argparse, asyncio, base64, collections_abc, dataclasses, enum, What a run costs, stage by stage (plan Commit 8.4). Cost is the one number a…, The two-lane scorer: what the agent did, counted where it happened. The report… (+26 more)

### Community 20 - "ProposalGateway"
Cohesion: 0.09
Nodes (38): ProposalGateway, Turns provider text into a validated proposal, with one repair attempt., message(), quiet_but_wrong(), The model proposal gateway: untrusted output, one repair, then fail closed., A transport error is a failed proposal, not an exception out of the session., The ask shape decides too: 'consider changing your password' is advice., A provider that would happily label suspicious mail and move on. (+30 more)

### Community 21 - "_receipt_route"
Cohesion: 0.40
Nodes (5): The persona policy's receipt threshold, applied to the amount the mail states., _receipt_route(), amount_in(), The largest amount mentioned in a text, as a float., test_money_is_read_from_the_mail()

### Community 22 - "VetoLevel"
Cohesion: 0.10
Nodes (28): ActionClass, _eval_credential_security(), _eval_injection_tripwires(), _eval_irreversible_external(), _eval_mass_send(), _eval_money_movement(), _eval_permanent_deletion(), _eval_unknown_tool() (+20 more)

### Community 23 - "test_sim_tools.py"
Cohesion: 0.15
Nodes (27): mailbox(), prepare(), Phase 3.3: the simulated tools and the prepare/authorize/commit contract. The…, The digest covers the steps, so approving one label never approves another., A draft with no body is a blocked step on the receipt, not a silent no-op., One vocabulary: a dataset action id either names a tool or has none on purpose., The goal: point it at sender, subject and body, and nothing else., A tool takes mail, not a case: the same call works for any message. (+19 more)

### Community 24 - "email_tools.py"
Cohesion: 0.08
Nodes (28): action_vocabulary(), ArchiveEmail, CreateDraft, Draft, _email_id(), LabelEmail, Notification, NotifyUser (+20 more)

### Community 25 - "test_draft_validation.py"
Cohesion: 0.15
Nodes (29): DraftCode, StrEnum, Why a draft may not be shown, as a code a test and a transcript can name., Everything the draft may state without inventing it: the mail, and its thread., Whether this draft may be shown. Fixed order, and the first refusal is the…, source_text(), validate_draft(), case() (+21 more)

### Community 26 - "Ledger"
Cohesion: 0.08
Nodes (16): Ledger, _money(), _percent(), The priced cost. Unpriced rows are excluded, and named by ``unpriced``., Most-spending stage first, so the table reads as a ranking., The per-stage table, under it the deflection line, and what the run cost per…, Say what the money figure covers, so an unpriced model cannot hide in a total.…, A cost, or ``n/a`` for a model nobody publishes a rate for. (+8 more)

### Community 27 - "build_provider"
Cohesion: 0.19
Nodes (13): build_provider(), Resolve a provider by name, refusing one that cannot run here. The model comes…, fake_client(), FakeCompletions, MonkeyPatch, SimpleNamespace, The slice of the OpenAI client the provider uses, capturing the request., The request carries the schema, so a model cannot omit a key or invent an… (+5 more)

### Community 28 - "agent/state.py"
Cohesion: 0.12
Nodes (25): The chosen route's expected loss, in handoffs., One line per decision, and one per reply: ids, hashes, bounded records., draft_fields(), hint_fields(), message_digest(), _plain(), prepared_fields(), Any (+17 more)

### Community 29 - "app.js"
Cohesion: 0.21
Nodes (23): action(), api(), attach(), CHOICES, clean(), el(), parseMail(), placeDraft() (+15 more)

### Community 30 - "jev.py"
Cohesion: 0.08
Nodes (31): _answer(), Jev, JevAnswer, JevError, _post(), proposing_provider(), Any, RuntimeError (+23 more)

### Community 31 - "drafts.py"
Cohesion: 0.10
Nodes (25): draft_reply(), FactSource, _first_name(), _flatten(), open_questions(), Picked, Predrafts for the ASK route (Phase 7). An ask is only worth the interruption if…, One example that fits the budget, and why it was the one kept. (+17 more)

### Community 32 - "ActionPayload"
Cohesion: 0.14
Nodes (18): ActionPayload, Standardized representation of a candidate tool action., FLR-001: Financial transactions in action params must escalate., An irreversible internal send keeps notify, ask and escalate, never silent., A mail whose sender the mailbox cannot vouch for., The mail fences, not the proposed action: a harmless label still collapses to…, Mailbox housekeeping commissioned by a stranger is the same shape, subject…, Please reply with the numbers' from a colleague is a request, and is left alone. (+10 more)

### Community 33 - "test_predrafts.py"
Cohesion: 0.13
Nodes (22): Drafting, A draft, what it read, and whether it may be shown., drafting(), held(), Path, Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing…, A reply the user cannot trust is worse than a mail handed back., A draft is mail text: the record keeps its shape, sizes and labels, not its… (+14 more)

### Community 34 - "Posterior"
Cohesion: 0.29
Nodes (4): Posterior, One estimate: the counts the store holds, with the prior folded in., The probability the user approves of this, before any sampling., How much has been counted at the answering level, in units of feedback.

### Community 35 - "FeedbackKind"
Cohesion: 0.11
Nodes (30): FeedbackKind, is_learnable(), What the user did after seeing a decision. Values are the dataset's…, Return whether this kind of feedback may update the learner., Whether a learner may use this, which is the kind's own rule., feedback(), Never tell me about these" is a never in the user's words and a yes in effect., The wiring, not just the rule: a line confirmed at a prompt moves a posterior. (+22 more)

### Community 36 - "SeededClock"
Cohesion: 0.08
Nodes (27): hashlib, EventStream, datetime, Seeded clock and append-only event stream (Phase 3.2). Replay has to be…, Replay events through a fresh seeded stream., A deterministic clock. Time moves because the simulation says so., The current simulated time., Move simulated time forward and return the new time. (+19 more)

### Community 37 - "test_events.py"
Cohesion: 0.05
Nodes (56): Attachment, DuplicateEventError, EmailEvent, EventValidationError, OutOfOrderEventError, ValueError, An attachment as metadata, plus its text when the text is extractable.…, A conversation: the messages that arrived before this case, oldest first. (+48 more)

### Community 38 - "mask_for_llm"
Cohesion: 0.10
Nodes (27): PII masking and anonymization package., forget_thread(), get_token_map(), mask_for_llm(), Access or initialize the singleton PresidioMasker., Sanitize subject and body before any model call. Returns masked text only., Retrieve the current token to original value map for a thread., Drop a thread's token registry and reverse map. (+19 more)

### Community 39 - "masker.py"
Cohesion: 0.07
Nodes (28): AnalyzerEngine, EntityRecognizer, presidio_analyzer, presidio_analyzer_nlp_engine, presidio_anonymizer, RecognizerResult, _build_custom_recognizers(), _clean_person_name() (+20 more)

### Community 40 - "Session"
Cohesion: 0.16
Nodes (18): importlib_util, One calibration run, driven a line at a time. The run is the one the CLI drives…, Session, A choice the page must not offer: nothing the user says takes this one off the…, The ask is for the user to edit: the reply, its facts and its gaps arrive…, Poll a session the way the page does, so a slow line fails as one readable…, The run writes the summary a line at a time; the page has to read it as one…, The four states are the colours on the page, so each card needs the route it… (+10 more)

### Community 41 - "run_typed"
Cohesion: 0.14
Nodes (17): block_of(), DecisionSource, One arrival's text, from its header up to the next arrival., Only one of the two has something to release, so only one says approval., A user typing rules at an escalation would be teaching the wrong thing., Sender, subject and body are inputs in production; labels are only answers.…, Replay the fixture, typing ``typed`` at the given interrupt numbers. Lines…, run_typed() (+9 more)

### Community 42 - "trace.py"
Cohesion: 0.20
Nodes (17): digest_of(), A short stable digest of a text, for a field that must not hold the text., _bounded(), _fingerprint(), Any, datetime, A nested record: its keys are scrubbed too, since a caller chose them., A refused key's name is itself replaced, so `token_map` cannot reach the file. (+9 more)

### Community 43 - "claims.py"
Cohesion: 0.12
Nodes (19): _action_words(), _bears_on(), Claim, _claim_from_record(), claim_id_for(), _claim_record(), Any, Path (+11 more)

### Community 44 - "pytest"
Cohesion: 0.06
Nodes (46): pytest, _dependencies_first(), dependencies_of(), Any, RuntimeError, Raised when a case names a dependency no window can deliver before it., The ids a case says must arrive before it, from…, Cut a lane into ordered windows, shuffling only inside each one. (+38 more)

### Community 45 - "arrivals"
Cohesion: 0.14
Nodes (18): arrivals(), dataset_routes(), labelled_routes(), Path, The case ids of the arrival blocks, in the order they were printed., The route the pipeline chose for each arrival, in order., The dataset's route for each arrival, which only the label view prints., The eval curve is built from these two, so they have to be the run's own record. (+10 more)

### Community 46 - "drafting_for"
Cohesion: 0.17
Nodes (12): drafting_for(), examples_from_row(), Any, How many examples this case allows. The row's ``needs_draft`` is deliberately…, The tool arguments that carry this draft. It is addressed to whoever wrote., Retrieve, write and check one draft for one mail., One reply the user actually sent, consented for style., Read one example from the shape a mailbox hands over. (+4 more)

### Community 47 - "LaneView"
Cohesion: 0.08
Nodes (16): LaneView, RuntimeError, Raised when code reaches across the learning/held-out firewall., Return the lane-bound handle for one lane., A lane-bound handle over the manifest. A view can only open cases in its own…, The lane's arriving events, in sequence order., Open one case from this lane. Refuses any other lane's case., Whether this lane may update the learner. (+8 more)

### Community 48 - "test_graph_resume.py"
Cohesion: 0.12
Nodes (23): approval_for(), Crash, Crashing, parametrize, RuntimeError, The provider answers differently on the second look: the yes no longer fits., A yes is not an answer where the floor sent it to a human to decide., The plan's crash matrix: whether the work ran or not, a resume applies it once. (+15 more)

### Community 49 - "retrieve_style"
Cohesion: 0.18
Nodes (19): estimate_tokens(), A rough token count for a budget decision, not for a bill., The few sent replies a draft may learn from: same person, then same intent,…, retrieve_style(), example(), Phase 7.1: retrieving the few sent replies a draft may learn from., One sent reply, from the mailbox's own history., A reply the user sent this person beats an older one to anybody else. (+11 more)

### Community 50 - "Routes"
Cohesion: 0.22
Nodes (8): Routes, Silence is not approval, The one-unit loss matrix, The order the router applies, The safety floor decides who is on the ballot, What an ask carries, Worked example: the ambiguous refund, Worked example: the AWS invoice

### Community 51 - "Manifest"
Cohesion: 0.07
Nodes (40): main(), Run the lanes, then print what they cost., main(), Run both lanes and print the report, so the scorer can be read before it is…, one_case_view(), A lane holding one arrival, so a transcript is about that mail and nothing…, main(), The eval run as a command, for anyone who would rather not go through the CLI. (+32 more)

### Community 52 - "test_graph.py"
Cohesion: 0.25
Nodes (15): Walk a lane through the graph, one decision per checkpoint thread., run_graph(), Path, The graph is not a second opinion: same proposals, same route, same receipts., runtime(), test_a_case_the_lane_does_not_hold_fails_with_its_name(), test_a_decision_the_floor_fences_waits_on_nothing(), test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing() (+7 more)

### Community 53 - "classify_action"
Cohesion: 0.18
Nodes (13): classify_action(), _extract_recipients(), _has_credential_intent(), _has_financial_intent(), _is_external_address(), Any, Extract and normalize all recipient addresses from action parameters., Return True if email_address domain does not match user_domain. (+5 more)

### Community 54 - "OpenAICompatibleProvider"
Cohesion: 0.13
Nodes (14): _attribute(), Endpoint, OpenAICompatibleProvider, Any, An OpenAI-compatible endpoint's settings., How a run reports which model it used., A model behind an OpenAI-compatible API. Used only when a key is configured., Which model a run is actually talking to. (+6 more)

### Community 55 - "Block"
Cohesion: 0.18
Nodes (8): Block, classify(), Any, Append one block, with the number the page polls from., Every block the page has not seen yet., One chunk of the run's output, as the page shows it., What the page should make of one chunk: mail, a wait, a typed line, the summary., test_blocks_are_classified_for_the_page()

### Community 56 - "ScopeAnchor"
Cohesion: 0.11
Nodes (33): preference_for(), The scoped preference a confirmed rule would leave behind for this sender.…, ClaimType, StrEnum, What kind of thing the user told us. Each still needs its evidence., How the claim's scope was arrived at, which is what its confidence means., ScopeAnchor, The constrained feedback parser, the scope echo, and what a claim has to be to… (+25 more)

### Community 57 - "interrupting_case_ids"
Cohesion: 0.20
Nodes (12): interrupting_case_ids(), CaptureFixture, MonkeyPatch, A piped stream has no prompt to answer, so its lines are corrections. Reading…, If the read fails, the prompts must see end of input, not wait forever., Fixture cases whose gold route asks the user, in delivery order., test_a_broken_input_stream_ends_the_run_instead_of_hanging(), test_a_correction_typed_at_a_prompt_binds_to_that_decision() (+4 more)

### Community 58 - "EffectLog"
Cohesion: 0.22
Nodes (4): EffectLog, What each step of each prepared action has already done. Keyed by the prepared…, One step of one exact action: the same digest and position is the same work., What this step did, if it already ran.

### Community 59 - "scan"
Cohesion: 0.08
Nodes (26): _check_authority_claims(), _check_base64_injection(), _check_zero_width_chars(), _decode_base64_candidate(), _names_its_own_domain(), Return the decoded text of a base64 candidate, or None when it is not valid…, Inspect text for embedded base64 payloads that decode into control instructions., Detect presence of invisible zero-width characters used for steganography. (+18 more)

### Community 60 - "TraceSink"
Cohesion: 0.24
Nodes (6): RuntimeError, The trace could not be written where it was asked to go., Append-only JSONL trace, one line per decision, flushed as it is written., Close the file. Safe to call twice, which an except-block may do., TraceError, TraceSink

### Community 61 - "Message"
Cohesion: 0.05
Nodes (54): Walk both lanes with nobody at the keyboard, and score what they did. Input is…, run_two_lanes(), _domain(), proposal_from(), One claim as a proposal, or None when the claim names no route., Answer from a claim where one bears on this mail, otherwise ask the inner one., The confirmed claim that bears on this mail and names a route, if one does., What the user's own words amount to for this mail, if anything. (+46 more)

### Community 62 - "ModelUser"
Cohesion: 0.25
Nodes (6): ModelUser, Queue, The person whose mailbox this is, played by a model that is not the proposer.…, The lines to hand the waiting decision: the reply, and a confirmation if…, Whether the draft on the table may be saved. Nothing is approved by default., The runner's interrupt hook: the waiting decision gets its lines from the model.

### Community 63 - "test_triage.py"
Cohesion: 0.15
Nodes (16): guesses(), manifest(), message(), fixture, Deterministic pre-triage: mail-only, deterministic, and measured against the…, An AWS invoice says a payment is due; it is still a bill, not a wire request., The classifier's input is a Message, so a label cannot be an input. Feeding it…, test_a_cloud_invoice_is_not_read_as_a_payment_request() (+8 more)

### Community 65 - "first_interrupt_of"
Cohesion: 0.24
Nodes (10): first_interrupt_of(), gold_route(), The interrupt number and case id of the first arrival with this gold route., Answer the prompts before ``position`` with a blank line, then type ``lines``.…, A yes at an ASK prompt is both the release and the reward the learner counts., Nothing was prepared, so a bare yes is not an approval to credit., test_a_policy_line_is_stored_only_once_it_is_confirmed(), test_an_approval_at_an_escalation_decides_nothing() (+2 more)

### Community 66 - "ask_curve"
Cohesion: 0.25
Nodes (6): ask_curve(), Block, The interruption curve: how many cases each block of the lane needed the user…, One block of a lane, in delivery order, and how much of it asked for the user., Blocks are the stream's own order, and four cases at block 12 is one block of…, test_the_curve_blocks_the_lane_in_delivery_order_and_the_last_block_may_be_short()

### Community 67 - "test_cases.py"
Cohesion: 0.06
Nodes (62): CaseReport, DatasetProblem, One thing the case set gets wrong, named so it can be found and fixed., What the case set holds and whatever is wrong with it. ``ok`` is about problems…, The report as a reader sees it: counts first, then what fails., Read a dotted path out of a row, or the default when any step is absent., The scenario a rule would be scoped to: who sent it, and about what. Sender…, Check one row's fields and enums. Returns its problems and its warnings. (+54 more)

### Community 68 - "_background_loop"
Cohesion: 0.29
Nodes (5): AbstractEventLoop, _background_loop(), Hand a typed line to the run that is waiting for one., End the run the way end of input does: nothing else is approved., One event loop for the process, running on its own thread. HTTP handlers arrive…

### Community 69 - "main"
Cohesion: 0.18
Nodes (11): data_validate(), main(), Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard., Print what a case set holds and everything wrong with it., Entry point for the ``wajo`` console script., sandbox_run_command(), CaptureFixture, MonkeyPatch (+3 more)

### Community 70 - "._line"
Cohesion: 0.33
Nodes (4): _json_default(), Any, A stable hash of the replay log., The canonical JSONL replay log: header line, then one line per arrival.

### Community 71 - "test_benign_workplace_clean_pass"
Cohesion: 0.29
Nodes (7): parametrize, Verify that every tool and parameter boundary resolves to the exact ActionClass., Everyday emails with natural language must NOT trigger false injection vetoes., Money, credentials and unrecognized tools mask every route except ESCALATE., test_benign_workplace_clean_pass(), test_classify_action_matrix(), test_fenced_actions_leave_escalate_alone()

### Community 72 - "test_replay.py"
Cohesion: 0.06
Nodes (32): manifest(), fixture, Unit tests for deterministic replay and the split firewall (Phase 3.2). Covers:…, The plan's check: two same-seed runs emit identical event logs., The seed is load-bearing, so it has to show up in the artifact., One header line, then one parseable line per arrival., The log's order is the dataset's sequence order, not file order., Counts per split and per lane, with the dataset's real sizes. (+24 more)

### Community 73 - "Router"
Cohesion: 0.07
Nodes (55): Learner, How many explicit decisions have been counted into a posterior., How many arms the user has refused outright., Counts what the user said into posteriors, once per event, never from silence.…, The constrained argmin, in the plan's fixed order. Floor mask, then claims,…, Choose one route for one arrival., Whether this route is on the ballot at all: the cautious ones always are., Everything the router is allowed to consider for one arrival. (+47 more)

### Community 74 - "test_graph_state.py"
Cohesion: 0.18
Nodes (15): message(), Path, The body and subject are inputs to the decision, and must not reach the file., No line may contain these words, in a key or in a value., Error handling at the boundary: a path that is not a file names itself., The run that dies is the one worth tracing, so lines are flushed as written., What the checkpointer serialises is what it reads back, unchanged., test_a_long_text_is_a_digest_and_a_short_one_is_not() (+7 more)

### Community 75 - "test_sim.py"
Cohesion: 0.23
Nodes (17): build_reply_tree(), Reconstruct the reply tree for a thread, bounded by depth and node caps.…, decision_sources(), message(), Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction., Which decision source produced the routes in a labelled run., A minimal message for tree tests; ``minutes=None`` means no timestamp., test_bad_caps_and_empty_threads_are_rejected() (+9 more)

### Community 76 - "_server"
Cohesion: 0.33
Nodes (7): _call(), Any, Path, The real handler on a free port, imported the way the entry point runs it., One call to the page's server: a body makes it a POST, no body a GET., _server(), test_the_page_is_served_and_can_drive_a_session()

### Community 77 - "Any"
Cohesion: 0.18
Nodes (10): Arrival, _case_blocks(), _preview(), Any, One generated mail, with the brief and the writer's own opinion that produced…, The mail in the loader's own shape. It carries no labels, because it has none., What the run keeps beside the row: which brief wrote it, and what it expected., The arrivals of the half the agent had never seen, in delivery order. (+2 more)

### Community 78 - "ProposalError"
Cohesion: 0.10
Nodes (14): ProposalError, ProposalRequest, RuntimeError, Raised when a provider cannot produce a usable proposal, after one repair., Everything a provider is allowed to see: the mail, plus what triage inferred., The request rendered for a text model. The mail is the only input., Return raw proposal text for one request., Ask once. A provider that fails in any way is a failed proposal, not a crash. A… (+6 more)

### Community 79 - "SandboxError"
Cohesion: 0.15
Nodes (12): parse_generated(), RuntimeError, Raised when the environment cannot be built or read., One situation to write a mail about, and how a careful assistant would treat it., Read one generated mail, naming what is wrong rather than guessing a field., SandboxError, Scenario, FakeModel (+4 more)

### Community 80 - "test_loop.py"
Cohesion: 0.09
Nodes (27): _answered_cases(), InterruptHook, IO, Queue, Calibrate on a lane, then walk the same lane with the rules it produced. Two…, Each arrival a rule answered, mapped to the arrival whose mail taught that rule., Types scripted lines at the decisions that wait for a human. A line handed over…, A hook that hands the waiting decision its lines, and closes input at the end. (+19 more)

### Community 81 - "server.py"
Cohesion: 0.25
Nodes (8): dotenv, main(), Serve the calibration page. uv run python frontend-ui/server.py Standard…, Start the server, ready to be run by the caller., serve(), http_server, ThreadingHTTPServer, webbrowser

### Community 83 - "Lane"
Cohesion: 0.08
Nodes (60): calibration_report(), held_out_report(), LaneRecord, What one lane run recorded, in the shape the report reads. Built from a chat…, Read a chat run: its per-case routes, what it asked, and what the user typed., Read a graph run, including the floor's ballot and who authorised each commit., Score the calibration lane: the dispositions, the typings and the ask curve., Score the sealed lane, refusing outright if anything about it could teach. Both… (+52 more)

### Community 87 - "autonomy/state.py"
Cohesion: 0.10
Nodes (23): Cutoffs, The posterior mean a route's bucket needs before the route may be considered., After an approval: easier to earn, down to the calibration floor., After a revert or a rejection: harder to earn, capped at certainty., Per-bucket cutoffs, adapted by explicit feedback (plan 4.3). Read through the…, The cutoffs this bucket is judged by, most specific first., Move this bucket's cutoffs by one explicit decision., ThresholdStore (+15 more)

### Community 88 - "Route"
Cohesion: 0.12
Nodes (27): One reference case: the mail, what it is here to show, and the route it…, The route the run actually chose., Scenario, How many arrivals took each of the four routes., Costs, Loss, pick(), The cheapest route. Ties go to the more cautious one, so a tie never buys… (+19 more)

### Community 98 - "Predraft"
Cohesion: 0.33
Nodes (4): Predraft, A reply, written but not sent, with its facts and its gaps. The case id rides…, The draft as a human should see it before approving anything., The draft this ask shows, or None when it shows none.

### Community 102 - "datetime"
Cohesion: 0.33
Nodes (3): datetime, Whether this consent still stands at a moment., One line a transcript can print about why nothing was kept.

### Community 104 - "LoopReport"
Cohesion: 0.14
Nodes (8): LoopReport, Decisions that would still wait for a human, with the rules in front., Decisions the same lane waits on with nothing remembered, or 0 with no control., Arrivals a rule sent somewhere else than the lane would have gone on its own., Of those, the arrivals that came after the mail their rule was taught on. This…, Asking the rules took off the user, measured against the lane with no rules.…, One lane, walked with a baseline pipeline and with what the user said during it., Decisions the chat pass waited on. Not a baseline: a rule takes effect from the…

### Community 105 - ".labels"
Cohesion: 0.50
Nodes (3): CaseLabels, The dataset's ground truth for a case. These are answers: what the case was…, The dataset's answer for this case, for scoring and debugging only.

### Community 106 - "_order_key"
Cohesion: 0.50
Nodes (4): _order_key(), _ordered_roots(), Every thread root, asked-for first, the rest in a deterministic order. A root…, A total order over messages: dated first, then undated, then by id. Thread…

### Community 107 - "run_sandbox"
Cohesion: 0.11
Nodes (22): _banner(), _blocks(), Judge, _judge_run(), _judged(), Judgement, _note(), IO (+14 more)

### Community 108 - "run_simulation"
Cohesion: 0.23
Nodes (12): close_input(), Any, DecisionSource, InterruptHook, IO, Queue, Tell a scripted run that no further lines are coming (EOF)., Read stdin without blocking the event loop. (+4 more)

### Community 111 - "write_mailbox"
Cohesion: 0.22
Nodes (10): generator_prompt(), Random, The request for one arrival. Everything fresh about it comes from this frame., A plain-text caller for one model role, or a named failure when it has no…, Write `count` fresh arrivals, cycling the briefs in a shuffled order. A…, How long a model call took, in the unit a reader cares about., _seconds(), text_call() (+2 more)

### Community 114 - ".save"
Cohesion: 0.33
Nodes (3): datetime, Write every claim to the store's file, one JSON object per line. The whole…, The reason this store may not read or write its file at this moment, or ''.

### Community 117 - "RememberedProvider"
Cohesion: 0.09
Nodes (22): Protocol, The user's own words, consulted before the provider. Wraps another provider:…, The pair's name, so a run says where a proposal could have come from., Whichever provider actually answers, named the way a run names it., How many arrivals a confirmed claim answered., RememberedProvider, ProposalProvider, A source of untrusted proposal text. (+14 more)

### Community 118 - "evaluate"
Cohesion: 0.10
Nodes (31): RuntimeError, Refuse a record whose counts cannot add up to what the run processed., Raised when a run cannot be scored as asked, rather than scored wrongly., ScoringError, evaluate(), _frozen(), load_script(), Any (+23 more)

### Community 121 - "safety/__init__.py"
Cohesion: 0.12
Nodes (16): _eval_plan_deviation(), FloorRule, Representation of an audited, immutable safety floor rule., FLR-INJ-002: Actions deviating from pre-committed plan must be escalated., Safety module: floor guardrails, action taxonomy, and injection tripwires., InjectionScanResult, plan_deviation(), Any (+8 more)

### Community 129 - "floor_check"
Cohesion: 0.13
Nodes (21): EmailContext, floor_check(), Email metadata and body context passed into safety evaluations.…, Evaluate a proposed action against the deterministic safety floor. Returns the…, The least autonomous route the floor left open, which is the fail-closed one., strictest_allowed(), FLR-001: Money requests in email body cannot trigger non-reversible actions., Load tests/adversarial_cases.yaml and verify 100% are vetoed with ESCALATE. (+13 more)

### Community 130 - "dispositions"
Cohesion: 0.15
Nodes (9): Disposition, dispositions(), How a lane's cases were handled, mutually exclusive by construction., The counts, then the denominator they have to add up to., Count routes into the three dispositions, refusing a route nobody defined., The plan's rule: three dispositions, one per case, adding up to all of them., A fifth route is a bug, and an uncounted case is the same bug wearing a number., test_a_route_the_report_does_not_know_is_refused_rather_than_counted() (+1 more)

## Knowledge Gaps
- **14 isolated node(s):** `ROUTES`, `CHOICES`, `email-autonomy-agent`, `graphify`, `Steps` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Route` connect `Route` to `runner.py`, `dispositions`, `floor_check`, `registry.py`, `test_economics.py`, `feedback.py`, `test_floor.py`, `ClaimScope`, `ChatRunner`, `test_jev.py`, `SandboxOutcome`, `test_sandbox.py`, `CalibrationReport`, `cli.py`, `ProposalGateway`, `_receipt_route`, `VetoLevel`, `test_sim_tools.py`, `agent/state.py`, `jev.py`, `ActionPayload`, `test_predrafts.py`, `FeedbackKind`, `test_events.py`, `Session`, `run_typed`, `claims.py`, `pytest`, `arrivals`, `Manifest`, `classify_action`, `ScopeAnchor`, `interrupting_case_ids`, `Message`, `first_interrupt_of`, `test_cases.py`, `test_benign_workplace_clean_pass`, `Router`, `SandboxError`, `Lane`, `RememberedProvider`, `safety/__init__.py`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `Router` connect `Router` to `GraphSession`, `runner.py`, `Posterior`, `graph.py`, `FeedbackKind`, `Bucket`, `run_sandbox`, `ChatRunner`, `run_simulation`, `pytest`, `test_loop.py`, `cli.py`, `test_graph.py`, `RememberedProvider`, `evaluate`, `autonomy/state.py`, `Route`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `Learner` connect `Router` to `runner.py`, `FeedbackKind`, `ClaimStore`, `Bucket`, `LoopReport`, `Session`, `run_sandbox`, `ChatRunner`, `claims.py`, `ClaimScope`, `run_simulation`, `test_loop.py`, `pytest`, `graph_run`, `cli.py`, `RememberedProvider`, `evaluate`, `autonomy/state.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 164 inferred relationships involving `Route` (e.g. with `dispositions()` and `held_out_report()`) actually correct?**
  _`Route` has 164 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `Lane` (e.g. with `main()` and `CalibrationReport`) actually correct?**
  _`Lane` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Are the 37 inferred relationships involving `Router` (e.g. with `cold_control()` and `run_scenario()`) actually correct?**
  _`Router` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `Learner` (e.g. with `run_scenario()` and `_frozen()`) actually correct?**
  _`Learner` has 31 INFERRED edges - model-reasoned connections that need verification._