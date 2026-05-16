import type {
  AdapterPreviewRequest,
  AdapterPreviewResponse,
  AdaptersResponse,
  ApiErrorResponse,
  ApiResult,
  HealthResponse,
  ParseRequest,
  ParseResponse,
  ReadinessResponse,
  SchemaResponse,
  ValidateRequest,
  ValidateResponse,
  ValidationEvidenceResponse,
  VersionResponse,
  WorkflowPlanRequest,
  WorkflowPlanResponse,
} from "./types";

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const SAFE_ERROR_FLAGS = {
  external_solver_executed: false,
  external_llm_required: false,
  proprietary_solver_required: false,
  production_grade_validation_claimed: false,
  formal_convergence_proof_claimed: false,
};

function endpoint(path: string): string {
  if (!path.startsWith("/api/")) {
    throw new Error(`Unsafe API path: ${path}`);
  }
  return `${API_BASE_URL.replace(/\/$/, "")}${path}`;
}

function localError(message: string): ApiErrorResponse {
  return {
    api_contract_version: "0.1",
    status: "error",
    error_code: "frontend_request_error",
    message,
    diagnostics: {
      errors: [message],
      warnings: [],
      missing_fields: [],
      assumptions: [],
      limitations: [],
      details: {},
    },
    recommended_next_actions: [
      "Check that the local Agent API is running on the configured API base URL.",
    ],
    ...SAFE_ERROR_FLAGS,
  };
}

async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<ApiResult<T>> {
  try {
    const response = await fetch(endpoint(path), {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init.headers || {}),
      },
    });
    const payload = (await response.json()) as ApiResult<T>;
    if (!response.ok && typeof payload === "object" && payload !== null) {
      return payload;
    }
    return payload;
  } catch (error) {
    return localError(error instanceof Error ? error.message : String(error));
  }
}

function post<T, B>(path: string, body: B): Promise<ApiResult<T>> {
  return request<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export const agentApi = {
  getHealth: () => request<HealthResponse>("/api/health"),
  getVersion: () => request<VersionResponse>("/api/version"),
  getAdapters: () => request<AdaptersResponse>("/api/adapters"),
  getSchema: () => request<SchemaResponse>("/api/schema"),
  parseSpec: (body: ParseRequest) => post<ParseResponse, ParseRequest>("/api/parse", body),
  validateSpec: (body: ValidateRequest) =>
    post<ValidateResponse, ValidateRequest>("/api/validate", body),
  getWorkflowPlan: (body: WorkflowPlanRequest) =>
    post<WorkflowPlanResponse, WorkflowPlanRequest>("/api/workflow-plan", body),
  getAdapterPreview: (body: AdapterPreviewRequest) =>
    post<AdapterPreviewResponse, AdapterPreviewRequest>("/api/adapter-preview", body),
  getValidationEvidence: () =>
    request<ValidationEvidenceResponse>("/api/validation-evidence"),
  getReadiness: () => request<ReadinessResponse>("/api/readiness"),
};
