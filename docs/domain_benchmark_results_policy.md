# Domain Benchmark Results Policy

Application-domain benchmark results are backend-readiness signals, not
production validation. They help maintainers see whether local deterministic
matching, material/template coverage, calculator/adapter expectations,
missing-input diagnostics, and safety boundaries remain stable.
The policy covers positive, ambiguous, underconstrained, unsupported, and
unsafe/blocked scenario types.

## How To Interpret Results

- `pass` means the local preview behavior matched the scenario expectation.
- `warn` means the backend stayed safe, but the domain is partial, deferred, or
  intentionally under-specified.
- `fail` means an expected safety, matching, diagnostic, or tool-call behavior
  changed and requires review.

Warnings are useful because they prevent partial coverage from masquerading as
complete optical-design validation. For example, fiber coupling and
polarization optics can be represented as planning domains while dedicated
physical calculators or solver validation remain future work.

## Unsupported and Commercial Requests

Requests for full Zemax optimization, full Lumerical FDTD execution, real solver
monitor results, production-ready prescription files, production-grade physical
validation, or formal convergence proof are blocked or deferred by default.
The backend may recommend local preview alternatives, but it does not execute
external solvers, call external LLMs, require proprietary solvers, upload
packages, create tags, or create releases.

## Safe Default Action

When a scenario is ambiguous or underconstrained, the backend should ask
questions and expose missing inputs instead of silently choosing an unsafe path.
When a scenario is unsupported, it should record blocked actions and keep
`external_solver_executed=false`, `external_llm_required=false`,
`production_grade_validation_claimed=false`, and
`formal_convergence_proof_claimed=false`.

## Scope Limitations

Benchmark results are preview/design-assist evidence. They do not validate
material constants, do not prove real solver results, and do not imply Elmer
Level 3 validation. PyPI publication, TestPyPI upload, tag creation, GitHub
release creation, and v1.0.0 release decisions remain separate maintainer
approvals.
