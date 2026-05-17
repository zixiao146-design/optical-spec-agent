import type {
  AdapterPreviewResponse,
  AdaptersResponse,
  HealthResponse,
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
  package_version: "0.9.0rc7.dev0",
  current_public_prerelease: "v0.9.0rc6",
  main_development_version: "0.9.0rc7.dev0",
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
  current_public_prerelease: "v0.9.0rc6",
  main_development_version: "0.9.0rc7.dev0",
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
