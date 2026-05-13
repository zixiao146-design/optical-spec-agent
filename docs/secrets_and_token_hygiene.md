# Secrets and Token Hygiene

## Scope

This policy covers:

- GitHub tokens
- TestPyPI tokens
- PyPI tokens
- external LLM API keys
- proprietary solver licenses or credentials

## Rules

- Never paste tokens into chat.
- Never commit tokens.
- Never print tokens.
- Never save tokens in docs, logs, or generated reports.
- Use `read -s` for local terminal entry when a token is truly required.
- Unset token environment variables after use.
- Revoke exposed tokens immediately.
- Use least-privilege tokens.
- TestPyPI and PyPI tokens are separate from GitHub tokens.
- TestPyPI upload requires explicit approval.
- PyPI publication requires separate explicit approval.

## Script Policy

- Smoke scripts must not require tokens.
- Quality gates must not require tokens.
- Preflight must not require upload tokens.
- Release creation tasks may require a GitHub token, but must not print it.
- Upload tasks may require a TestPyPI or PyPI token, but only after explicit
  approval.

## Incident Response

- If a token is pasted into chat or logs, revoke it.
- Rotate the token.
- Check git history before commit.
- Do not continue using an exposed token.
- Record the incident and the replacement decision outside public release notes
  if the details would expose credential material.
