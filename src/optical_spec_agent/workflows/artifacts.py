"""Small artifact helpers for workflow orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from optical_spec_agent.workflows.models import WorkflowArtifact


def ensure_workflow_dirs(output_dir: Path) -> dict[str, Path]:
    """Create and return the standard v0.9 workflow directory layout."""
    output_dir.mkdir(parents=True, exist_ok=True)
    steps_dir = output_dir / "steps"
    artifacts_dir = output_dir / "artifacts"
    replay_dir = output_dir / "replay"
    for path in (steps_dir, artifacts_dir, replay_dir):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "root": output_dir,
        "steps": steps_dir,
        "artifacts": artifacts_dir,
        "replay": replay_dir,
    }


def jsonable(value: Any) -> Any:
    """Convert Pydantic/dataclass-ish values into JSON-serializable values."""
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    return value


def write_json(path: Path, payload: Any) -> Path:
    """Write JSON with UTF-8 and stable indentation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_text(path: Path, content: str) -> Path:
    """Write text with UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def artifact_from_path(
    *,
    name: str,
    path: Path,
    output_dir: Path,
    artifact_type: str,
    producer_step: str,
    description: str = "",
    required: bool = False,
) -> WorkflowArtifact:
    """Create a workflow artifact record."""
    return WorkflowArtifact.from_path(
        name=name,
        path=path,
        output_dir=output_dir,
        artifact_type=artifact_type,
        producer_step=producer_step,
        description=description,
        required=required,
    )
