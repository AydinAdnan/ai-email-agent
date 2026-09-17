"""Streaming inbox simulator: arrival schedule, chat loop and reply-tree reconstruction."""
from agent.sim.policy import (
    Decision,
    GoldPolicy,
    email_context_for,
    floor_verdict_for,
)
from agent.sim.reply_tree import ReplyTree, build_reply_tree
from agent.sim.runner import INTERRUPTING_ROUTES, SimOutcome, run_simulation
from agent.sim.schedule import ScheduleError, Window, release_order, schedule
from agent.tools.email_tools import ACTION_TO_TOOL

__all__ = [
    "ACTION_TO_TOOL",
    "INTERRUPTING_ROUTES",
    "Decision",
    "GoldPolicy",
    "ReplyTree",
    "ScheduleError",
    "SimOutcome",
    "Window",
    "build_reply_tree",
    "email_context_for",
    "floor_verdict_for",
    "release_order",
    "run_simulation",
    "schedule",
]
