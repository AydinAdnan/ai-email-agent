"""Concurrent chat-style simulator loop (Phase 3.4, arrivals scheduled by 3.5).

Two tasks run at once: an arrival task that walks the lane window by window, and a
stdin task that keeps reading lines. The arrival task blocks only when a route needs the
user (ASK_FIRST_WITH_PREDRAFT or ESCALATE); SILENT and NOTIFY never wait, even if the
user has already queued something to say.

Arrivals are ordered by :mod:`agent.sim.schedule`: the lane is cut into windows of ten
and the order inside a window is drawn from the run's seed, so a session arrives the way
an inbox does rather than in dataset order. Delivery order is the stream's order, so an
arrival takes its delivered position as its ``sequence_index`` - the row keeps the
dataset's own index, which is what a case's provenance means.

Arrivals are printed the way an inbox presents mail - sender, recipients, subject,
body, thread - and never with the dataset's labels, unless ``show_labels`` is on.
Sender, subject and body are what a production agent gets; intent, relationship class
and the gold route are what Phase 8 scores it against, and printing those in front of
whoever is calibrating would let the answer key steer them.

A line is interpreted by when it was typed:

- while a decision is waiting for an answer, the next line is the answer;
- lines already handed over when the next arrival is processed are free-text
  corrections bound to the decision they followed, so "this/that sender" resolves to
  that decision's sender. A pipe has no prompt to answer, so everything it buffers is
  read this way rather than being pinned on whichever case is prompting when it drains.

Unparsed input is recorded as ``FeedbackKind.NONE`` with
``explicit_for_learning=False``: a line nobody has parsed yet, and silence at the end
of input, must never reach the learner. Commit 3.6 replaces that with the constrained
parser and its scope echo.
"""
import asyncio
import sys
import textwrap
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import IO, Any

from agent.autonomy.bandit import Learner
from agent.autonomy.confidence import Bucket
from agent.autonomy.router import Router
from agent.dataset import Case, LaneView
from agent.events import FeedbackEvent, FeedbackKind, SenderIdentity, is_learnable
from agent.gateway import NO_ACTION_TOOL
from agent.learning.feedback import (
    FeedbackContext,
    Reading,
    confirm_claim,
    read_feedback,
)
from agent.memory.claims import Claim, ClaimStore
from agent.memory.consent import ConsentRequired, session_grant
from agent.replay import EventStream, SeededClock
from agent.safety.floor import Route
from agent.sim.policy import (
    INTERRUPTING_ROUTES,
    Decision,
    GoldPolicy,
    ProposalPolicy,
    quietenable,
)
from agent.sim.reply_tree import ReplyTree, build_reply_tree
from agent.sim.schedule import WINDOW_SIZE, Window, schedule
from agent.state import (
    GraphState,
    hint_fields,
    message_digest,
    prepared_fields,
    receipt_fields,
    routing_fields,
    verdict_fields,
)
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.tools.registry import (
    Approval,
    ApprovalRequired,
    AuthorizationRefused,
    PreparedAction,
    Receipt,
    ToolRegistry,
)
from agent.trace import TraceSink

DecisionSource = ProposalPolicy | GoldPolicy


class SimError(RuntimeError):
    """Raised when a run cannot continue, naming the case it stopped on."""


InterruptHook = Callable[[int, Decision], Awaitable[None]]
_INPUT_CLOSED = object()

# How long to let the input task hand over lines already typed before deciding that
# the user is waiting rather than mid-sentence. Long enough for a buffered line to
# arrive, far too short for a human to answer a prompt that has not been shown yet.
_INPUT_SETTLE_SECONDS = 0.01


def thread_tree_for(case: Case) -> ReplyTree:
    """Reconstruct one case's thread, bounded by the reply-tree caps."""
    messages = (case.event.message, *case.event.thread.messages_before)
    known = {message.message_id for message in messages}
    parent_id = case.event.thread.parent_message_id
    return build_reply_tree(messages, root_id=parent_id if parent_id in known else None)


