import type {
  AgentTraceResponse,
  AgentTaskSessionResponse,
  AdapterPreviewResponse,
  AdaptersResponse,
  ExampleDetailResponse,
  ExamplesResponse,
  HealthResponse,
  MaterialSuggestionResponse,
  MaterialsResponse,
  ParseResponse,
  ReadinessResponse,
  SchemaResponse,
  ValidateResponse,
  ValidationEvidenceResponse,
  VersionResponse,
  WorkflowPlanResponse,
} from "../api/types";

export const DEMO_FIXTURE_LOADED_MESSAGE =
  "Demo fixture loaded - not live validation until submitted.";

export const demoNaturalLanguageSpec =
  "Use Meep FDTD to simulate an 80 nm gold nanoparticle on a 100 nm gold film with a 5 nm SiO2 gap, normal-incidence plane wave from 400-900 nm, and report the scattering spectrum.";

export const demoChineseNaturalLanguageSpec =
  "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。优先使用开源仿真工具链，默认不运行外部求解器，不调用外部 LLM，只生成可检查的规格、工作流计划和适配器预览。";

export const demoValidateRequestText = JSON.stringify(
  { path: "examples/specs/minimal_nanoparticle.json" },
  null,
  2,
);

export const demoWorkflowRequestText = JSON.stringify(
  { path: "examples/workflows/local_preview_request.json" },
  null,
  2,
);

export const demoAdapterPreviewRequestText = JSON.stringify(
  { path: "examples/specs/minimal_nanoparticle.json", tool: "gmsh" },
  null,
  2,
);

const base = {
  external_solver_executed: false,
  external_llm_required: false,
  proprietary_solver_required: false,
  production_grade_validation_claimed: false,
  formal_convergence_proof_claimed: false,
  api_contract_version: "0.1",
  status: "ok",
  diagnostics: {
    errors: [],
    warnings: ["Demo fixture mode: this is not live validation."],
    missing_fields: [],
    assumptions: [],
    limitations: ["Demo fixtures are for local frontend development only."],
    details: {},
  },
  recommended_next_actions: [
    "Start the local Agent API for live validation.",
    "Use demo fixtures only for UI walkthroughs.",
  ],
};

export const demoHealth: HealthResponse = {
  ...base,
  service: "optical-spec-agent",
};

export const demoVersion: VersionResponse = {
  ...base,
  package_version: "0.9.0rc8.dev0",
  current_public_prerelease: "v0.9.0rc7",
  main_development_version: "0.9.0rc8.dev0",
  pypi_published: false,
  testpypi_verified: true,
  testpypi_verified_version: "0.9.0rc6.dev0",
};

export const demoAdapters: AdaptersResponse = {
  ...base,
  adapters: [
    {
      tool_name: "gmsh",
      display_name: "Gmsh geometry / meshing",
      solver_family: "geometry / mesh",
      current_status: "mvp",
      maturity_level: "Level 3",
      evidence: "validation/gmsh/gmsh_validation_pilot_2026-05-14.md",
      external_solver_required_by_default: false,
      production_grade_validation_claimed: false,
      formal_convergence_proof_claimed: false,
      limitations: ["Preview scaffold only; does not run gmsh."],
    },
    {
      tool_name: "meep",
      display_name: "Meep FDTD",
      solver_family: "FDTD",
      current_status: "preview",
      maturity_level: "Level 3",
      evidence: "validation/meep/meep_validation_pilot_2026-05-14.md",
      external_solver_required_by_default: false,
      production_grade_validation_claimed: false,
      formal_convergence_proof_claimed: false,
      limitations: ["Generates scripts only; Meep execution is explicit."],
    },
    {
      tool_name: "mpb",
      display_name: "MIT Photonic Bands (MPB)",
      solver_family: "eigenmode / band structure",
      current_status: "mvp",
      maturity_level: "Level 3",
      evidence: "validation/mpb/mpb_validation_pilot_2026-05-14.md",
      external_solver_required_by_default: false,
      production_grade_validation_claimed: false,
      formal_convergence_proof_claimed: false,
      limitations: ["Preview scaffold only; does not run MPB."],
    },
    {
      tool_name: "elmer",
      display_name: "Elmer FEM",
      solver_family: "FEM",
      current_status: "mvp",
      maturity_level: "Level 2 + Level-3-ready",
      evidence: "validation/elmer/elmer_install_deferred_2026-05-15.md",
      external_solver_required_by_default: false,
      production_grade_validation_claimed: false,
      formal_convergence_proof_claimed: false,
      limitations: ["Elmer Level 3 validation is deferred."],
    },
    {
      tool_name: "optiland",
      display_name: "Optiland",
      solver_family: "sequential ray tracing",
      current_status: "mvp",
      maturity_level: "Level 3",
      evidence: "validation/optiland/optiland_validation_pilot_2026-05-14.md",
      external_solver_required_by_default: false,
      production_grade_validation_claimed: false,
      formal_convergence_proof_claimed: false,
      limitations: ["Scaffold only; does not run Optiland."],
    },
  ],
};

