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
from .application_domains import (
    get_application_domain,
    list_application_domains,
    match_goal_to_application_domains,
)
from .domain_cross_check import (
    cross_check_all_application_domains,
    cross_check_application_domain,
)
from .domain_benchmarks import (
    ApplicationDomainScenarioResponse,
    application_domain_benchmark_response,
    evaluate_all_domain_scenarios,
    evaluate_domain_scenario,
    get_domain_scenario,
    list_domain_scenarios,
)

__all__ = [
    "application_domain_benchmark_response",
    "ApplicationDomainScenarioResponse",
    "build_example_agent_trace",
    "cross_check_all_application_domains",
    "cross_check_application_domain",
    "evaluate_all_domain_scenarios",
    "evaluate_domain_scenario",
    "get_application_domain",
    "get_domain_scenario",
    "get_optical_design_example",
    "get_requirement_template",
    "list_application_domains",
    "list_domain_scenarios",
    "list_optical_design_examples",
    "list_requirement_templates",
    "match_goal_to_application_domains",
    "match_goal_to_template",
]
