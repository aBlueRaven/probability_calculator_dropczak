"""Discover Streamlit scenario plugins from the source directory."""

from __future__ import annotations

import importlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScenarioPlugin:
    """A discovered scenario and its Streamlit rendering function."""

    name: str
    render: Callable[[], None]


def discover_scenarios(
    source_directory: Path | None = None,
) -> tuple[dict[str, ScenarioPlugin], dict[str, str]]:
    """Return valid scenario plugins and non-fatal loading errors."""
    source_directory = source_directory or Path(__file__).parent
    scenarios: dict[str, ScenarioPlugin] = {}
    errors: dict[str, str] = {}
    importlib.invalidate_caches()

    for scenario_directory in sorted(source_directory.iterdir()):
        ui_module = scenario_directory / "streamlit_ui.py"
        if not scenario_directory.is_dir() or not ui_module.is_file():
            continue

        scenario_name = scenario_directory.name
        try:
            module = importlib.import_module(f"src.{scenario_name}.streamlit_ui")
            render = getattr(module, "render")
            if not callable(render):
                raise TypeError("render must be callable")
        except Exception as error:
            errors[scenario_name] = str(error)
            continue

        scenarios[scenario_name] = ScenarioPlugin(scenario_name, render)

    return scenarios, errors
