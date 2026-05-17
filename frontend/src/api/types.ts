export interface SafetyFlags {
  external_solver_executed: boolean;
  external_llm_required: boolean;
  proprietary_solver_required: boolean;
  production_grade_validation_claimed: boolean;
  formal_convergence_proof_claimed: boolean;
}

export interface ApiDiagnostic {
  errors: string[];
  warnings: string[];
  missing_fields: string[];
  assumptions: string[];
  limitations: string[];
  details: Record<string, unknown>;
}

export interface ApiResponseBase extends SafetyFlags {
  api_contract_version: string;
  status: string;
  diagnostics: ApiDiagnostic;
  recommended_next_actions: string[];
}

export interface HealthResponse extends ApiResponseBase {
  service: string;
}

export interface VersionResponse extends ApiResponseBase {
  package_version: string;
  current_public_prerelease: string;
  main_development_version: string;
  pypi_published: boolean;
  testpypi_verified: boolean;
  testpypi_verified_version: string;
}

export interface AdapterSummary {
  tool_name: string;
  display_name: string;
  solver_family: string;
  current_status: string;
  maturity_level: string;
  evidence?: string | null;
  external_solver_required_by_default: boolean;
  production_grade_validation_claimed: boolean;
  formal_convergence_proof_claimed: boolean;
  limitations: string[];
}

export interface AdaptersResponse extends ApiResponseBase {
  adapters: AdapterSummary[];
}

export interface SchemaResponse extends ApiResponseBase {
  schema_name: string;
  schema: Record<string, unknown>;
}

export interface ParseRequest {
  text: string;
  task_id?: string;
  parser?: "heuristic" | "rule";
  json?: boolean;
}

export interface ParseResponse extends ApiResponseBase {
  parser: string;
  spec: Record<string, unknown>;
  summary: string;
}

export interface ValidateRequest {
  spec?: Record<string, unknown>;
  path?: string;
}

export interface ValidateResponse extends ApiResponseBase {
  valid: boolean;
}

export interface WorkflowPlanRequest extends ValidateRequest {
  text?: string;
  parser?: "heuristic" | "rule";
  tool?: string;
}

export interface WorkflowPlanResponse extends ApiResponseBase {
  workflow_plan: Record<string, unknown>;
  public_top_level_keys: string[];
}

export interface AdapterPreviewRequest extends ValidateRequest {
  tool: string;
}

export interface AdapterPreviewResponse extends ApiResponseBase {
  tool: string;
  display_name: string;
  output_language: string;
  output_extension: string;
  preview_content: string;
  artifact_summary: Record<string, unknown>;
}

export interface ValidationEvidenceItem {
  tool_name: string;
  display_name: string;
  maturity_level: string;
  evidence?: string | null;
  status_note: string;
  production_grade_validation_claimed: boolean;
  formal_convergence_proof_claimed: boolean;
}

export interface ValidationEvidenceResponse extends ApiResponseBase {
  validation_evidence: ValidationEvidenceItem[];
}

export interface ReadinessResponse extends ApiResponseBase {
  current_public_prerelease: string;
  main_development_version: string;
  testpypi: Record<string, unknown>;
  pypi: Record<string, unknown>;
  public_contract_freeze: Record<string, unknown>;
  adapter_maturity: Record<string, string>;
  v1_0_0_released: boolean;
}

export interface RefractiveIndexModel {
  kind: string;
  n?: number | null;
  k?: number | null;
  wavelength_nm?: number | null;
}

export interface MaterialSummary {
  material_id: string;
  display_name: string;
  aliases: string[];
  category: string;
  common_use: string[];
  optical_role: string;
  production_grade: boolean;
  validation_level: string;
  source_note: string;
}

export interface MaterialDetail extends MaterialSummary {
  wavelength_range_nm?: [number, number] | null;
  refractive_index_model: RefractiveIndexModel;
  notes: string[];
}

export interface MaterialsResponse extends ApiResponseBase {
  materials: MaterialSummary[];
  catalog_status: string;
  catalog_note: string;
}

