"""Application-domain registry for local optical design previews.

The registry connects broad optical application domains to deterministic
requirement templates, preview material guidance, calculators, adapters,
missing-input prompts, and evidence boundaries. It is local-only and does not
query external material databases, call LLMs, or execute solvers.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.examples.requirements import get_requirement_template


DomainMatchConfidence = Literal["high", "medium", "low", "none"]


class ApplicationDomain(BaseModel):
    domain_id: str
    title: str
    title_zh: str
    aliases: list[str] = Field(default_factory=list)
    natural_language_keywords_en: list[str] = Field(default_factory=list)
    natural_language_keywords_zh: list[str] = Field(default_factory=list)
    linked_requirement_templates: list[str] = Field(default_factory=list)
    suggested_materials: list[str] = Field(default_factory=list)
    unsuitable_materials: list[str] = Field(default_factory=list)
    expected_calculators: list[str] = Field(default_factory=list)
    expected_adapters: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    optional_inputs: list[str] = Field(default_factory=list)
    common_missing_inputs: list[str] = Field(default_factory=list)
    default_assumptions: list[str] = Field(default_factory=list)
    recommended_questions: list[str] = Field(default_factory=list)
    evidence_boundary: str
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainMatchResult(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    matched_domains: list[str] = Field(default_factory=list)
    confidence: DomainMatchConfidence = "none"
    candidate_domains: list[str] = Field(default_factory=list)
    recommended_questions: list[str] = Field(default_factory=list)
    ambiguity_notes: list[str] = Field(default_factory=list)
    no_external_llm_used: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainsResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    domains: list[ApplicationDomain] = Field(default_factory=list)
    domain_count: int = 0
    catalog_status: str = "local_preview_application_domains"
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainDetailResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    domain: ApplicationDomain
    recommended_next_actions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


DOMAIN_ORDER = [
    "nanoparticle_plasmonics",
    "thin_film_coating",
    "slab_waveguide",
    "photonic_crystal",
    "dielectric_metasurface",
    "lens_ray_optics",
    "gaussian_beam_focusing",
    "imaging_system_preview",
    "fiber_coupling_preview",
    "polarization_optics_preview",
]


DOMAINS: dict[str, ApplicationDomain] = {
    "nanoparticle_plasmonics": ApplicationDomain(
        domain_id="nanoparticle_plasmonics",
        title="Nanoparticle plasmonics",
        title_zh="纳米颗粒等离激元",
        aliases=["nanoparticle scattering", "plasmonic particle", "gap plasmon"],
        natural_language_keywords_en=["nanoparticle", "plasmon", "scattering", "extinction", "particle"],
        natural_language_keywords_zh=["纳米颗粒", "纳米粒子", "等离激元", "散射", "消光"],
        linked_requirement_templates=["nanoparticle_plasmonics"],
        suggested_materials=["ag", "au", "sio2", "air", "water"],
        unsuitable_materials=["glass_bk7_preview", "glass_fused_silica_preview"],
        expected_calculators=[],
        expected_adapters=["meep", "gmsh"],
        required_inputs=["particle_material", "particle_radius", "background_or_gap_medium", "wavelength_band"],
        optional_inputs=["film_material", "film_thickness", "polarization", "incidence_direction"],
        common_missing_inputs=["particle_radius", "film_thickness", "gap_medium", "polarization"],
        default_assumptions=["Plane-wave-like broadband preview source.", "400-900 nm preview wavelength band."],
        recommended_questions=[
            "What particle material, size, and surrounding medium should be used?",
            "Should the observable be scattering, extinction, or near-field enhancement?",
        ],
        evidence_boundary="Material/adapter/source-monitor preview; real scattering spectra require explicit solver execution.",
    ),
    "thin_film_coating": ApplicationDomain(
        domain_id="thin_film_coating",
        title="Thin-film coating",
        title_zh="薄膜镀膜",
        aliases=["anti-reflection coating", "AR coating", "thin film stack"],
        natural_language_keywords_en=["thin film", "coating", "anti-reflection", "antireflection", "ar coating"],
        natural_language_keywords_zh=["薄膜", "镀膜", "增透", "减反", "薄膜堆栈"],
        linked_requirement_templates=["thin_film_ar_coating"],
        suggested_materials=["sio2", "tio2", "al2o3", "glass_bk7_preview"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.thin_film.spectrum", "optics.thin_film.quarter_wave_ar"],
        expected_adapters=["preview-only TMM calculator path"],
        required_inputs=["incident_medium", "substrate_material", "target_wavelength_nm", "layer_materials"],
        optional_inputs=["incidence_angle", "polarization", "wavelength_band"],
        common_missing_inputs=["substrate_material", "coating_material", "target_wavelength_nm", "incidence_angle"],
        default_assumptions=["Normal-incidence scalar transfer-matrix preview.", "Lossless layer constants unless k is provided."],
        recommended_questions=[
            "What substrate and target wavelength should the coating optimize?",
            "Is normal incidence acceptable for the preview?",
        ],
        evidence_boundary="Sanity-checked thin-film preview calculator; not production-grade coating validation.",
    ),
    "slab_waveguide": ApplicationDomain(
        domain_id="slab_waveguide",
        title="Slab waveguide",
        title_zh="平板波导",
        aliases=["single-mode waveguide", "integrated photonics waveguide"],
        natural_language_keywords_en=["waveguide", "single mode", "mode confinement", "integrated photonics"],
        natural_language_keywords_zh=["波导", "单模", "模式", "集成光子"],
        linked_requirement_templates=["slab_waveguide_single_mode"],
        suggested_materials=["si", "si3n4", "sio2", "air"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.waveguide.sweep", "optics.waveguide.single_mode_range"],
        expected_adapters=["mpb", "elmer"],
        required_inputs=["core_material", "cladding_material", "core_thickness_um", "wavelength_nm"],
        optional_inputs=["polarization", "mode_index", "sidewall_angle"],
        common_missing_inputs=["core_thickness_um", "cladding_material", "wavelength_nm", "polarization"],
        default_assumptions=["Scalar slab V-number preview.", "Single-mode threshold is approximate."],
        recommended_questions=[
            "What core/cladding materials and operating wavelength should be used?",
            "Is this TE-like, TM-like, or polarization-agnostic?",
        ],
        evidence_boundary="Waveguide V-number preview; full mode solving requires explicit solver execution.",
    ),
    "photonic_crystal": ApplicationDomain(
        domain_id="photonic_crystal",
        title="Photonic crystal",
        title_zh="光子晶体",
        aliases=["PhC band", "band structure preview"],
        natural_language_keywords_en=["photonic crystal", "band structure", "band diagram", "lattice", "mpb"],
        natural_language_keywords_zh=["光子晶体", "能带", "带隙", "晶格"],
        linked_requirement_templates=["photonic_crystal_band_preview"],
        suggested_materials=["si", "gaas", "sio2", "air"],
        unsuitable_materials=["water"],
        expected_calculators=[],
        expected_adapters=["mpb"],
        required_inputs=["lattice_constant", "unit_cell_geometry", "material_contrast", "k_point_path"],
        optional_inputs=["num_bands", "resolution", "polarization"],
        common_missing_inputs=["lattice_constant", "unit_cell_geometry", "k_point_path"],
        default_assumptions=["MPB-style band structure preview metadata.", "No real band data without MPB execution."],
        recommended_questions=[
            "What lattice type, lattice constant, and k-point path should be used?",
            "How many bands should the preview plan request?",
        ],
        evidence_boundary="Adapter-native MPB preview metadata; real band frequencies require explicit MPB execution.",
    ),
    "dielectric_metasurface": ApplicationDomain(
        domain_id="dielectric_metasurface",
        title="Dielectric metasurface",
        title_zh="介质超表面",
        aliases=["metalens", "phase profile preview", "meta atom"],
        natural_language_keywords_en=["metasurface", "metalens", "meta atom", "phase profile"],
        natural_language_keywords_zh=["超表面", "超透镜", "相位", "单元结构"],
        linked_requirement_templates=["dielectric_metasurface_preview"],
        suggested_materials=["tio2", "si3n4", "si", "sio2"],
        unsuitable_materials=["ag", "au", "water"],
        expected_calculators=[],
        expected_adapters=["meep", "gmsh"],
        required_inputs=["target_phase_profile", "period", "wavelength_nm", "material_stack"],
        optional_inputs=["polarization", "numerical_aperture", "unit_cell_height"],
        common_missing_inputs=["target_phase_profile", "period", "polarization", "unit_cell_geometry"],
        default_assumptions=["Plane-wave preview source.", "Phase-profile/far-field observable metadata only."],
        recommended_questions=[
            "What phase profile or focusing target should the metasurface implement?",
            "What period, height, and polarization should define the unit-cell preview?",
        ],
        evidence_boundary="Material/geometry/adapter preview; no full-wave metasurface result is computed by default.",
    ),
    "lens_ray_optics": ApplicationDomain(
        domain_id="lens_ray_optics",
        title="Lens ray optics",
        title_zh="透镜光线光学",
        aliases=["paraxial lens", "ray trace preview", "singlet lens"],
        natural_language_keywords_en=["lens", "ray trace", "focal length", "singlet", "relay"],
        natural_language_keywords_zh=["透镜", "光线", "焦距", "单透镜", "中继"],
        linked_requirement_templates=["paraxial_lens_imaging"],
        suggested_materials=["glass_bk7_preview", "glass_fused_silica_preview", "air"],
        unsuitable_materials=["ag", "au", "si"],
        expected_calculators=["optics.paraxial.two_lens_relay", "optics.paraxial.thin_lens"],
        expected_adapters=["optiland"],
        required_inputs=["focal_length_mm", "object_distance_mm", "aperture"],
        optional_inputs=["field_of_view", "wavelength_nm", "glass_choice"],
        common_missing_inputs=["focal_length_mm", "aperture", "field_of_view"],
        default_assumptions=["Paraxial thin-lens preview.", "No aberrations or production ray-trace validation."],
        recommended_questions=[
            "What focal length, aperture, and field of view should be previewed?",
            "Is paraxial approximation acceptable for this first pass?",
        ],
        evidence_boundary="Paraxial calculator and Optiland preview metadata; real ray trace requires explicit execution.",
    ),
    "gaussian_beam_focusing": ApplicationDomain(
        domain_id="gaussian_beam_focusing",
        title="Gaussian beam focusing",
        title_zh="高斯光束聚焦",
        aliases=["beam waist", "Rayleigh range", "focused Gaussian beam"],
        natural_language_keywords_en=["gaussian", "beam waist", "rayleigh", "focused beam", "waist"],
        natural_language_keywords_zh=["高斯光束", "光腰", "瑞利", "聚焦光束"],
        linked_requirement_templates=["gaussian_beam_focus"],
        suggested_materials=["air", "glass_fused_silica_preview"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.gaussian_beam.series", "optics.gaussian_beam.focus"],
        expected_adapters=["optiland"],
        required_inputs=["wavelength_nm", "input_waist_um", "propagation_distance_or_focal_length"],
        optional_inputs=["medium_index", "beam_quality_factor", "aperture"],
        common_missing_inputs=["wavelength_nm", "waist_um", "propagation_distance_or_focal_length"],
        default_assumptions=["Paraxial Gaussian beam approximation.", "M2=1 unless specified."],
        recommended_questions=[
            "What wavelength, input waist, and propagation/focal distance should be used?",
            "Should the preview include a thin lens focus estimate?",
        ],
        evidence_boundary="Gaussian beam calculator preview; not a measured or solver-derived focal field.",
    ),
    "imaging_system_preview": ApplicationDomain(
        domain_id="imaging_system_preview",
        title="Imaging system preview",
        title_zh="成像系统预览",
        aliases=["image plane preview", "relay imaging", "optical imaging"],
        natural_language_keywords_en=["imaging system", "image plane", "magnification", "field of view"],
        natural_language_keywords_zh=["成像系统", "像面", "放大率", "视场"],
        linked_requirement_templates=["paraxial_lens_imaging"],
        suggested_materials=["glass_bk7_preview", "glass_fused_silica_preview", "air"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.paraxial.two_lens_relay"],
        expected_adapters=["optiland"],
        required_inputs=["object_distance_mm", "image_distance_or_magnification", "aperture"],
        optional_inputs=["field_of_view", "wavelength_nm", "lens_spacing"],
        common_missing_inputs=["magnification", "field_of_view", "aperture"],
        default_assumptions=["Paraxial relay preview.", "Image quality metrics are metadata unless Optiland is explicitly run."],
        recommended_questions=[
            "What magnification and image plane should the preview target?",
            "What aperture and field should constrain the imaging system?",
        ],
        evidence_boundary="Paraxial imaging preview; real spot/MTF requires explicit ray-trace execution.",
    ),
    "fiber_coupling_preview": ApplicationDomain(
        domain_id="fiber_coupling_preview",
        title="Fiber coupling preview",
        title_zh="光纤耦合预览",
        aliases=["fiber coupling", "mode overlap", "coupling efficiency"],
        natural_language_keywords_en=["fiber coupling", "mode overlap", "coupling efficiency", "fiber mode"],
        natural_language_keywords_zh=["光纤耦合", "模式重叠", "耦合效率", "光纤模式"],
        linked_requirement_templates=["gaussian_beam_focus", "slab_waveguide_single_mode"],
        suggested_materials=["glass_fused_silica_preview", "sio2", "si3n4", "air"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.fiber_coupling.gaussian_mode_overlap"],
        expected_adapters=["mpb", "optiland"],
        required_inputs=["mode_field_diameter", "wavelength_nm", "alignment_tolerance", "target_mode"],
        optional_inputs=["fiber_na", "waveguide_mode_index", "lens_focal_length"],
        common_missing_inputs=["mode_field_diameter", "target_mode", "alignment_tolerance"],
        default_assumptions=[
            "Scalar Gaussian fiber-mode overlap preview.",
            "No coupled-mode solver is run by default.",
        ],
        recommended_questions=[
            "What fiber mode field diameter and wavelength should be assumed?",
            "Is the target coupling into a fiber, waveguide, or free-space focus?",
        ],
        evidence_boundary="Scalar Gaussian mode-overlap preview; real coupling efficiency still requires explicit solver or measurement validation.",
    ),
    "polarization_optics_preview": ApplicationDomain(
        domain_id="polarization_optics_preview",
        title="Polarization optics preview",
        title_zh="偏振光学预览",
        aliases=["polarizer", "waveplate", "Jones preview"],
        natural_language_keywords_en=["polarization", "polarizer", "waveplate", "retarder", "jones"],
        natural_language_keywords_zh=["偏振", "偏振片", "波片", "延迟器", "琼斯"],
        linked_requirement_templates=["dielectric_metasurface_preview"],
        suggested_materials=["tio2", "si3n4", "sio2", "glass_fused_silica_preview"],
        unsuitable_materials=["ag", "au"],
        expected_calculators=["optics.polarization.jones"],
        expected_adapters=["meep"],
        required_inputs=["input_polarization", "target_polarization_transform", "wavelength_nm"],
        optional_inputs=["retardance", "axis_angle", "bandwidth"],
        common_missing_inputs=["input_polarization", "target_polarization_transform", "retardance"],
        default_assumptions=[
            "Ideal Jones-calculus polarizer/waveplate preview.",
            "No Jones/Mueller production model is claimed.",
        ],
        recommended_questions=[
            "What input and output polarization states should be transformed?",
            "Is the target a polarizer, waveplate, or metasurface polarization element?",
        ],
        evidence_boundary="Jones-calculus preview only; real vector EM or measured Mueller/Jones validation is deferred.",
    ),
}


def list_application_domains() -> list[ApplicationDomain]:
    """Return stable application domains."""

    return [DOMAINS[domain_id] for domain_id in DOMAIN_ORDER]


def get_application_domain(domain_id: str) -> ApplicationDomain:
    """Return one application domain."""

    try:
        return DOMAINS[domain_id]
    except KeyError as exc:
        raise ValueError(f"Unknown application domain: {domain_id}") from exc


def match_goal_to_application_domains(goal: str) -> ApplicationDomainMatchResult:
    """Match a natural-language goal to one or more application domains."""

    text = goal.strip()
    if not text:
        return ApplicationDomainMatchResult(
            status="needs_review",
            confidence="none",
            ambiguity_notes=["No goal text was supplied."],
            recommended_questions=[
                "Which optical application domain should be previewed?",
                "What material system and target observable should be used?",
            ],
        )

    lowered = text.lower()
    scores: list[tuple[int, int, str]] = []
    for priority, domain_id in enumerate(DOMAIN_ORDER):
        domain = DOMAINS[domain_id]
        keywords = [
            *domain.aliases,
            *domain.natural_language_keywords_en,
            *domain.natural_language_keywords_zh,
        ]
        score = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if score:
            scores.append((score, -priority, domain_id))

    if not scores:
        generic_tokens = ("optical system", "optical design", "光学系统", "光学设计")
        if any(token in lowered for token in generic_tokens):
            candidates = [
                "thin_film_coating",
                "slab_waveguide",
                "lens_ray_optics",
                "gaussian_beam_focusing",
                "nanoparticle_plasmonics",
            ]
            return ApplicationDomainMatchResult(
                status="needs_review",
                confidence="low",
                candidate_domains=candidates,
                ambiguity_notes=["Generic optical-system wording does not identify a single domain."],
                recommended_questions=[
                    "Is the goal about coatings, beams, waveguides, lenses, metasurfaces, photonic crystals, or nanoparticles?",
                    "Which material system and observable should be previewed?",
                ],
            )
        return ApplicationDomainMatchResult(
            status="needs_review",
            confidence="none",
            ambiguity_notes=["No deterministic application-domain keywords matched."],
            recommended_questions=[
                "Name the optical application domain before choosing materials or tools.",
                "Specify whether the first artifact should be a calculator result or adapter preview.",
            ],
        )

    sorted_scores = sorted(scores, reverse=True)
    top_score = sorted_scores[0][0]
    candidates = [domain_id for score, _, domain_id in sorted_scores if score == top_score]
    all_candidates = [domain_id for _, _, domain_id in sorted_scores]
    if len(candidates) > 1 or _looks_mixed_domain_goal(all_candidates):
        confidence: DomainMatchConfidence = "low"
        matched: list[str] = []
        status = "needs_review"
        ambiguity_notes = ["Multiple application domains matched; the backend will ask for clarification."]
    elif top_score >= 2:
        confidence = "high"
        matched = [candidates[0]]
        status = "ok"
        ambiguity_notes = []
    else:
        confidence = "medium"
        matched = [candidates[0]]
        status = "needs_review"
        ambiguity_notes = ["Only one domain keyword matched; missing inputs should be reviewed."]

    questions = _domain_questions(candidates or all_candidates)
    return ApplicationDomainMatchResult(
        status=status,
        matched_domains=matched,
        confidence=confidence,
        candidate_domains=all_candidates,
        ambiguity_notes=ambiguity_notes,
        recommended_questions=questions,
    )


def _looks_mixed_domain_goal(candidate_domains: list[str]) -> bool:
    high_level = set(candidate_domains[:3])
    return len(high_level & {"thin_film_coating", "slab_waveguide", "lens_ray_optics", "gaussian_beam_focusing"}) > 1


def _domain_questions(domain_ids: list[str]) -> list[str]:
    questions: list[str] = []
    seen: set[str] = set()
    for domain_id in domain_ids:
        domain = DOMAINS[domain_id]
        for question in domain.recommended_questions[:2]:
            if question not in seen:
                questions.append(question)
                seen.add(question)
    return questions[:6]


def linked_templates_exist(domain: ApplicationDomain) -> bool:
    """Return true when all linked requirement templates can be loaded."""

    for template_id in domain.linked_requirement_templates:
        get_requirement_template(template_id)
    return True
