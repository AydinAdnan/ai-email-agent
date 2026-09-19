"""What a run spent: calls, tokens and estimated cost, by stage.

The meter sits where the money leaves - the provider - so every call the pipeline makes
lands in it, including the one repair attempt, and including the offline rules provider,
whose calls are counted and cost nothing rather than hidden. Beside that it counts the
arrivals the pipeline settled before asking anyone: pre-triage is not free, it is what
keeps the model calls few, and a deflection rate is the only number that shows it.

Two honesty rules. A model with no published rate is reported as unpriced rather than as
free, because an invented number is worse than a missing one. And a total is the total of
what was priced, with the unpriced rows named next to it.

    uv run python -m evals.economics
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

# Published rates in USD per million tokens, as (input, output). A model absent from this
# table is unpriced, not free, and the table says so.
PRICES: Mapping[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    "inference-net/schematron-v2-small": (0.05, 0.23),
    "inference-net/schematron-v2-turbo": (0.03, 0.15),
    # The sandbox's two roles, at the rates the provider's own catalogue publishes.
    "prism-ml/ternary-bonsai-2-27b": (0.075, 0.50),
    "~deepseek/deepseek-flash-latest": (0.135, 0.54),
}


@dataclass
class Spend:
    """One row: what one stage spent with one model."""

    stage: str
    provider: str
    model: str
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def cost(self) -> float | None:
        """The estimated cost, or None when this model has no published rate.

        A call that reported no tokens costs nothing whatever the model's rate, so an
        offline provider is priced at zero rather than left unpriced.
        """
        if self.tokens == 0:
            return 0.0
        rate = PRICES.get(self.model)
        if rate is None:
            return None
        per_input, per_output = rate
        return (self.prompt_tokens * per_input + self.completion_tokens * per_output) / 1_000_000


@dataclass
class Ledger:
    """A process's spend: every provider call, and every arrival it never had to ask about."""

    spends: dict[tuple[str, str, str], Spend] = field(default_factory=dict)
    arrivals: int = 0
    deflected: int = 0

    def arrival(self, *, deflected: bool = False) -> None:
        """One case reached the proposal stage. A deflected one was settled without a call."""
        self.arrivals += 1
        if deflected:
            self.deflected += 1

    def record(
        self,
        *,
        stage: str,
        provider: str,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
    ) -> Spend:
        """One provider call, with whatever token counts its response reported."""
        row = self.spends.setdefault((stage, provider, model), Spend(stage, provider, model))
        row.calls += 1
        row.prompt_tokens += max(0, int(prompt_tokens))
        row.completion_tokens += max(0, int(completion_tokens))
        return row

    @property
    def calls(self) -> int:
        return sum(row.calls for row in self.spends.values())

    @property
    def tokens(self) -> int:
        return sum(row.tokens for row in self.spends.values())

    @property
    def cost(self) -> float:
        """The priced cost. Unpriced rows are excluded, and named by ``unpriced``."""
        return sum(row.cost or 0.0 for row in self.spends.values())

    @property
    def unpriced(self) -> tuple[Spend, ...]:
        return tuple(row for row in self.spends.values() if row.calls and row.cost is None)

    @property
    def deflection_rate(self) -> float:
        return 0.0 if not self.arrivals else self.deflected / self.arrivals

    def rows(self) -> tuple[Spend, ...]:
        """Most-spending stage first, so the table reads as a ranking."""
        return tuple(sorted(self.spends.values(), key=lambda row: (-row.calls, row.stage)))

    def render(self) -> str:
        """The per-stage table, under it the deflection line, and what the run cost per case."""
        table = [("stage", "model", "calls", "in tokens", "out tokens", "est. cost")]
        table += [
            (
                row.stage,
                row.model or "(offline)",
                f"{row.calls:,}",
                f"{row.prompt_tokens:,}",
                f"{row.completion_tokens:,}",
                _money(row.cost),
            )
            for row in self.rows()
        ]
        table.append(
            (
                "total",
                f"{len(self.spends)} stage(s)",
                f"{self.calls:,}",
                f"{sum(row.prompt_tokens for row in self.spends.values()):,}",
                f"{sum(row.completion_tokens for row in self.spends.values()):,}",
                _money(self.cost),
            )
        )
        widths = [max(len(cell) for cell in column) for column in zip(*table, strict=True)]
        lines = [
            "  ".join(cell.ljust(width) for cell, width in zip(row, widths, strict=True)).rstrip()
            for row in table
        ]
        return "\n".join(
            [
                *lines,
                "",
                f"deflection rate: {self.deflected}/{self.arrivals} arrival(s) settled "
                f"before a provider was asked ({_percent(self.deflection_rate)})",
                self._cost_note(),
            ]
        )

    def _cost_note(self) -> str:
        """Say what the money figure covers, so an unpriced model cannot hide in a total.

        Calls are reported per arrival as well: a run whose calls outnumber its arrivals
        spent them on repairs, and that is worth seeing next to the bill.
        """
        per_case = self.cost / self.arrivals if self.arrivals else 0.0
        per_arrival = self.calls / self.arrivals if self.arrivals else 0.0
        note = (
            f"estimated cost: {_money(self.cost)} over {self.arrivals} arrival(s), "
            f"{_money(per_case)} each ({self.calls:,} provider call(s), {per_arrival:.2f} per arrival)"
        )
        if self.unpriced:
            named = ", ".join(sorted({row.model or row.provider for row in self.unpriced}))
            note += f"; unpriced and excluded: {named}"
        return note


# The process's meter. Providers write calls and tokens into it, the gateway writes
# arrivals and deflections, and a command prints it at the end of a run.
LEDGER = Ledger()


def _money(value: float | None) -> str:
    """A cost, or ``n/a`` for a model nobody publishes a rate for."""
    return "n/a" if value is None else f"${value:.4f}"


def _percent(rate: float) -> str:
    return f"{round(rate * 100)}%"


__all__ = [
    "LEDGER",
    "PRICES",
    "Ledger",
    "Spend",
]
