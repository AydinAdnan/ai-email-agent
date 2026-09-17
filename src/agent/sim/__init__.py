"""Streaming inbox simulator: arrival loop, chat CLI and reply-tree reconstruction."""
from agent.sim.policy import (
    ACTION_TO_TOOL,
    Decision,
    GoldPolicy,
    email_context_for,
    floor_verdict_for,
)
from agent.sim.reply_tree import ReplyTree, build_reply_tree
from agent.sim.runner import INTERRUPTING_ROUTES, SimOutcome, run_simulation

__all__ = [
    "ACTION_TO_TOOL",
    "INTERRUPTING_ROUTES",
    "Decision",
    "GoldPolicy",
    "ReplyTree",
    "SimOutcome",
    "build_reply_tree",
    "email_context_for",
    "floor_verdict_for",
    "run_simulation",
]
