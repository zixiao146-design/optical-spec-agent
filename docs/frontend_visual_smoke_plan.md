# Agent Studio Frontend Visual Smoke Plan

## Purpose

This plan defines lightweight local visual smoke checks for the Agent Studio
frontend MVP. Playwright visual smoke support is now added as a manual optional
check. It is not part of the default release gate or `run_quality_gates.sh`
unless a maintainer explicitly promotes it later.

Runbook: [`frontend_visual_smoke_runbook.md`](frontend_visual_smoke_runbook.md).

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

The Playwright smoke checks should confirm:

- No upload/release controls are visible.
- No PyPI/TestPyPI publication controls are visible.
- No tag/release controls are visible.
- No default solver or external LLM controls are visible.
- Preview and validation boundaries remain visible.
- Demo fixture mode is labeled as not live validation.

## Current Tooling

- Playwright config: `frontend/playwright.config.ts`.
- Visual smoke test: `frontend/tests/visual/agent-studio-smoke.spec.ts`.
- Manual wrapper: `scripts/smoke_frontend_visual.sh`.

The smoke is assertion-first rather than snapshot-first. Screenshots and HTML
reports are written only to ignored Playwright output directories and should
not be committed by default.

The check runs against local-only frontend and API processes. It should not
access external networks from the frontend, execute solvers, call external
LLMs, upload packages, create tags, or create releases.
