# Agent Studio Frontend Visual Smoke Plan

## Purpose

This plan defines future screenshot checks for the Agent Studio frontend MVP.
It is not required for the current MVP hardening task, and it does not add
Playwright or any browser automation dependency yet.

## Pages to Screenshot

- Dashboard
- Spec Input
- Adapter Matrix
- Workflow Plan
- Artifact Preview
- Validation Evidence
- System Status

## States to Cover

- API connected state with live local API responses.
- API disconnected/demo mode state with fixture-backed content.
- Loading state during pending local API calls.
- Empty state before parse, validate, workflow, or preview actions.
- Error state for invalid JSON or stable API error responses.

## Safety Checks

Future visual smoke checks should confirm:

- No upload/release controls are visible.
- No PyPI/TestPyPI publication controls are visible.
- No tag/release controls are visible.
- No default solver or external LLM controls are visible.
- Preview and validation boundaries remain visible.
- Demo fixture mode is labeled as not live validation.

## Future Tooling

Playwright or an equivalent lightweight screenshot tool can be added later.
When added, it should run against local-only frontend and API processes and
should not access external networks, execute solvers, call external LLMs,
upload packages, create tags, or create releases.
