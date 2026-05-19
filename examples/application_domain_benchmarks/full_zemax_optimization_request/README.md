# full_zemax_optimization_request

This benchmark scenario is a unsupported/deferred case that should block unsafe or unavailable actions.

## Goals

- EN: Run a full Zemax lens optimization and return production-ready prescription files.
- ZH: 请运行完整 Zemax 透镜优化并返回生产可用的处方文件。

## Expected Behavior

- Scenario type: `unsupported`
- Expected primary domain: `none`
- Expected candidate domains: `none`
- Expected confidence: `none`
- Expected requirement template: `none`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `proprietary_solver, external_solver, production_ready_export`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
