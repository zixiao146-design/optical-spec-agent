# v1.0 Stability Gate

## Purpose

`v1.0` should not be declared until public CLI/API/schema/adapter/workflow
behavior is stable enough for downstream users.

## Required stability areas

- CLI contract
- Schema contract
- Parser behavior
- Adapter support matrix
- Workflow preview contract
- Validation boundary
- Packaging gate
- TestPyPI/PyPI decision
- Token/security policy
- Release rollback policy

## Current status

- Current public prerelease: v0.9.0rc6
- Current main release draft: 0.9.0rc7
- Product positioning: open-source-solver-first
- v1.0.0 not ready yet
- Production-grade physical validation not claimed
- Formal convergence proof not claimed
- External solver validation is optional/manual
- External LLM is optional and not required by default
- Proprietary solvers are not default dependencies
- No proprietary license is required for default tests, smoke, examples, or
  release validation

## Minimum v1.0 exit criteria

- Stable CLI surface
- Stable schema/API compatibility policy
- Documented adapter support levels
- Documented validation claims
- Reproducible release process
- Packaging/TestPyPI/PyPI decision documented
- No accidental token exposure in docs/logs
- No default external solver/LLM requirement
- Rollback/yanking strategy documented if PyPI is used
