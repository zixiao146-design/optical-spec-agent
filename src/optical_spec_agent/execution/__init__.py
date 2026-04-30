"""Execution helpers for optional solver runs."""

from .csv_sanity import CsvSanityResult, check_csv_numeric_sanity
from .meep_runner import (
    ExecutionResult,
    PostprocessResult,
    check_meep_available,
    collect_meep_outputs,
    find_meep_python,
    parse_postprocess_results,
    parse_typed_postprocess_results,
    run_meep_script,
)

__all__ = [
    "CsvSanityResult",
    "ExecutionResult",
    "PostprocessResult",
    "check_csv_numeric_sanity",
    "check_meep_available",
    "collect_meep_outputs",
    "find_meep_python",
    "parse_postprocess_results",
    "parse_typed_postprocess_results",
    "run_meep_script",
]
