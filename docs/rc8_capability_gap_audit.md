# rc8.dev0 Capability Gap Audit

Current public prerelease: `v0.9.0rc7`.
Current main development version: `0.9.0rc8.dev0`.

This audit identifies backend gaps that should be reviewed before any future
`v0.9.0rc8`, PyPI, or `v1.0.0` decision. It is preview/design-assist planning,
not production-grade physical validation.

## Release and Safety Status

- `v0.9.0rc8` tag: not created.
- `v1.0.0` tag: not created.
- PyPI: not published.
- PyPI publication approval: not granted.
- TestPyPI uploaded and verified only for `0.9.0rc6.dev0`.
- TestPyPI upload for `0.9.0rc8.dev0`: not performed.
- External solver execution: blocked by default.
- External LLM calls: blocked by default.
- Production-grade physical validation: not claimed.
- Formal convergence proof: not claimed.
- Elmer Level 3: deferred; Elmer remains Level 2 + Level-3-ready.

## Gap Matrix

| Capability | Current state | Gap | Risk | Recommended rc8 action |
| --- | --- | --- | --- | --- |
| Sub-agent reality | Deterministic roles execute in traces and audit | Roles are not standalone autonomous packages/classes | Maintainers may overread "agent" as independent installed agents | Keep audit wording explicit and add examples showing deterministic orchestration. |
| Tool-call ledger | Records internal calls and blocked external actions | Ledger is session-scoped, not persisted across runs | Harder to compare historical evidence | Add optional JSON export examples before rc8 draft. |
| Material library | Local preview catalog, provenance fields, suitability diagnostics, and suggestions | Preview optical constants still require external human verification | Material suggestions may be mistaken for authoritative constants | Keep provenance warnings prominent and add application-specific review cases. |
| Optical calculators | Reference sanity cases exist, including fiber coupling and Jones polarization checks | Limited domains and simplified assumptions | Users may apply preview outputs outside supported assumptions | Add more failure-mode tests and assumption summaries when new calculators are added. |
| Source/monitor diagnostics | Template and goal inference plus critical/optional missing-input diagnostics exists | Ambiguous multi-source/multi-monitor cases can still be deeper | Missing inputs may be underreported for novel systems | Continue expanding negative and multi-observable examples. |
| Observable diagnostics | Taxonomy and adapter compatibility exist | Combined observables need richer required-input handling | Preview artifacts may hide observable prerequisites | Add multi-observable cases and expected warnings. |
| Adapter-native mappings | Five adapters mapped with golden metadata | Mapping is preview metadata, not executed solver semantics | Real solver users may expect monitor results | Keep `solver_execution_required_for_real_result` prominent. |
| Adapter golden coverage | Strict metadata diffs cover five golden cases | Coverage is narrow per adapter | Adapter changes can pass without broader semantic coverage | Add one additional case per adapter when adapter previews change. |
| Design requirement templates | Seven templates and deterministic matching exist | Requirements lack tolerance/optimization constraints | Goals may not capture design acceptance criteria | Add tolerance, sweep, and pass/fail fields for candidate templates. |
| Natural-language to optical-language matching | Deterministic heuristic EN/ZH matching, candidate templates, confidence, and questions exist | Novel phrasing may still need more negative examples | Unexpected matches can produce misleading plans | Keep adding ambiguous/negative cases and confidence-threshold tests. |
| Application domain coverage | Ten domains map to templates, materials, calculators/adapters, and missing-input questions | Fiber coupling and polarization now have deterministic preview calculators, but real coupling/vector validation remains deferred | Domain coverage could be mistaken for full physical validation | Keep pass/warning/fail semantics explicit and require explicit solver or experimental evidence for physical validation. |
| Material-template cross-checks | Domain checks verify templates, local materials, expected tools, and questions | Cross-checks are preview metadata, not solver evidence | Users may overread pass status as production readiness | Keep preview-only wording and material user-verification flags prominent. |
| Application-domain benchmarks | Positive, ambiguous, underconstrained, unsupported, and unsafe/blocked scenarios exercise domain behavior | Fiber coupling and polarization warning cases are closed by preview calculators | Benchmark pass could be mistaken for physical validation | Keep benchmark result policy explicit and add scenarios as new domains are introduced. |
| Frontend Agent Studio | Local MVP exists | Backend evidence is not yet summarized in UI | Maintainer review remains docs/scripts-first | Defer until backend evidence shape stabilizes. |
| PyPI publication | Deferred and not approved | No final PyPI approval path executed | Publishing before decision could create irreversible public surface | Keep PyPI gate closed until explicit approval. |
| v1.0.0 criteria | Public contract freeze approved | PyPI decision, final release readiness, and validation boundaries remain open | Premature v1.0.0 could overstate maturity | Use rc8 gap closure and separate v1.0 planning package. |
| Elmer Level 3 | Level 2 + Level-3-ready, install deferred | No completed ElmerSolver execution evidence | Level 3 would overclaim current validation | Keep deferred until maintainable install route and opt-in validation pass. |

## Capability Gaps Found

1. Calculator depth remains preview-oriented.
   The local calculators are useful for sanity checks and design-assist
   summaries, but they are not production-grade physical validation.

2. Material provenance should be strengthened; rc8.dev0 has already made the
   first strengthening pass.
   Starter materials now expose provenance fields and suitability diagnostics,
   but all optical constants still require independent user verification.

3. Natural-language matching should add negative and ambiguous examples; rc8.dev0
   now has an initial negative/ambiguous example set.
   The deterministic matcher should continue to prefer safe low/none confidence
   diagnostics and questions over overconfident case selection.

4. Adapter-native mapping evidence is metadata-only.
   Golden cases prove preview semantics and safety boundaries, not real solver
   monitor results.

5. Elmer remains explicitly deferred.
   Elmer is not Level 3 and should remain non-blocking until installation and
   opt-in validation become maintainable.

## Non-gaps / Stable Enough

- Current public prerelease remains `v0.9.0rc7`.
- Main development version is `0.9.0rc8.dev0`.
- Backend evidence pack, backend capability report, sub-agent audit, and
  adapter golden coverage are available.
- Application-domain registry and material-template cross-checks are available
  for ten preview domains, including fiber coupling and polarization preview
  calculators with solver validation still deferred.
- Tool-call ledger records blocked solver/LLM/publication/release actions.
- PyPI is not published and publication approval remains not granted.
- No `v0.9.0rc8` or `v1.0.0` tag is created.

## Decision Impact

This audit supports continued v1.0 readiness/backend engineering. It does not
approve a `v0.9.0rc8` release draft, TestPyPI upload, PyPI publication, tag
creation, GitHub release creation, or `v1.0.0` release.

## Validation Maturity Gap Status

Validation maturity is now tracked explicitly in
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md).
The remaining gap is not missing labels; it is deeper optional validation beyond
preview evidence. That future work must stay separate from PyPI and release
decisions unless maintainers explicitly decide otherwise.
