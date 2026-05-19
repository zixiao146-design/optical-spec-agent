"""Cross-check application domains against templates, materials, and tools."""

from __future__ import annotations

from pydantic import BaseModel, Field

from optical_spec_agent.examples.application_domains import (
    ApplicationDomain,
    get_application_domain,
    list_application_domains,
    linked_templates_exist,
)
from optical_spec_agent.materials.catalog import diagnose_material_suitability, get_material


class ApplicationDomainCrossCheck(BaseModel):
    domain_id: str
    status: str
    template_coverage: bool
    material_suitability_coverage: bool
    expected_calculators: list[str] = Field(default_factory=list)
    expected_adapters: list[str] = Field(default_factory=list)
    expected_tool_status: str
    missing_input_questions_present: bool
    suggested_materials: list[str] = Field(default_factory=list)
    unsuitable_materials: list[str] = Field(default_factory=list)
    material_suitability_summary: list[dict[str, str | bool | None]] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    deferred_capability: str | None = None
    preview_only: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainCrossChecksResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    cross_checks: list[ApplicationDomainCrossCheck] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def cross_check_application_domain(domain_id: str) -> ApplicationDomainCrossCheck:
    """Cross-check one application domain."""

    domain = get_application_domain(domain_id)
    diagnostics: list[str] = []
    template_coverage = _template_coverage(domain, diagnostics)
    material_coverage, suitability_summary = _material_coverage(domain, diagnostics)
    questions_present = bool(domain.recommended_questions and domain.common_missing_inputs)
    if not questions_present:
        diagnostics.append("Domain is missing recommended questions or common missing-input prompts.")

    expected_tool_status = "covered"
    deferred_capability = None
    if domain.domain_id in {"fiber_coupling_preview", "polarization_optics_preview"}:
        expected_tool_status = "partial_deferred"
        deferred_capability = (
            "Domain has preview material/template context, but dedicated calculator or "
            "solver-backed physical result remains deferred."
        )
        diagnostics.append(deferred_capability)
    elif not domain.expected_calculators and not domain.expected_adapters:
        expected_tool_status = "needs_review"
        diagnostics.append("Domain has no expected calculator or adapter path.")

    status = "pass"
    if not (template_coverage and material_coverage and questions_present):
        status = "fail"
    elif expected_tool_status != "covered":
        status = "warning"

    return ApplicationDomainCrossCheck(
        domain_id=domain.domain_id,
        status=status,
        template_coverage=template_coverage,
        material_suitability_coverage=material_coverage,
        expected_calculators=domain.expected_calculators,
        expected_adapters=domain.expected_adapters,
        expected_tool_status=expected_tool_status,
        missing_input_questions_present=questions_present,
        suggested_materials=domain.suggested_materials,
        unsuitable_materials=domain.unsuitable_materials,
        material_suitability_summary=suitability_summary,
        diagnostics=diagnostics or ["Application domain has local preview coverage."],
        deferred_capability=deferred_capability,
    )


def cross_check_all_application_domains() -> ApplicationDomainCrossChecksResponse:
    """Cross-check all registered application domains."""

    checks = [cross_check_application_domain(domain.domain_id) for domain in list_application_domains()]
    summary = {
        "total": len(checks),
        "pass": sum(1 for check in checks if check.status == "pass"),
        "warning": sum(1 for check in checks if check.status == "warning"),
        "fail": sum(1 for check in checks if check.status == "fail"),
        "preview_only": sum(1 for check in checks if check.preview_only),
    }
    return ApplicationDomainCrossChecksResponse(
        status="needs_review" if summary["fail"] else "ok",
        cross_checks=checks,
        summary=summary,
    )


def _template_coverage(domain: ApplicationDomain, diagnostics: list[str]) -> bool:
    try:
        return linked_templates_exist(domain)
    except ValueError as exc:
        diagnostics.append(str(exc))
        return False


def _material_coverage(
    domain: ApplicationDomain,
    diagnostics: list[str],
) -> tuple[bool, list[dict[str, str | bool | None]]]:
    summary: list[dict[str, str | bool | None]] = []
    ok = True
    for material_id in domain.suggested_materials:
        material = get_material(material_id)
        if material is None:
            diagnostics.append(f"Suggested material not found in local catalog: {material_id}")
            ok = False
            continue
        diagnostic = diagnose_material_suitability(material_id, domain.domain_id)
        if diagnostic.suitability == "unknown":
            diagnostics.append(
                f"No deterministic suitability rule for {material_id} in {domain.domain_id}."
            )
        summary.append(
            {
                "material_id": diagnostic.material_id,
                "suitability": diagnostic.suitability,
                "suitable": diagnostic.suitable,
                "requires_user_verification": diagnostic.requires_user_verification,
            }
        )
    return ok and bool(summary), summary

