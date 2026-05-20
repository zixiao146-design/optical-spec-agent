# Solver Evidence Validation Maturity Mapping zh-CN

Current public prerelease: v0.9.0rc7.
Current main release draft: `0.9.0rc8`.

本文说明 optional solver micro-benchmark evidence 如何映射到保守的 backend
validation maturity model。

## Mapping Table

| Solver | Evidence status | Maturity mapping | Default gates | Boundary |
| --- | --- | --- | --- | --- |
| Gmsh | executed / passed / reviewed / accepted | optional manual mesh-generation smoke evidence | 默认不执行 solver | 不是 optical correctness evidence |
| Optiland | executed / passed / reviewed / accepted | optional manual ray/path smoke evidence | 默认不执行 solver | 不是 production-grade optical design validation |
| Meep | executed / passed / reviewed / accepted | optional manual PyMeep/FDTD smoke evidence | 默认不执行 solver | 不是 production-grade FDTD validation |
| MPB | executed / passed / reviewed / accepted | optional manual MPB/band-structure smoke evidence | 默认不执行 solver | 不是 production band-structure validation |
| Elmer | deferred / not executed | documented preview / deferred | 默认不执行 solver | not Level 3 |

## Maturity Interpretation

Optional manual solver evidence 表示 maintainer 明确批准了某个 solver-specific
opt-in run，该 run passed，并且 review decision 接受为该 solver path 的 smoke
evidence。它不会让 solver 成为 default dependency，也不会把 solver execution
加入 pytest、smoke、quality 或 release gates。

## Non-claims

- 不声明 production-grade physical validation。
- 不声明 production-grade solver validation。
- 不声明 formal convergence proof。
- 不声明 optical correctness。
- PyPI publication 仍然单独 gate，并且不代表 production-grade validation。

## Elmer

Elmer 继续 deferred，直到存在可维护的 `ElmerSolver` install route。本 review
中 Elmer 不是 Level 3。

