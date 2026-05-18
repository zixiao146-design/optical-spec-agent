"""Local optical design example registry."""

from .registry import (
    build_example_agent_trace,
    get_optical_design_example,
    list_optical_design_examples,
)
from .requirements import (
    get_requirement_template,
    list_requirement_templates,
    match_goal_to_template,
)

__all__ = [
    "build_example_agent_trace",
    "get_optical_design_example",
    "get_requirement_template",
    "list_optical_design_examples",
    "list_requirement_templates",
    "match_goal_to_template",
]