export const demoEvidence: ValidationEvidenceResponse = {
  ...base,
  validation_evidence: demoAdapters.adapters.map((adapter) => ({
    tool_name: adapter.tool_name,
    display_name: adapter.display_name,
    maturity_level: adapter.maturity_level,
    evidence: adapter.evidence,
    status_note:
      adapter.tool_name === "elmer"
        ? "Level 3 validation deferred pending maintainable ElmerSolver availability."
        : "Optional manual validation evidence recorded.",
    production_grade_validation_claimed: false,
    formal_convergence_proof_claimed: false,
  })),
};

export const demoReadiness: ReadinessResponse = {
  ...base,
  current_public_prerelease: "v0.9.0rc7",
  main_development_version: "0.9.0rc8.dev0",
  testpypi: {
    uploaded_and_verified: true,
    verified_version: "0.9.0rc6.dev0",
    upload_for_current_dev_version: "not performed",
  },
  pypi: {
    published: false,
    publication_approval: "not granted",
  },
  public_contract_freeze: {
    status: "approved",
    date: "2026-05-16",
  },
  adapter_maturity: {
    gmsh: "Level 3",
    meep: "Level 3",
    mpb: "Level 3",
    optiland: "Level 3",
    elmer: "Level 2 + Level-3-ready",
  },
  v1_0_0_released: false,
};

export const demoSchema: SchemaResponse = {
  ...base,
  schema_name: "OpticalSpec",
  schema: {
    title: "OpticalSpec",
    type: "object",
    properties: {
      task: { type: "object" },
      physics: { type: "object" },
      simulation: { type: "object" },
      output: { type: "object" },
    },
  },
};

export const demoParseResponse: ParseResponse = {
  ...base,
  parser: "heuristic",
  spec: {
    task: { task_type: "simulation" },
    simulation: { solver_method: "fdtd", software_tool: "meep" },
  },
  summary: "Demo parse fixture. Start the local API for live parsing.",
};

export const demoValidateResponse: ValidateResponse = {
  ...base,
  valid: true,
};

export const demoWorkflowPlan: WorkflowPlanResponse = {
  ...base,
  workflow_plan: {
    schema_version: "workflow_plan.v0.9",
    selected_tool: "mpb",
    execute_policy: "no_execute_by_default",
    planned_steps: ["intake", "parse", "validate", "adapter_selection", "generation", "human_review"],
    limitations: ["Demo workflow plan only; no solver was executed."],
  },
  public_top_level_keys: [
    "schema_version",
    "selected_tool",
    "execute_policy",
    "planned_steps",
    "limitations",
  ],
};

export const demoAdapterPreview: AdapterPreviewResponse = {
  ...base,
  tool: "gmsh",
  display_name: "Gmsh geometry / meshing",
  output_language: "geo",
  output_extension: ".geo",
  preview_content:
    "// Demo preview fixture only. No solver was executed. Start the local API for live adapter preview.",
  artifact_summary: {
    content_length: 98,
    generated_files: {},
    missing_required: [],
    defaults_applied: [],
  },
};

