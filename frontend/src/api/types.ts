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

export interface ApiErrorResponse extends ApiResponseBase {
  status: "error";
  error_code: string;
  message: string;
}

export type ApiResult<T> = T | ApiErrorResponse;
