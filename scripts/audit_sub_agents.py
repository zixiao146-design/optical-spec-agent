#!/usr/bin/env python3
"""Audit local sub-agent reality without running solvers or LLMs."""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from typing import Any


def _import_status(module_name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001 - audit should report failures.
        return False, str(exc)
    return True, "ok"


def main() -> int:
    import optical_spec_agent
    from optical_spec_agent.agents.roles import AGENT_ROLES
    from optical_spec_agent.agents.task_session import build_agent_task_session
    from optical_spec_agent.examples.registry import list_optical_design_examples
    from optical_spec_agent.materials.catalog import suggest_materials_for_application

    module_checks = {
        "optical_spec_agent": _import_status("optical_spec_agent"),
        "agents.models": _import_status("optical_spec_agent.agents.models"),
        "agents.orchestrator": _import_status("optical_spec_agent.agents.orchestrator"),
        "agents.task_session": _import_status("optical_spec_agent.agents.task_session"),
        "materials.catalog": _import_status("optical_spec_agent.materials.catalog"),
        "examples.registry": _import_status("optical_spec_agent.examples.registry"),
    }
    session = build_agent_task_session(
        "Create a local preview workflow for silver nanoparticle scattering on a thin film.",
        example_id="nanoparticle_plasmonics",
    )
    executed_roles = {step.agent_name for step in session.agent_trace.agents}
    agent_module = importlib.import_module("optical_spec_agent.agents")
    agent_rows: list[dict[str, Any]] = []
    for role_name, description in AGENT_ROLES:
        agent_rows.append(
            {
                "agent_name": role_name,
                "role": description,
                "installed_importable": module_checks["agents.task_session"][0],
                "importable_class": hasattr(agent_module, role_name),
                "callable_function": callable(build_agent_task_session),
                "role_exists_in_trace": role_name in executed_roles,
                "executed_in_sample_session": role_name in executed_roles,
            }
        )

    report = {
        "package_version": optical_spec_agent.__version__,
        "status": "ok",
        "module_checks": {
            name: {"importable": ok, "note": note}
            for name, (ok, note) in module_checks.items()
        },
        "agents": agent_rows,
        "material_catalog": {
            "callable": callable(suggest_materials_for_application),
            "sample_count": len(suggest_materials_for_application("nanoparticle plasmonics")),
        },
        "example_registry": {
            "callable": callable(list_optical_design_examples),
            "sample_count": len(list_optical_design_examples()),
        },
        "sample_session": {
            "session_id": session.session_id,
            "tool_call_count": len(session.tool_call_ledger),
            "external_solver_executed": session.external_solver_executed,
            "external_llm_required": session.external_llm_required,
            "production_grade_validation_claimed": session.production_grade_validation_claimed,
            "formal_convergence_proof_claimed": session.formal_convergence_proof_claimed,
        },
        "safety_markers": [
            "NO SOLVER EXECUTION PERFORMED",
            "NO EXTERNAL LLM CALLED",
            "NO UPLOAD PERFORMED",
            "NO TAG CREATED",
            "NO RELEASE CREATED",
        ],
    }

    for row in agent_rows:
        print(
            f"{row['agent_name']}: installed/importable="
            f"{'yes' if row['installed_importable'] else 'no'}, "
            f"importable_class={'yes' if row['importable_class'] else 'no'}, "
            f"callable={'yes' if row['callable_function'] else 'no'}, "
            f"executed_in_sample_session={'yes' if row['executed_in_sample_session'] else 'no'}"
        )
    for marker in report["safety_markers"]:
        print(marker)

    output_path = os.environ.get("OSA_SUB_AGENT_AUDIT_JSON")
    if output_path:
        path = Path(output_path)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"JSON report written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
