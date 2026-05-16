import type { ApiErrorResponse, ApiResult } from "./types";

export type RemoteStatus = "idle" | "loading" | "ready" | "demo" | "error";

export interface RemoteState<T> {
  status: RemoteStatus;
  data?: T;
  error?: ApiErrorResponse;
  message?: string;
}

export const INITIAL_LOADING_STATE = {
  status: "loading",
  message: "Loading from the local Agent API.",
} as const;

export function isApiError(payload: unknown): payload is ApiErrorResponse {
  return (
    typeof payload === "object" &&
    payload !== null &&
    (payload as { status?: string }).status === "error" &&
    typeof (payload as { error_code?: unknown }).error_code === "string"
  );
}

export function isApiDisconnected(payload: unknown): payload is ApiErrorResponse {
  return isApiError(payload) && payload.error_code === "frontend_request_error";
}

export function stateFromPayload<T>(
  payload: ApiResult<T>,
  demoData: T,
  demoMessage: string,
): RemoteState<T> {
  if (isApiDisconnected(payload)) {
    return {
      status: "demo",
      data: demoData,
      error: payload,
      message: demoMessage,
    };
  }
  if (isApiError(payload)) {
    return {
      status: "error",
      error: payload,
      message: payload.message,
    };
  }
  return {
    status: "ready",
    data: payload,
    message: "Live local API response.",
  };
}

export function jsonParseError(error: unknown): ApiErrorResponse {
  const message = error instanceof Error ? error.message : String(error);
  return {
    api_contract_version: "0.1",
    status: "error",
    error_code: "invalid_json",
    message,
    diagnostics: {
      errors: [message],
      warnings: [],
      missing_fields: [],
      assumptions: [],
      limitations: [],
      details: {},
    },
    recommended_next_actions: ["Fix the JSON request and try again."],
    external_solver_executed: false,
    external_llm_required: false,
    proprietary_solver_required: false,
    production_grade_validation_claimed: false,
    formal_convergence_proof_claimed: false,
  };
}