export const demoMaterials: MaterialsResponse = {
  ...base,
  catalog_status: "local_preview_catalog",
  catalog_note:
    "Material data is a local preview/design-assist catalog and not a production-grade optical constants database.",
  materials: [
    {
      material_id: "sio2",
      display_name: "Silicon dioxide (SiO2)",
      aliases: ["silica", "oxide", "fused_silica"],
      category: "dielectric",
      common_use: ["thin film coating", "waveguide cladding", "spacer"],
      optical_role: "low-index dielectric",
      production_grade: false,
      validation_level: "preview",
      source_note: "Curated local preview value for examples only.",
    },
    {
      material_id: "si",
      display_name: "Silicon (Si)",
      aliases: ["silicon"],
      category: "semiconductor",
      common_use: ["waveguide", "photonic crystal", "metasurface"],
      optical_role: "high-index semiconductor",
      production_grade: false,
      validation_level: "preview",
      source_note: "Curated local preview value for examples only.",
    },
    {
      material_id: "au",
      display_name: "Gold (Au)",
      aliases: ["gold"],
      category: "metal",
      common_use: ["nanoparticle plasmonics", "film", "antenna"],
      optical_role: "plasmonic metal",
      production_grade: false,
      validation_level: "preview",
      source_note: "Curated local preview value for examples only.",
    },
    {
      material_id: "ag",
      display_name: "Silver (Ag)",
      aliases: ["silver"],
      category: "metal",
      common_use: ["nanoparticle plasmonics", "film", "antenna"],
      optical_role: "plasmonic metal",
      production_grade: false,
      validation_level: "preview",
      source_note: "Curated local preview value for examples only.",
    },
  ],
};

export const demoMaterialSuggestion: MaterialSuggestionResponse = {
  ...base,
  application: "nanoparticle plasmonics",
  catalog_status: "local_preview_catalog",
  catalog_note:
    "Suggestions are local preview guidance only; verify material data independently.",
  suggested_materials: demoMaterials.materials.filter((item) =>
    ["au", "ag", "sio2"].includes(item.material_id),
  ),
};

export const demoAgentTrace: AgentTraceResponse = {
  ...base,
  trace_id: "trace-demo-nanoparticle",
  example_id: "nanoparticle_plasmonics",
  design_goal: "Preview a local workflow for plasmonic nanoparticle scattering.",
  timeline_summary:
    "Example Gallery -> Material suggestions -> Adapter recommendation -> Agent trace timeline -> Workflow plan -> Artifact preview -> Evidence -> Next action",
  material_suggestions: ["au", "ag", "sio2"],
  adapter_recommendation: "meep with gmsh geometry preview",
  agents: [
    {
      step_index: 1,
      agent_name: "SpecAgent",
      role: "Interprets user intent / spec and identifies missing fields.",
      stage: "spec_intake",
      input_summary: "Nanoparticle plasmonics request.",
      output_summary: "Prepared a local preview intent summary.",
      diagnostics: ["Spec interpretation is deterministic and local."],
      recommended_next_actions: ["Review wavelength, geometry, material, and output fields."],
      confidence: "candidate",
      status: "ok",
      safety_notes: ["No external LLM was called for this preview trace."],
      evidence_refs: [],
    },
    {
      step_index: 2,
      agent_name: "MaterialAgent",
      role: "Suggests materials from the local preview material catalog.",
      stage: "material_selection",
      input_summary: "Application: nanoparticle plasmonics.",
      output_summary: "Suggested Au, Ag, and SiO2 as preview materials.",
      diagnostics: ["Material constants are preview/design-assist values only."],
      recommended_next_actions: ["Verify optical constants before physical conclusions."],
      confidence: "preview",
      status: "ok",
      safety_notes: ["Material data is not production-grade optical constants."],
      evidence_refs: ["docs/material_library.md"],
    },
    {
      step_index: 4,
      agent_name: "AdapterAgent",
      role: "Recommends adapter/tool and explains maturity / limitations.",
      stage: "adapter_recommendation",
      input_summary: "Nanoparticle plasmonics with local material hints.",
      output_summary: "Recommended Meep with Gmsh geometry preview.",
      diagnostics: ["Open-source-solver-first recommendation; no proprietary dependency."],
      recommended_next_actions: ["Use adapter preview before optional solver execution."],
      confidence: "candidate",
      status: "ok",
      safety_notes: ["No proprietary solver is required by default."],
      evidence_refs: ["docs/adapter_support_matrix.md"],
    },
    {
      step_index: 7,
      agent_name: "SafetyAgent",
      role: "Checks no overclaim and no default solver/LLM/publish/release actions.",
      stage: "safety_review",
      input_summary: "Collaboration trace safety review.",
      output_summary: "Safety flags remain false.",
      diagnostics: ["No production-grade validation or formal convergence proof is claimed."],
      recommended_next_actions: ["Keep preview boundaries visible in the UI."],
      confidence: "validated",
      status: "ok",
      safety_notes: ["No solver, LLM, upload, tag, or release action."],
      evidence_refs: ["docs/frontend_safety_policy.md"],
    },
  ],
  final_recommendation:
    "Use local preview materials, generate a workflow plan, and inspect adapter previews without executing a solver.",
};

