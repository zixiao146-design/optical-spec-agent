# v1.0 Contract Non-goals

The following items are explicitly outside the approved v1.0 frozen public
contract unless a future maintainer decision changes the scope.

- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.
- External solvers are not default dependencies.
- External LLM is not default dependency.
- Proprietary solvers are not default targets.
- Generated adapter internals are not frozen.
- Workflow internals are not frozen.
- Optional solver validation internals are not frozen.
- Elmer Level 3 is deferred.
- PyPI publication is not yet approved.
- `v1.0.0` final release is not yet approved.

These non-goals keep the v1.0 public contract focused on the documented CLI,
schema, adapter registry, examples, workflow-plan public shape, package
metadata, and default no-network/no-solver/no-LLM/no-proprietary guarantees.

The approved freeze does not convert these non-goals into supported claims.
