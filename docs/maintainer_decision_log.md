# Maintainer Decision Log

## Current Decisions

- v0.9.0rc4 is the current public prerelease.
- main moved to 0.9.0rc5.dev0 for post-rc4 development.
- TestPyPI upload approval: pending.
- Upload command authorized: no.
- PyPI publication approval: not granted.
- Continue v1.0 readiness engineering.
- Do not create v0.9.0rc5 tag now.
- Do not create a GitHub release now.
- Do not use proprietary solvers as default dependencies.
- Do not require external solver or external LLM by default.
- Do not publish PyPI without explicit approval.
- Do not upload TestPyPI without explicit approval.

## Safety Notes

- Tokens must not be printed, committed, logged, or pasted into chat.
- Default smoke, quality, and preflight scripts remain no-upload and no-release.
- Existing release tags must not be moved, deleted, or re-created.