export interface MaterialDetailResponse extends ApiResponseBase {
  material: MaterialDetail;
  catalog_status: string;
  catalog_note: string;
}

export interface MaterialSuggestionRequest {
  application: string;
  wavelength_nm?: number;
}

export interface MaterialSuggestionResponse extends ApiResponseBase {
  application: string;
  suggested_materials: MaterialSummary[];
  catalog_status: string;
  catalog_note: string;
}

export interface AgentStep {
  step_index: number;
  agent_name: string;
  role: string;
  stage: string;
  input_summary: string;
  output_summary: string;
  diagnostics: string[];
  recommended_next_actions: string[];
  confidence: string;
  status: string;
  safety_notes: string[];
  evidence_refs: string[];
}

export interface AgentTraceRequest {
  spec?: Record<string, unknown>;
  text?: string;
  example_id?: string;
}

export interface AgentTraceResponse extends ApiResponseBase {
  trace_id: string;
  example_id?: string | null;
  design_goal: string;
  timeline_summary: string;
  agents: AgentStep[];
  final_recommendation: string;
  material_suggestions: string[];
  adapter_recommendation: string;
}

export type AgentPlanStatus = "pending" | "completed" | "warning" | "blocked";
export type PermissionGateStatus = "allowed" | "blocked" | "requires_explicit_approval";

export interface AgentPlanStep {
  step_index: number;
  title: string;
  title_zh: string;
  description: string;
  description_zh: string;
  agent_name: string;
  status: AgentPlanStatus;
  endpoint_or_tool: string;
  expected_output: string;
  safety_note: string;
}

export interface AgentArtifact {
  artifact_id: string;
  label: string;
  label_zh: string;
  artifact_type:
    | "spec"
    | "workflow_plan"
    | "adapter_preview"
    | "agent_trace"
    | "material_suggestions"
    | "evidence";
  summary: string;
  preview_content?: string | null;
  source_endpoint: string;
  generated_by_agent: string;
  production_grade: boolean;
}

export interface PermissionGate {
  gate_id: string;
  label: string;
  label_zh: string;
  status: PermissionGateStatus;
  reason: string;
  risk_level: "low" | "medium" | "high";
  default_allowed: boolean;
}

export interface AgentSessionRequest {
  goal: string;
  example_id?: string | null;
  language?: "en" | "zh-CN";
}

export interface AgentTaskSessionResponse extends ApiResponseBase {
  session_id: string;
  user_goal: string;
  optical_intent_summary: string;
  selected_example_id?: string | null;
  design_case_summary: string;
  plan_steps: AgentPlanStep[];
  agent_trace: AgentTraceResponse;
  artifacts: AgentArtifact[];
  permission_gates: PermissionGate[];
  final_recommendation: string;
}

export interface ExampleSafety {
  external_solver_executed: boolean;
  external_llm_required: boolean;
  production_grade_validation_claimed: boolean;
  formal_convergence_proof_claimed: boolean;
}

export interface OpticalDesignExampleSummary {
  example_id: string;
  title: string;
  title_zh: string;
  design_goal: string;
  design_goal_zh: string;
  category: string;
  suggested_materials: string[];
  suggested_adapter: string;
  physical_system: string;
  workflow_focus: string[];
  maturity_note: string;
  spec_path: string;
  has_agent_trace: boolean;
  safety: ExampleSafety;
}

export interface OpticalDesignExampleDetail {
  summary: OpticalDesignExampleSummary;
  spec: Record<string, unknown>;
  expected_agent_trace: Record<string, unknown>;
  recommended_next_actions: string[];
  safety_boundaries: string[];
}

export interface ExamplesResponse extends ApiResponseBase {
  examples: OpticalDesignExampleSummary[];
  gallery_status: string;
  gallery_note: string;
}

export interface ExampleDetailResponse extends ApiResponseBase {
  example: OpticalDesignExampleDetail;
  gallery_status: string;
  gallery_note: string;
}

export interface ApiErrorResponse extends ApiResponseBase {
  status: "error";
  error_code: string;
  message: string;
}

export type ApiResult<T> = T | ApiErrorResponse;
