"""Workflow parse agent."""

from __future__ import annotations

import json

from optical_spec_agent.parsers.llm import LLMParserConfig
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json
from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult


class ParseAgent(WorkflowAgent):
    """Run rule/LLM/hybrid parsing and write spec artifacts."""

    name = "parse"

    def run(self, context: WorkflowContext) -> AgentResult:
        config = LLMParserConfig(
            provider=context.config.llm_provider,
            parser_mode="hybrid" if context.config.parser == "hybrid" else "llm",
        )
        service = SpecService(parser=context.config.parser, llm_config=config)
        spec = service.process(context.input_text, task_id=context.run_id)
        context.current_spec = spec
        context.parser_report = (
            service.last_parser_report.model_dump(mode="json")
            if service.last_parser_report is not None
            else None
        )
        context.assumptions.extend(spec.assumption_log)

        spec_path = context.dirs["artifacts"] / "spec.json"
        spec_path.write_text(spec_to_json(spec), encoding="utf-8")

        artifacts = {
            "spec.json": artifact_from_path(
                name="spec.json",
                path=spec_path,
                output_dir=context.output_dir,
                artifact_type="spec",
                producer_step=self.name,
                description="Validated OpticalSpec JSON.",
                required=True,
            )
        }
        payload = {
            "parser": context.config.parser,
            "task_id": spec.task.task_id,
            "missing_fields": spec.missing_fields,
            "validation_errors": spec.validation_status.errors,
            "validation_warnings": spec.validation_status.warnings,
        }
        if context.parser_report is not None:
            report_path = context.dirs["artifacts"] / "parser_report.json"
            write_json(report_path, context.parser_report)
            artifacts["parser_report.json"] = artifact_from_path(
                name="parser_report.json",
                path=report_path,
                output_dir=context.output_dir,
                artifact_type="parser_report",
                producer_step=self.name,
                description="Rule/LLM/hybrid parser report.",
            )

        summary_path = context.dirs["artifacts"] / "parse_summary.json"
        write_json(summary_path, payload)
        artifacts["parse_summary.json"] = artifact_from_path(
            name="parse_summary.json",
            path=summary_path,
            output_dir=context.output_dir,
            artifact_type="summary",
            producer_step=self.name,
            description="Parse step summary.",
        )

        # Ensure parser output remains JSON serializable while keeping failures explicit.
        json.loads(spec_path.read_text(encoding="utf-8"))
        parse_warnings = [*spec.validation_status.warnings, *spec.validation_status.errors]
        return AgentResult(
            status="warning" if parse_warnings else "success",
            payload=payload,
            artifacts=artifacts,
            warnings=parse_warnings,
            errors=[],
            assumptions=list(spec.assumption_log),
        )
