"""Simulated tools and the prepare/authorize/commit contract a real adapter will share."""
from agent.tools.email_tools import (
    ACTION_TO_TOOL,
    TOOL_CLASSES,
    SimulatedMailbox,
    build_registry,
)
from agent.tools.registry import (
    AUTONOMOUS_ROUTES,
    Approval,
    ApprovalRequired,
    Authorization,
    AuthorizationRefused,
    Effect,
    PreparedAction,
    Receipt,
    StaleApproval,
    Step,
    Tool,
    ToolError,
    ToolRegistry,
    UnknownTool,
)

__all__ = [
    "ACTION_TO_TOOL",
    "AUTONOMOUS_ROUTES",
    "TOOL_CLASSES",
    "Approval",
    "ApprovalRequired",
    "Authorization",
    "AuthorizationRefused",
    "Effect",
    "PreparedAction",
    "Receipt",
    "SimulatedMailbox",
    "StaleApproval",
    "Step",
    "Tool",
    "ToolError",
    "ToolRegistry",
    "UnknownTool",
    "build_registry",
]