@dataclass
class SimOutcome:
    """What one simulator run did."""

    processed: int = 0
    interrupts: int = 0
    replies: int = 0
    corrections: int = 0
    silent_ends: int = 0
    route_counts: dict[str, int] = field(default_factory=dict)
    feedback: list[FeedbackEvent] = field(default_factory=list)
    replay_digest: str = ""
    receipts: list[Receipt] = field(default_factory=list)
    # Prepared but not committed: an ASK route waits for an approval only the user can
    # give, and a confirmed approval releases it through the digest-bound contract.
    awaiting_approval: list[PreparedAction] = field(default_factory=list)
    refusals: list[str] = field(default_factory=list)
    # Rules the user confirmed during the run. Nothing reaches here unconfirmed.
    claims: list[Claim] = field(default_factory=list)
    # Of the prompts this run asked, how many a rule the user could state would take off
    # their screen. The rest are kept by the mail itself, and no rule changes them.
    quietenable: int = 0

    @property
    def learnable_feedback(self) -> tuple[FeedbackEvent, ...]:
        """Feedback a learner would accept, which is nothing until Commit 3.6."""
        return tuple(item for item in self.feedback if item.explicit_for_learning)

    def effects(self, tool: str) -> int:
        """How many times a tool actually ran, counted from the receipts."""
        return sum(
            1
            for receipt in self.receipts
            for effect in receipt.effects
            if effect.tool == tool
        )


