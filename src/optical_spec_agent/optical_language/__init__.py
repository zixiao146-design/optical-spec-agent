"""Local optical-language helpers for source, monitor, and diagnostics."""

from .adapter_mapping import AdapterSourceMonitorMapping, map_source_monitor_to_adapter
from .golden_coverage import (
    AdapterGoldenCoverageItem,
    AdapterGoldenCoverageReport,
    build_adapter_golden_coverage_report,
)
from .observables import (
    ObservableDiagnostic,
    diagnose_observable,
    suggest_observables_for_template,
)
from .source_monitor import (
    OpticalLanguageDiagnostics,
    OpticalMonitorModel,
    OpticalSourceModel,
    SourceMonitorInference,
    diagnose_missing_inputs,
    infer_source_monitor_from_goal,
    template_source_monitor_defaults,
)

__all__ = [
    "AdapterSourceMonitorMapping",
    "AdapterGoldenCoverageItem",
    "AdapterGoldenCoverageReport",
    "ObservableDiagnostic",
    "OpticalLanguageDiagnostics",
    "OpticalMonitorModel",
    "OpticalSourceModel",
    "SourceMonitorInference",
    "diagnose_missing_inputs",
    "diagnose_observable",
    "infer_source_monitor_from_goal",
    "build_adapter_golden_coverage_report",
    "map_source_monitor_to_adapter",
    "suggest_observables_for_template",
    "template_source_monitor_defaults",
]
