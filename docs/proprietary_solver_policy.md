# Proprietary Solver Policy

## Current policy

- Proprietary tools are not default dependencies.
- Proprietary tools are not required for default tests.
- Proprietary tools are not required for `scripts/smoke_release.sh`.
- Proprietary tools are not required for GitHub prerelease validation.
- Proprietary tools are not required for examples.

## Commercial tools

The following commercial tools are not default supported backends in the current
project:

- Zemax
- Lumerical
- COMSOL
- proprietary Ansys optics tools

They are not registered default adapters unless source code explicitly registers
them in the adapter registry.

## Future optional export-only stance

Future support, if added, should be export-only or manually executed unless
explicitly approved. Export-only means generating scripts, templates, or configs
that a user may inspect and run manually.

Export-only does not mean solver-backed correctness. Export-only does not mean
production-grade validation. Export-only does not make a commercial solver a
default test, smoke, example, or release-validation dependency.

## Testing policy

- No CI test should require a proprietary license.
- No default smoke test should require a proprietary license.
- No release gate should require a proprietary license.
- Any proprietary integration test must be optional, manual, and skipped by
  default.

## Documentation policy

- Docs must not imply proprietary tools are required.
- Docs must not imply commercial solver validation unless evidence exists.
- README should keep proprietary tools out of the default quickstart.
- Commercial names may appear in compatibility, policy, or export-only contexts
  only when the non-default boundary is explicit.
