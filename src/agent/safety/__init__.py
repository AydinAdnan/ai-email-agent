"""Safety module: floor guardrails, action taxonomy, and injection tripwires."""
from src.agent.safety.floor import (
    FLOOR_RULES,
    FLOOR_VERSION,
    ActionClass,
    ActionPayload,
    EmailContext,
    FloorRule,
    SafetyVerdict,
    VetoLevel,
    classify_action,
    floor_check,
)
from src.agent.safety.injection import (
    InjectionScanResult,
    plan_deviation,
    scan,
)

__all__ = [
    "FLOOR_VERSION",
    "FLOOR_RULES",
    "ActionClass",
    "ActionPayload",
    "EmailContext",
    "FloorRule",
    "SafetyVerdict",
    "VetoLevel",
    "classify_action",
    "floor_check",
    "InjectionScanResult",
    "plan_deviation",
    "scan",
]
