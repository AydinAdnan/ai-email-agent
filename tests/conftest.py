"""Environment the suite runs under.

``main`` loads .env so a command can be run without exporting anything, which means a
developer's own WAJO_PROVIDER would otherwise decide what these tests run: a test that
replays the offline rules would go to the network instead, and would pass or fail by
whichever keys happen to be in the dotfile.

Pinned to the offline stand-in here. A test that wants the configured value says so
itself, and its own monkeypatch wins over this fixture.
"""
import pytest


@pytest.fixture(autouse=True)
def offline_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every test proposes from the offline rules unless it asks for something else."""
    monkeypatch.setenv("WAJO_PROVIDER", "rules")