class ChatRunner:
    """Drive a lane through the chat loop: arrivals on one task, input on another."""

    def __init__(
        self,
        view: LaneView,
        *,
        seed: int = 7,
        out: IO[str] | None = None,
        policy: DecisionSource | None = None,
        input_queue: asyncio.Queue[Any] | None = None,
        on_interrupt: InterruptHook | None = None,
        show_labels: bool = False,
        mailbox: SimulatedMailbox | None = None,
        registry: ToolRegistry | None = None,
        store: ClaimStore | None = None,
        learner: Learner | None = None,
        router: Router | None = None,
        window: int = WINDOW_SIZE,
        trace: TraceSink | None = None,
    ) -> None:
        self.view = view
        self.seed = seed
        self.window = window
        self.windows: tuple[Window, ...] = schedule(view.cases, window=window, seed=seed)
        self.out = out if out is not None else sys.stdout
        self.policy: DecisionSource = policy if policy is not None else ProposalPolicy()
        self.queue: asyncio.Queue[Any] = input_queue if input_queue is not None else asyncio.Queue()
        self.on_interrupt = on_interrupt
        self.show_labels = show_labels
        self.mailbox = mailbox if mailbox is not None else SimulatedMailbox()
        self.registry = registry if registry is not None else build_registry(self.mailbox)
        self.stream = EventStream(SeededClock(seed=seed))
        self.outcome = SimOutcome()
        # The posteriors this session moves. A run that keeps nothing has no learner at all.
        self.learner = learner
        # The router reads those posteriors and the refusals beside them; a run given no
        # router routes with a cold one, which is the persona's own rules and no more.
        self.router = router if router is not None else Router(learner)
        self.closed = False
        self.last_decision: Decision | None = None
        self.input_error: str | None = None
        # Why the last decision is waiting, from the code the registry raised: an ASK is
        # work to release, an escalation is a call nobody but the user can make.
        self.wait_code = ""
        # The prepared action an approval would release, and the rules the user confirmed.
        self.pending: PreparedAction | None = None
        # A calibration session is a human present and answering, so it carries consent
        # for the session's own purpose and nothing wider. A run without that consent
        # hears the same lines and keeps none of them.
        self.store = (
            store
            if store is not None
            else ClaimStore(grant=session_grant(purpose="calibration session"))
        )
        # The last case's work, kept so the trace line can name what was prepared and
        # what was committed without the arrival block having to thread it back up.
        self.last_prepared: PreparedAction | None = None
        self.last_receipt: Receipt | None = None
        self.trace = trace

    async def run(self) -> SimOutcome:
        """Deliver every case in the lane, window by window, in the order the seed drew."""
        deliveries = tuple(case for item in self.windows for case in item.cases)
        self._emit(
            f"schedule: {len(deliveries)} cases in {len(self.windows)} window(s) of up to "
            f"{self.window}, order drawn from seed {self.seed}"
        )
        for index, case in enumerate(deliveries, start=1):
            await self._absorb_corrections()
            decision = await self._decide(case, delivered=index)
            tree = thread_tree_for(case)
            outcome_line = self._act(decision)
            self._emit(
                self._arrival_block(index, len(deliveries), case, decision, tree, outcome_line)
            )
            self._trace("decision", case, decision, delivered=index)
            if decision.interrupts:
                feedback = len(self.outcome.feedback)
                claims = len(self.outcome.claims)
                await self._handle_interrupt(index, decision, tree)
                self._trace(
                    "reply",
                    case,
                    decision,
                    delivered=index,
                    feedback=self.outcome.feedback[feedback:],
                    claims=self.outcome.claims[claims:],
                )

        self.outcome.processed = len(deliveries)
        self.outcome.replay_digest = self.stream.digest()
        self._summarise()
        return self.outcome

    async def _decide(self, case: Case, *, delivered: int) -> Decision:
        try:
            decision = await self.policy.decide(case, router=self.router)
        except Exception as error:
            # A traceback that does not name the case is a bug hunt, not a bug report.
            raise SimError(
                f"case {case.case_id} could not be decided: {type(error).__name__}: {error}"
            ) from error
        # The stream's order is delivery order, and the windowed schedule is what decides
        # it, so the arrival is recorded at the position it arrived.
        self.stream.append(replace(case.event, sequence_index=delivered))
        self.last_decision = decision
        counts = self.outcome.route_counts
        counts[decision.route.value] = counts.get(decision.route.value, 0) + 1
        return decision

    def _act(self, decision: Decision) -> str:
        """Prepare the decision's steps, authorize them, and commit what may run.

        Preparing validates without touching anything, so an action that will never be
        authorized - every ASK, every escalation - leaves the mailbox exactly as it was.
        """
        self.wait_code = ""
        self.pending = None
        self.last_prepared = None
        self.last_receipt = None
        case = self.view.open(decision.case_id)
        prepared = self.registry.prepare(
            case_id=decision.case_id,
            message_id=case.event.message.message_id,
            route=decision.route,
            action_id=decision.action_id,
            tool_name=None if decision.tool_name == NO_ACTION_TOOL else decision.tool_name,
            params=decision.params,
        )
        self.last_prepared = prepared
        try:
            authorization = self.registry.authorize(
                prepared, verdict_routes=decision.verdict.allowed_routes
            )
        except ApprovalRequired as waiting:
            # An approval only the user can give, which the reply parser reads.
            self.wait_code = waiting.code
            self.pending = prepared
            self.outcome.awaiting_approval.append(prepared)
            self.outcome.refusals.append(f"{decision.case_id}: {waiting}")
            return f"prepared {prepared.summary()} [{waiting.code}: {_REFUSAL_WORDS[waiting.code]}]"
        except AuthorizationRefused as refusal:
            # Escalation: a human decides, so there is nothing to wait for here.
            self.wait_code = refusal.code
            self.outcome.refusals.append(f"{decision.case_id}: {refusal}")
            return f"nothing prepared [{refusal.code}: {_REFUSAL_WORDS[refusal.code]}]"

        receipt = self.registry.commit(prepared, authorization, at=self.stream.clock.now())
        self.outcome.receipts.append(receipt)
        self.last_receipt = receipt
        return f"{receipt.receipt_id} {receipt.summary()}"

    def _trace(
        self,
        event: str,
        case: Case,
        decision: Decision,
        *,
        delivered: int,
        feedback: Sequence[FeedbackEvent] = (),
        claims: Sequence[Claim] = (),
    ) -> None:
        """One line per decision, and one per reply: ids, hashes, bounded records."""
        if self.trace is None:
            return
        message = case.event.message
        state: GraphState = {
            "case_id": case.case_id,
            "message_id": message.message_id,
            "thread_id": message.thread_id,
            "lane": self.view.lane.value,
            "sequence_index": delivered,
            "message_digest": message_digest(message),
            "dataset_digest": self.view.manifest.dataset_digest,
            "replay_seed": self.seed,
            "hints": hint_fields(decision.hints),
            "proposal": {
                "source": decision.source,
                "route": decision.route.value,
                "action_id": decision.action_id,
                "reason": decision.reason,
            },
            "floor": verdict_fields(decision.verdict),
            "routing": routing_fields(decision.routing),
            "route": decision.route.value,
            "action_id": decision.action_id,
            "prepared": prepared_fields(self.last_prepared),
            "receipt": receipt_fields(self.last_receipt),
            "interrupt": {"code": self.wait_code} if self.wait_code else {},
            "feedback": [item.event_id for item in feedback],
            "claims": [claim.claim_id for claim in claims],
            "node": "sim",
        }
        self.trace.write(event, state, at=self.stream.clock.now())

    async def _handle_interrupt(self, index: int, decision: Decision, tree: ReplyTree) -> None:
        self.outcome.interrupts += 1
        self._emit(f"  {_WAIT_WORDS.get(self.wait_code, '[waiting] this one is yours')}")
        # Whether a rule could take this one off the user's screen is the question they are
        # about to answer by typing, so it is answered for them first. A mail the persona
        # has demanded escalation for is not a mail any rule can quieten, and typing one at
        # it teaches nothing.
        could_quiet = quietenable(self.view.open(decision.case_id))
        self.outcome.quietenable += 1 if could_quiet else 0
        if not could_quiet:
            self._emit(
                "        no rule quietens this one: it stays your call, so decide it here"
            )
        if self.on_interrupt is not None:
            await self.on_interrupt(index, decision)

        answer = await self._next_line()
        if answer is None:
            self.outcome.silent_ends += 1
            self._emit("        no reply before end of input (silence is not approval)")
            return

        self.outcome.replies += 1
        self._emit(f"        reply for {decision.case_id}: {answer!r}")
        reading = read_feedback(
            answer, context=self._feedback_context(decision), recorded_at=self.stream.clock.now()
        )
        self._emit(f"        {reading.echo}")
        if reading.claim is not None:
            await self._settle(reading, decision)
            return
        if reading.kind is FeedbackKind.APPROVE and self.wait_code == ApprovalRequired.code:
            self._record(answer, decision.case_id, kind=reading.kind)
            self._release(decision)
            return
        if reading.kind in {FeedbackKind.APPROVE, FeedbackKind.REJECT}:
            # Nothing was prepared for this one, so a bare yes or no did not decide
            # anything: saying it did would credit the wrong arm later.
            self._emit(
                "        nothing was prepared for this one, so that decided nothing"
                " - say what to do instead, e.g. 'always escalate these'"
            )
            self._record(answer, decision.case_id)
            return
        self._record(answer, decision.case_id, kind=reading.kind)

    async def _settle(self, reading: Reading, decision: Decision) -> None:
        """Ask the one bounded question and store the rule only if it is confirmed."""
        self._emit(f"        {reading.prompt}")
        answer = await self._next_line()
        if answer is None:
            self._emit("        no answer before end of input; nothing was stored")
            return
        claim = confirm_claim(
            reading.claim,
            answer,
            context=self._feedback_context(decision),
            recorded_at=self.stream.clock.now(),
        )
        if claim is None:
            self._emit("        not confirmed, so nothing was stored as a rule")
            return
        try:
            stored = self.store.store(claim)
        except ConsentRequired as refusal:
            # Heard, understood, and not kept: a session without consent for learning
            # still calibrates, it just remembers nothing.
            self._emit(f"        not stored: {refusal}")
            self._record(
                claim.quote, claim.source_case_id, kind=reading.kind, claim=claim, decision=decision
            )
            return
        self.outcome.claims.append(stored)
        self._record(
            claim.quote, claim.source_case_id, kind=reading.kind, claim=claim, decision=decision
        )
        self._emit(f"        stored {stored.claim_id}: {stored.describe()}")

    def _release(self, decision: Decision) -> None:
        """Commit the work the user just approved, bound to the prepared digest."""
        prepared = self.pending
        if prepared is None:
            return
        try:
            authorization = self.registry.authorize(
                prepared,
                approval=Approval(prepared_digest=prepared.digest, approved_by="user"),
                verdict_routes=decision.verdict.allowed_routes,
            )
        except AuthorizationRefused as refusal:
            self.outcome.refusals.append(f"{decision.case_id}: {refusal}")
            self._emit(f"        could not release it [{refusal.code}]")
            return
        receipt = self.registry.commit(prepared, authorization, at=self.stream.clock.now())
        self.outcome.receipts.append(receipt)
        if prepared in self.outcome.awaiting_approval:
            self.outcome.awaiting_approval.remove(prepared)
        self._emit(f"        released {receipt.receipt_id} {receipt.summary()}")

    def _feedback_context(self, decision: Decision) -> FeedbackContext:
        """What the reply parser may look at: the mail and the decision, never a label."""
        hints = decision.hints
        message = self.view.open(decision.case_id).event.message
        return FeedbackContext(
            case_id=decision.case_id,
            sender=decision.sender,
            intent=hints.intent if hints is not None else "",
            relationship_class=hints.relationship_class if hints is not None else "",
            route=decision.route,
            action_id=decision.action_id,
            subject=message.subject,
            message_id=message.message_id,
        )

    async def _absorb_corrections(self) -> None:
        """Consume lines typed while the previous decision was live.

        The settle first, because a line the user typed while the agent was busy is a
        correction to the decision they just saw; without it the line would sit in
        the buffer and be taken as the answer to the next prompt, a different case.
        """
        await asyncio.sleep(_INPUT_SETTLE_SECONDS)
        for line in self._drain():
            self.outcome.corrections += 1
            target = self.last_decision
            if target is None:
                self._emit(f"        correction recorded before any decision: {line!r}")
                self._record(line, None)
                continue
            self._emit(
                f"        correction bound to {target.case_id} "
                f"(sender {target.sender}): {line!r}"
            )
            self._read_correction(line, target)

    def _read_correction(self, line: str, target: Decision) -> None:
        """Read a line typed while the agent was busy, and say what it read.

        A buffered line is never an answer: it was typed before the prompt it would be
        answering existed, so a plain yes or no is not an approval of this decision and
        nothing is credited to it. A rule needs a confirmation at a prompt, and a
        correction that names the mail stands on its own.
        """
        reading = read_feedback(
            line, context=self._feedback_context(target), recorded_at=self.stream.clock.now()
        )
        self._emit(f"        {reading.echo}")
        if reading.claim is not None:
            self._emit("        it needs a confirmed prompt before it becomes a rule")
            self._record(line, target.case_id, decision=target)
            return
        if reading.kind in {FeedbackKind.APPROVE, FeedbackKind.REJECT}:
            self._emit("        typed before the prompt, so it decided nothing")
            self._record(line, target.case_id, decision=target)
            return
        self._record(line, target.case_id, kind=reading.kind, decision=target)

    def _record(
        self,
        text: str,
        case_id: str | None,
        *,
        kind: FeedbackKind = FeedbackKind.NONE,
        claim: Claim | None = None,
        decision: Decision | None = None,
    ) -> None:
        """Record one line, and count it if an explicit decision may teach the learner."""
        event = FeedbackEvent(
            event_id=f"{case_id or 'unbound'}:input:{len(self.outcome.feedback) + 1}",
            case_id=case_id or "unbound",
            kind=kind,
            explicit_for_learning=is_learnable(kind),
            text=text,
            # What the reading asked for, when it asked for anything: the route is the
            # vote, and the action is the arm a refusal applies to.
            chosen_route=claim.route if claim is not None else None,
            chosen_action_id=claim.action_id if claim is not None else None,
            recorded_at=self.stream.clock.now(),
        )
        self.outcome.feedback.append(event)
        target = decision if decision is not None else self.last_decision
        if self.learner is not None and target is not None:
            bucket = _bucket_of(target)
            # The cutoffs move on the same reading the posterior does, and only when the
            # learner actually counted it: a replayed event teaches neither one twice.
            if self.learner.observe(event, bucket, claim=claim):
                self.router.observe(event, bucket)

    async def pump(self, source: AsyncIterator[str]) -> None:
        """Hand typed lines to the chat, and always close the queue when the read ends.

        The close is in a ``finally`` on purpose: if the read fails and the sentinel
        never arrives, the next prompt waits on a queue no producer will ever feed and
        the session hangs with nothing on screen to say why.
        """
        try:
            async for line in source:
                await self.queue.put(line.rstrip("\n"))
        # An input stream can fail any way it likes; the point is that the session ends
        # loudly instead of waiting on a queue nothing will ever feed.
        except Exception as error:  # noqa: BLE001
            self.input_error = f"{type(error).__name__}: {error}"
            self._emit(f"  input failed, carrying on as if input ended: {self.input_error}")
        finally:
            await close_input(self.queue)

    async def _next_line(self) -> str | None:
        if self.closed:
            return None
        item = await self.queue.get()
        if item is _INPUT_CLOSED:
            self.closed = True
            return None
        return item

    def _drain(self) -> list[str]:
        lines: list[str] = []
        if self.closed:
            return lines
        while True:
            try:
                item = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                return lines
            if item is _INPUT_CLOSED:
                self.closed = True
                return lines
            lines.append(item)

    def _emit(self, text: str) -> None:
        self.out.write(text + "\n")
        self.out.flush()

    def _arrival_block(
        self,
        index: int,
        total: int,
        case: Case,
        decision: Decision,
        tree: ReplyTree,
        outcome_line: str = "",
    ) -> str:
        """The arriving mail the way an inbox shows it.

        Sender, recipients, subject, body and the thread are what a production agent
        gets; the dataset's labels - intent, relationship class, the gold route - are
        what Phase 8 scores it against. Printing those here would let the answer key
        steer whoever is calibrating, so they are behind ``show_labels``.
        """
        message = case.event.message
        lines = [f"[{index:2}/{total}] {case.case_id}"]
        if self.show_labels:
            hints = decision.hints
            if case.labelled:
                labels = case.labels
                lines.append(
                    f"    labels:   dataset_route={labels.autonomy_outcome} "
                    f"dataset_intent={labels.intent!r} "
                    f"relationship={labels.relationship_class!r} dataset_action={labels.action_id}"
                )
            else:
                lines.append("    labels:   none (this input is mail only)")
            pipeline = f"    pipeline: route={decision.route.value} source={decision.source}"
            if hints is not None:
                pipeline += f" intent={hints.intent!r} relationship={hints.relationship_class!r}"
            lines.append(pipeline)
            agreed = (
                "yes" if case.labelled and decision.route.value == case.labels.autonomy_outcome else "no"
            )
            lines.append(
                f"    score:    agree={agreed if case.labelled else 'n/a'} "
                f"floor={decision.verdict.rule_id or '-'} action={decision.action_id} "
                f"{_tree_stats(tree)}"
            )
        lines.append(f"  From:    {_address(message.sender)}")
        lines.append(f"  To:      {', '.join(message.recipients) or '(none)'}")
        if message.cc:
            lines.append(f"  Cc:      {', '.join(message.cc)}")
        lines.append(f"  Subject: {message.subject}")
        lines.append(f"  Thread:  {_thread_context(tree)}")
        for attachment in message.attachments:
            size = f", {attachment.size_bytes} bytes" if attachment.size_bytes else ""
            lines.append(f"  Attach:  {attachment.filename} ({attachment.content_type}{size})")
        lines.extend(_prior_lines(tree, message.message_id))
        lines.append("")
        lines.extend(_body_lines(message.body))
        if outcome_line:
            lines.append(f"  Acted:   {outcome_line}")
        return "\n".join(lines)

    def _summarise(self) -> None:
        self._emit("")
        self._emit("run summary")
        for route in Route:
            self._emit(f"    {route.value:24} {self.outcome.route_counts.get(route.value, 0)}")
        self._emit(
            f"    interrupts={self.outcome.interrupts} replies={self.outcome.replies} "
            f"corrections={self.outcome.corrections} silent_ends={self.outcome.silent_ends}"
        )
        self._emit(
            f"    receipts={len(self.outcome.receipts)} "
            f"awaiting_approval={len(self.outcome.awaiting_approval)} "
            f"refusals={len(self.outcome.refusals)} sends={self.outcome.effects('send_email')}"
        )
        self._emit(
            f"    labels={self.outcome.effects('label')} archives={self.outcome.effects('archive')} "
            f"drafts={self.outcome.effects('create_draft')} "
            f"notifications={self.outcome.effects('notify')}"
        )
        self._emit(f"    claims={len(self.outcome.claims)} learnable_feedback={len(self.outcome.learnable_feedback)}")
        if self.learner is not None:
            store = self.learner.store
            self._emit(
                f"    posteriors: {len(store.contexts())} context(s) of "
                f"{len(store.observed())} level(s) counted, updates={self.learner.updates} "
                f"ignored={self.learner.ignored} refused_arms={self.learner.refusals}"
            )
            for bucket in store.contexts()[:3]:
                self._emit(f"        {bucket.describe()}: {store.posterior(bucket).describe()}")
        self._emit(
            f"    prompts a rule could quieten={self.outcome.quietenable} "
            f"kept by the mail itself={self.outcome.interrupts - self.outcome.quietenable}"
        )
        self._emit(f"    seed={self.seed} replay_digest={self.outcome.replay_digest[:24]}")
        if self.input_error is not None:
            self._emit(f"    input_error={self.input_error}")