export const demoAgentSession: AgentTaskSessionResponse = {
  ...base,
  session_id: "session-demo-nanoparticle",
  user_goal: demoChineseNaturalLanguageSpec,
  optical_intent_summary: "nanoparticle plasmonics / scattering preview",
  selected_example_id: "nanoparticle_plasmonics",
  design_case_summary: "nanoparticle_plasmonics example-backed nanoparticle plasmonics / scattering preview",
  plan_steps: [
    {
      step_index: 1,
      title: "Interpret optical goal",
      title_zh: "理解光学目标",
      description: "Translate the natural language goal into nanoparticle scattering intent.",
      description_zh: "将自然语言目标转换为纳米颗粒散射意图。",
      agent_name: "SpecAgent",
      status: "completed",
      endpoint_or_tool: "local heuristic intent detector",
      expected_output: "optical_intent_summary",
      safety_note: "No external LLM is called by default.",
    },
    {
      step_index: 2,
      title: "Suggest materials",
      title_zh: "推荐材料",
      description: "Use the local preview material catalog.",
      description_zh: "使用本地预览材料库。",
      agent_name: "MaterialAgent",
      status: "completed",
      endpoint_or_tool: "/api/materials/suggest",
      expected_output: "material_suggestions",
      safety_note: "Material data is preview/design-assist, not production-grade optical constants.",
    },
    {
      step_index: 3,
      title: "Plan local workflow",
      title_zh: "规划本地工作流",
      description: "Plan parse, validate, adapter preview, evidence, and human review.",
      description_zh: "规划解析、验证、适配器预览、证据和人工审阅。",
      agent_name: "WorkflowAgent",
      status: "completed",
      endpoint_or_tool: "/api/workflow-plan",
      expected_output: "workflow_plan artifact",
      safety_note: "No solver is executed by default.",
    },
  ],
  agent_trace: demoAgentTrace,
  artifacts: [
    {
      artifact_id: "spec-preview",
      label: "Spec preview",
      label_zh: "规格预览",
      artifact_type: "spec",
      summary: "Design intent mapped to a local nanoparticle plasmonics preview.",
      preview_content: "examples/optical_design/nanoparticle_plasmonics/spec.json",
      source_endpoint: "/api/agent-session",
      generated_by_agent: "SpecAgent",
      production_grade: false,
    },
    {
      artifact_id: "material-suggestions",
      label: "Material suggestions",
      label_zh: "材料建议",
      artifact_type: "material_suggestions",
      summary: "au, ag, sio2",
      source_endpoint: "/api/materials/suggest",
      generated_by_agent: "MaterialAgent",
      production_grade: false,
    },
    {
      artifact_id: "agent-trace",
      label: "Sub-agent trace",
      label_zh: "子智能体轨迹",
      artifact_type: "agent_trace",
      summary: "Deterministic local collaboration trace.",
      source_endpoint: "/api/agent-session",
      generated_by_agent: "RecommendationAgent",
      production_grade: false,
    },
  ],
  permission_gates: [
    {
      gate_id: "parse_local_spec",
      label: "Parse local spec",
      label_zh: "本地解析规格",
      status: "allowed",
      reason: "Local deterministic parsing is part of the preview workflow.",
      risk_level: "low",
      default_allowed: true,
    },
    {
      gate_id: "run_external_solver",
      label: "External solver execution",
      label_zh: "外部求解器执行",
      status: "requires_explicit_approval",
      reason: "External solvers are never executed by default.",
      risk_level: "high",
      default_allowed: false,
    },
    {
      gate_id: "create_github_release",
      label: "GitHub release creation",
      label_zh: "GitHub release 创建",
      status: "blocked",
      reason: "Release operations are not controlled from Agent Studio.",
      risk_level: "high",
      default_allowed: false,
    },
  ],
  final_recommendation:
    "Inspect material candidates, review permission gates, then generate local workflow and adapter-preview artifacts only.",
};