# What the screen says while a decision waits, keyed by the code the registry raised.
# An approval is work the user releases; an escalation is a call they own with nothing
# prepared to release. Both carry one "[waiting]" so a transcript greps as one thing,
# and they differ after it because they are not the same question.
_WAIT_WORDS: Mapping[str, str] = {
    "APPROVAL_REQUIRED": "[waiting] approval required: nothing goes out until you say so",
    "AUTHORIZATION_REFUSED": "[waiting] escalated: nothing was prepared, this one is your call",
}

# The default view says what will happen in words, never in the route vocabulary: a
# route name on screen is the answer key leaking back in through the transcript.
_REFUSAL_WORDS: Mapping[str, str] = {
    "APPROVAL_REQUIRED": "waiting for your approval; nothing was changed",
    "AUTHORIZATION_REFUSED": "a human decides this one; nothing was changed",
    "APPROVAL_STALE": "the approval no longer matches the work",
}


def _tree_stats(tree: ReplyTree) -> str:
    """One compact field for the labelled view: reconstructed messages and depth."""
    return f"thread={tree.node_count}n/{tree.max_depth_reached}d{'+' if tree.truncated else ''}"


def _address(sender: SenderIdentity) -> str:
    """The address a reader sees, with its unverified display name left visible."""
    return f"{sender.display_name} <{sender.email}>" if sender.display_name else sender.email


def _thread_context(tree: ReplyTree) -> str:
    """What the bounded thread reconstruction found, next to the mail."""
    context = f"{tree.root.thread_id} ({tree.node_count} message(s), depth {tree.max_depth_reached}"
    if tree.truncated:
        context += ", truncated"
    if tree.orphan_ids:
        context += f", {len(tree.orphan_ids)} with a missing parent"
    return context + ")"


def _prior_lines(tree: ReplyTree, arrival_id: str, width: int = 72) -> list[str]:
    """The earlier messages in the thread, in the order the DFS reconstructed them."""
    lines: list[str] = []
    for message in tree.walk():
        if message.message_id == arrival_id:
            continue
        text = " ".join((message.quoted_text or message.body or "").split())
        snippet = text[:width] + ("..." if len(text) > width else "")
        lines.append(f"  prior:  {message.sender.email}: {snippet or '(no text)'}")
    return lines


def _body_lines(body: str, width: int = 88, limit: int = 40) -> list[str]:
    """Wrap the body for a terminal, without reflowing the line breaks it arrived with."""
    lines: list[str] = []
    for raw in body.splitlines():
        lines.extend(f"    {piece}" if piece else "" for piece in textwrap.wrap(raw, width=width) or [""])
    if len(lines) > limit:
        return [*lines[:limit], f"    ... ({len(lines) - limit} more wrapped lines)"]
    return lines