export const demoExamples: ExamplesResponse = {
  ...base,
  gallery_status: "local_preview_examples",
  gallery_note:
    "Examples are local preview workflows with solver execution disabled by default and no production-grade validation claim.",
  examples: [
    {
      example_id: "nanoparticle_plasmonics",
      title: "Nanoparticle Plasmonics Preview",
      title_zh: "纳米颗粒等离激元预览",
      design_goal: "Preview a local workflow for plasmonic nanoparticle scattering.",
      design_goal_zh: "预览一个本地纳米颗粒散射工作流。",
      category: "plasmonics",
      suggested_materials: ["au", "ag", "sio2", "water", "air"],
      suggested_adapter: "meep",
      physical_system: "nanoparticle_on_film",
      workflow_focus: ["parse", "validate", "material_suggest", "workflow_plan", "adapter_preview"],
      maturity_note: "Meep/Gmsh preview path; material constants must be verified.",
      spec_path: "examples/optical_design/nanoparticle_plasmonics/spec.json",
      has_agent_trace: true,
      safety: {
        external_solver_executed: false,
        external_llm_required: false,
        production_grade_validation_claimed: false,
        formal_convergence_proof_claimed: false,
      },
    },
    {
      example_id: "thin_film_coating",
      title: "Thin Film Coating Preview",
      title_zh: "薄膜镀膜预览",
      design_goal: "Preview a thin-film coating stack workflow.",
      design_goal_zh: "预览一个薄膜叠层设计工作流。",
      category: "coating",
      suggested_materials: ["sio2", "tio2", "al2o3"],
      suggested_adapter: "preview-only; future TMM adapter candidate",
      physical_system: "thin_film_stack",
      workflow_focus: ["parse", "validate", "material_suggest", "workflow_plan", "artifact_preview"],
      maturity_note: "Preview-only; future TMM adapter candidate.",
      spec_path: "examples/optical_design/thin_film_coating/spec.json",
      has_agent_trace: true,
      safety: {
        external_solver_executed: false,
        external_llm_required: false,
        production_grade_validation_claimed: false,
        formal_convergence_proof_claimed: false,
      },
    },
  ],
};

export const demoExampleDetail: ExampleDetailResponse = {
  ...base,
  gallery_status: "local_preview_examples",
  gallery_note: "Use these examples for local Agent Studio workflow preview.",
  example: {
    summary: demoExamples.examples[0],
    spec: {
      example_id: "nanoparticle_plasmonics",
      design_goal: "Preview a local workflow for plasmonic nanoparticle scattering.",
      application: "nanoparticle plasmonics",
      suggested_materials: ["au", "ag", "sio2", "water", "air"],
      suggested_adapter: "meep",
    },
    expected_agent_trace: {
      expected_agents: ["SpecAgent", "MaterialAgent", "GeometryAgent", "AdapterAgent", "WorkflowAgent", "EvidenceAgent", "SafetyAgent", "RecommendationAgent"],
    },
    recommended_next_actions: [
      "Review material suggestions.",
      "Generate the agent trace timeline.",
      "Create a no-execute adapter preview.",
    ],
    safety_boundaries: [
      "No solver is executed by default.",
      "No external LLM is called by default.",
      "Preview artifacts are not production-grade physical validation.",
      "Formal convergence proof is not claimed.",
    ],
  },
};