def _bucket_of(decision: Decision) -> Bucket:
    """The bucket a decision belongs to: the mail's shape, and the work that was proposed."""
    hints = decision.hints
    return Bucket(
        sender=decision.sender,
        intent=hints.intent if hints is not None else "",
        action=decision.action_id or "",
    )


async def close_input(queue: asyncio.Queue[Any]) -> None:
    """Tell a scripted run that no further lines are coming (EOF)."""
    await queue.put(_INPUT_CLOSED)


async def _stdin_lines() -> AsyncIterator[str]:
    """Read stdin without blocking the event loop."""
    while True:
        line = await asyncio.to_thread(sys.stdin.readline)
        if not line:
            return
        yield line


async def run_simulation(
    view: LaneView,
    *,
    seed: int = 7,
    out: IO[str] | None = None,
    input_queue: asyncio.Queue[Any] | None = None,
    on_interrupt: InterruptHook | None = None,
    policy: DecisionSource | None = None,
    show_labels: bool = False,
    mailbox: SimulatedMailbox | None = None,
    window: int = WINDOW_SIZE,
    trace: TraceSink | None = None,
    store: ClaimStore | None = None,
    learner: Learner | None = None,
    router: Router | None = None,
) -> SimOutcome:
    """Replay a lane through the chat loop, blocking only where the plan says to.

    Pass an ``input_queue`` to drive the run from code (tests) instead of stdin, then
    ``await close_input(queue)`` when the scripted lines run out.
    """
    runner = ChatRunner(
        view,
        seed=seed,
        out=out,
        policy=policy,
        input_queue=input_queue,
        on_interrupt=on_interrupt,
        show_labels=show_labels,
        mailbox=mailbox,
        window=window,
        trace=trace,
        store=store,
        learner=learner,
        router=router,
    )
    pump: asyncio.Task[None] | None = None
    if input_queue is None:
        pump = asyncio.create_task(runner.pump(_stdin_lines()))
    try:
        return await runner.run()
    finally:
        if pump is not None:
            pump.cancel()


__all__ = [
    "INTERRUPTING_ROUTES",
    "ChatRunner",
    "InterruptHook",
    "SimError",
    "SimOutcome",
    "close_input",
    "run_simulation",
    "thread_tree_for",
]
