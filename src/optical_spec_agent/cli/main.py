"""CLI entry-point powered by Typer."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.utils.format import spec_to_json, spec_to_summary

app = typer.Typer(
    name="optical-spec",
    help="Optical Spec Agent — NL -> validated simulation spec",
    add_completion=False,
)
console = Console()


# ---- parse ----

@app.command()
def parse(
    text: str = typer.Argument(..., help="Natural language task description"),
    task_id: str = typer.Option("", "--task-id", "-t", help="Optional task ID"),
    output: Path = typer.Option(None, "--output", "-o", help="Write JSON to file"),
    show_json: bool = typer.Option(False, "--json", help="Print raw JSON to stdout"),
    parser_name: str = typer.Option(
        "rule",
        "--parser",
        help="Parser mode: rule, llm, or hybrid",
    ),
    llm_provider: str = typer.Option(
        "mock",
        "--llm-provider",
        help="LLM provider for llm/hybrid parser modes: mock or disabled",
    ),
    llm_model: str = typer.Option(
        "mock-optical-parser",
        "--llm-model",
        help="Model name recorded in parser reports",
    ),
    llm_temperature: float = typer.Option(
        0.0,
        "--llm-temperature",
        help="LLM temperature recorded in parser config",
    ),
    no_llm_repair: bool = typer.Option(
        False,
        "--no-llm-repair",
        help="Disable common JSON repair for LLM responses",
    ),
    no_llm_fallback: bool = typer.Option(
        False,
        "--no-llm-fallback",
        help="Disable fallback to the rule-based parser on LLM failure",
    ),
    show_parser_report: bool = typer.Option(
        False,
        "--show-parser-report",
        help="Print parser report in human-readable mode",
    ),
    parser_report_output: Path | None = typer.Option(
        None,
        "--parser-report-output",
        help="Write parser report JSON to a file",
    ),
):
    """Parse natural language into a validated spec."""
    from optical_spec_agent.parsers.llm import LLMParserConfig, LLMProviderError
    from optical_spec_agent.parsers.registry import ParserRegistryError

    try:
        text, request_options = _resolve_text_request(text)
        parser_name = request_options.get("parser", parser_name)
        llm_provider = request_options.get("llm_provider", llm_provider)
        llm_model = request_options.get("llm_model", llm_model)
    except ValueError as exc:
        if show_json:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Parser input error:[/red] {exc}")
        raise typer.Exit(1)

    if show_json and show_parser_report and parser_report_output is None:
        typer.echo("--show-parser-report cannot be mixed with --json unless --parser-report-output is set.")
        raise typer.Exit(1)

    llm_config = LLMParserConfig(
        provider=llm_provider,
        model=llm_model,
        temperature=llm_temperature,
        allow_repair=not no_llm_repair,
        fallback_to_rule_based=not no_llm_fallback,
        parser_mode="hybrid" if parser_name == "hybrid" else "llm",
    )
    try:
        svc = SpecService(parser=parser_name, llm_config=llm_config)
        spec = svc.process(text, task_id=task_id)
    except (ParserRegistryError, LLMProviderError, Exception) as exc:
        if show_json:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Parser error:[/red] {exc}")
        raise typer.Exit(1)

    if show_json:
        typer.echo(spec_to_json(spec))
    else:
        console.print(spec_to_summary(spec))
        if show_parser_report and svc.last_parser_report is not None:
            console.print("\n[bold]Parser report[/bold]")
            console.print_json(json.dumps(svc.last_parser_report.model_dump(), ensure_ascii=False))

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(spec_to_json(spec), encoding="utf-8")
        if not show_json:
            console.print(f"\n[dim]JSON written to {output}[/dim]")

    if parser_report_output and svc.last_parser_report is not None:
        parser_report_output.parent.mkdir(parents=True, exist_ok=True)
        parser_report_output.write_text(
            json.dumps(svc.last_parser_report.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        if not show_json:
            console.print(f"[dim]Parser report written to {parser_report_output}[/dim]")


@app.command("llm-eval")
def llm_eval(
    benchmark_file: Path = typer.Argument(..., help="Path to LLM benchmark JSON cases"),
    parser_name: str = typer.Option(
        "hybrid",
        "--parser",
        help="Parser mode: llm or hybrid",
    ),
    llm_provider: str = typer.Option("mock", "--llm-provider", help="LLM provider: mock or disabled"),
    llm_model: str = typer.Option(
        "mock-optical-parser",
        "--llm-model",
        help="Model name recorded in the report",
    ),
    report: Path | None = typer.Option(None, "--report", help="Write JSON report"),
    summary_csv: Path | None = typer.Option(None, "--summary-csv", help="Write CSV summary"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON report to stdout"),
):
    """Run deterministic LLM parser evaluation cases."""
    from optical_spec_agent.parsers.llm.evaluator import run_llm_evaluation

    try:
        result = run_llm_evaluation(
            cases_path=benchmark_file,
            parser_mode=parser_name,
            llm_provider=llm_provider,
            llm_model=llm_model,
            report_path=report,
            summary_csv_path=summary_csv,
        )
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]LLM eval error:[/red] {exc}")
        raise typer.Exit(1)

    if json_output:
        typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
        if result["failed_cases"]:
            raise typer.Exit(1)
        return

    console.print("[bold]LLM eval[/bold]")
    console.print(f"Parser: {result['parser_mode']}")
    console.print(f"Provider: {result['provider']}")
    console.print(f"Cases: {result['passed_cases']}/{result['total_cases']} passed")
    console.print(f"Field accuracy: {result['field_accuracy']:.3f}")
    if report:
        console.print(f"[dim]Report written to {report}[/dim]")
    if summary_csv:
        console.print(f"[dim]CSV summary written to {summary_csv}[/dim]")
    if result["failed_cases"]:
        raise typer.Exit(1)


# ---- validate ----

@app.command()
def validate(
    path: Path = typer.Argument(..., help="Path to a spec JSON file"),
):
    """Validate an existing spec JSON file."""
    if not path.exists():
        console.print(f"[red]File not found: {path}[/red]")
        raise typer.Exit(1)

    from optical_spec_agent.validators.spec_validator import SpecValidator

    data = json.loads(path.read_text(encoding="utf-8"))
    spec = OpticalSpec.model_validate(data)
    validator = SpecValidator()
    spec = validator.validate(spec)

    console.print(spec_to_summary(spec))


# ---- schema ----

@app.command(name="schema")
def export_schema(
    output: Path = typer.Option(None, "--output", "-o", help="Write schema JSON to file"),
):
    """Export the JSON Schema for the OpticalSpec model."""
    schema_str = OpticalSpec.export_json_schema()
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(schema_str, encoding="utf-8")
        console.print(f"[green]JSON Schema written to {output}[/green]")
    else:
        console.print_json(schema_str)


# ---- example ----

@app.command(name="example")
def run_example(
    name: str = typer.Argument(
        "01",
        help="Example number or keyword (01-05, or 'all')",
    ),
    output_dir: Path = typer.Option(
        Path("outputs"), "--output-dir", "-o", help="Output directory",
    ),
):
    """Run a built-in example."""
    examples = _load_examples()
    if name == "all":
        for key, text in examples.items():
            _run_single_example(key, text, output_dir)
    elif name in examples:
        _run_single_example(name, examples[name], output_dir)
    else:
        console.print(f"[red]Unknown example: {name}[/red]")
        console.print(f"Available: {', '.join(examples.keys())}")
        raise typer.Exit(1)


def _load_examples() -> dict[str, str]:
    return {
        "01": (
            "用FDTD仿真一个gap plasmon体系：80nm金纳米立方体放在金膜上，"
            "间隙填充SiO2（5 nm），用总场散射场(TFSF)光源正入射，"
            "扫间隙厚度从2nm到20nm，步长2nm，计算散射截面和吸收截面。"
            "波长范围400-900nm。"
        ),
        "02": (
            "建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，"
            "放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，"
            "x偏振和y偏振都要做，波长范围500-1200nm。"
        ),
        "03": (
            "Lumerical FDTD仿真硅纳米球的Mie散射，直径150nm，"
            "环境折射率1.5，用TFSF光源，扫波长300-800nm，"
            "计算散射截面、吸收截面和消光截面，提取散射谱主峰位置。"
        ),
        "04": (
            "COMSOL模式分析：Si3N4脊波导（宽800nm，高400nm，蚀刻深度250nm），"
            "SiO2下包层，上包层为空气，计算1.55μm波长下的基模有效折射率和模场分布，"
            "TE和TM模式都要计算。"
        ),
        "05": (
            "对实验测得的散射谱进行Lorentzian拟合，数据范围500-900nm，"
            "主峰位于680nm附近，提取FWHM和T2退相干时间。"
            "用Python scipy做曲线拟合。"
        ),
    }


def _run_single_example(key: str, text: str, output_dir: Path) -> None:
    console.rule(f"[bold cyan]Example {key}")
    console.print(f"[dim]Input:[/dim] {text[:80]}...\n")

    svc = SpecService()
    spec = svc.process(text, task_id=f"ex-{key}")

    console.print(spec_to_summary(spec))

    out_path = output_dir / f"example_{key}_spec.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(spec_to_json(spec), encoding="utf-8")
    console.print(f"\n[dim]  Saved to {out_path}[/dim]\n")


if __name__ == "__main__":
    app()


# ---- meep-generate ----

@app.command("meep-generate")
def meep_generate(
    spec_file: Path = typer.Argument(..., help="Path to spec JSON file"),
    output: Path = typer.Option(None, "-o", "--output", help="Output .py script path"),
    mode: str = typer.Option(
        "preview",
        "--mode",
        help="Meep script mode: preview, research-preview, or smoke",
    ),
):
    """Generate a Meep Python script from a validated spec JSON."""
    if not spec_file.exists():
        console.print(f"[red]File not found: {spec_file}[/red]")
        raise typer.Exit(1)

    from optical_spec_agent.adapters.meep import MeepAdapter, AdapterError

    data = json.loads(spec_file.read_text(encoding="utf-8"))

    # Handle flat-dict format (from to_flat_dict) and raw OpticalSpec format
    if "task" in data and isinstance(data["task"], dict):
        # Check if it's flat-dict format (section fields contain {value, status, note})
        task_fields = data["task"]
        has_status = any(
            isinstance(v, dict) and "status" in v
            for v in task_fields.values()
        )
        if has_status:
            spec = _reconstruct_spec(data)
        else:
            spec = OpticalSpec.model_validate(data)
    else:
        console.print("[red]Invalid spec format: missing 'task' section[/red]")
        raise typer.Exit(1)

    adapter = MeepAdapter()

    if not adapter.can_handle(spec):
        console.print("[red]This spec is not compatible with the Meep adapter.[/red]")
        console.print("[dim]Required: physical_system=nanoparticle_on_film, "
                       "solver_method=fdtd, software_tool=meep[/dim]")
        raise typer.Exit(1)

    readiness = adapter.validate_ready(spec)

    if readiness.errors:
        console.print("[red]Meep adapter readiness check failed.[/red]")
        for error in readiness.errors:
            console.print(f"  - {error}")
        if readiness.defaults_applied:
            console.print("\n[yellow]Defaults the adapter would need:[/yellow]")
            for item in readiness.defaults_applied:
                console.print(f"  - {item}")
        if readiness.warnings:
            console.print("\n[yellow]Warnings:[/yellow]")
            for warning in readiness.warnings:
                console.print(f"  - {warning}")
        raise typer.Exit(1)

    if readiness.defaults_applied:
        console.print("[yellow]Meep adapter defaults in use:[/yellow]")
        for item in readiness.defaults_applied:
            console.print(f"  - {item}")
    if readiness.warnings:
        console.print("[yellow]Meep adapter warnings:[/yellow]")
        for warning in readiness.warnings:
            console.print(f"  - {warning}")

    try:
        result = adapter.generate(spec, script_mode=mode)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
    except AdapterError as e:
        console.print(f"[red]Adapter error: {e}[/red]")
        raise typer.Exit(1)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.content, encoding="utf-8")
        console.print(f"[green]Meep script ({mode}) written to {output}[/green]")
    else:
        console.print(result.content)


# ---- meep execution harness ----

@app.command("meep-check")
def meep_check(
    json_output: bool = typer.Option(False, "--json", help="Print structured JSON output"),
):
    """Check whether Meep is importable in a supported Python environment."""
    from optical_spec_agent.execution import check_meep_available

    result = check_meep_available()
    if json_output:
        console.print_json(json.dumps(result.to_dict(), ensure_ascii=False))
        return

    console.print(f"Meep available: {'yes' if result.available else 'no'}")
    if result.command:
        console.print(f"Command: {' '.join(result.command)}")
    if result.errors:
        console.print("[red]Errors:[/red]")
        for error in result.errors:
            console.print(f"  - {error}")
    if result.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"  - {warning}")


@app.command("meep-run")
def meep_run(
    script_path: Path = typer.Argument(..., help="Path to an existing Meep Python script"),
    workdir: Path | None = typer.Option(
        None,
        "--workdir",
        help="Directory where the script runs and output files are collected",
    ),
    timeout: int = typer.Option(300, "--timeout", help="Execution timeout in seconds"),
    expected_mode: str = typer.Option(
        "auto",
        "--expected-mode",
        help="Expected script mode: auto, smoke, preview, or research-preview",
    ),
    run_id: str | None = typer.Option(None, "--run-id", help="Optional execution run ID"),
    json_output: bool = typer.Option(False, "--json", help="Print structured JSON output"),
    no_save_artifacts: bool = typer.Option(
        False,
        "--no-save-artifacts",
        help="Do not write stdout.txt, stderr.txt, execution_result.json, or run_manifest.json",
    ),
):
    """Run an existing generated Meep script and collect known outputs."""
    from optical_spec_agent.execution import run_meep_script

    result = run_meep_script(
        script_path=script_path,
        workdir=workdir,
        timeout=timeout,
        expected_mode=expected_mode,
        save_artifacts=not no_save_artifacts,
        run_id=run_id,
    )

    if json_output:
        console.print_json(json.dumps(result.to_dict(), ensure_ascii=False))
        if not result.success:
            raise typer.Exit(1)
        return

    _print_execution_result(result)

    if result.postprocess_results is not None:
        console.print("\n[bold]postprocess_results.json[/bold]")
        console.print_json(json.dumps(result.postprocess_results, ensure_ascii=False))

    if not result.success:
        raise typer.Exit(1)


@app.command("adapter-list")
def adapter_list(
    json_output: bool = typer.Option(False, "--json", help="Print adapter metadata as JSON"),
):
    """List registered solver-input adapters."""
    from optical_spec_agent.adapters.registry import list_adapters

    adapters = [metadata.model_dump() for metadata in list_adapters()]
    if json_output:
        typer.echo(json.dumps({"adapters": adapters}, indent=2, ensure_ascii=False))
        return

    console.print("[bold]Registered adapters[/bold]")
    for metadata in adapters:
        console.print(
            f"- [cyan]{metadata['tool_name']}[/cyan] "
            f"({metadata['display_name']}): {metadata['current_status']}, "
            f"*{metadata['output_extension']}"
        )
        console.print(f"  Solver family: {metadata['solver_family']}")
        console.print(
            "  Methods: "
            + (", ".join(metadata["supported_solver_methods"]) or "not specified")
        )
        if metadata["limitations"]:
            console.print(f"  Limitation: {metadata['limitations'][0]}")


@app.command("adapter-generate")
def adapter_generate(
    spec_file: Path = typer.Argument(..., help="Path to a spec JSON file"),
    tool: str = typer.Option(
        "auto",
        "--tool",
        help="Adapter tool: auto, meep, mpb, gmsh, elmer, or optiland",
    ),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file path"),
    mesh: Path | None = typer.Option(None, "--mesh", help="Mesh path for Elmer scaffolds"),
    json_output: bool = typer.Option(False, "--json", help="Print structured JSON output"),
    allow_preview_defaults: bool = typer.Option(
        False,
        "--allow-preview-defaults",
        help="Acknowledge that MVP adapters may apply scaffold defaults",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Fail if adapter readiness reports errors or missing required fields",
    ),
):
    """Generate solver-native input using the generic adapter registry."""
    from optical_spec_agent.adapters.registry import AdapterRegistryError, dispatch_adapter

    try:
        spec = _load_spec_file(spec_file)
        adapter = dispatch_adapter(spec, preferred_tool=tool)
    except (AdapterRegistryError, FileNotFoundError, ValueError) as exc:
        payload = _adapter_error_payload(str(exc), spec_file=spec_file, tool=tool)
        if json_output:
            typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    readiness = _adapter_readiness(adapter, spec, mesh=mesh)
    missing_required = list(getattr(readiness, "missing_required", []) or [])
    readiness_errors = list(getattr(readiness, "errors", []) or [])
    readiness_warnings = list(getattr(readiness, "warnings", []) or [])
    defaults_applied = list(getattr(readiness, "defaults_applied", []) or [])

    if strict and (readiness_errors or missing_required):
        payload = _adapter_report_payload(
            status="error",
            adapter=adapter,
            output=output,
            result=None,
            missing_required=missing_required,
            warnings=readiness_warnings,
            errors=readiness_errors or ["Strict mode blocked generation."],
            defaults_applied=defaults_applied,
            allow_preview_defaults=allow_preview_defaults,
        )
        if json_output:
            typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            _print_adapter_generation_summary(payload)
        raise typer.Exit(1)

    try:
        if adapter.tool_name == "elmer":
            result = adapter.generate(spec, mesh_path=mesh)
        else:
            result = adapter.generate(spec)
    except Exception as exc:
        payload = _adapter_error_payload(str(exc), spec_file=spec_file, tool=adapter.tool_name)
        if json_output:
            typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Adapter error:[/red] {exc}")
        raise typer.Exit(1)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.content, encoding="utf-8")
        result.generated_files["primary"] = str(output)

    status = "warning" if (missing_required or readiness_warnings or result.warnings) else "success"
    payload = _adapter_report_payload(
        status=status,
        adapter=adapter,
        output=output,
        result=result,
        missing_required=missing_required or result.missing_required,
        warnings=[*readiness_warnings, *result.warnings],
        errors=[*readiness_errors, *result.errors],
        defaults_applied=[*defaults_applied, *result.defaults_applied],
        allow_preview_defaults=allow_preview_defaults,
    )

    if not output:
        payload["generated_content"] = result.content

    if json_output:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    _print_adapter_generation_summary(payload)
    if output:
        console.print(f"[green]Generated input written to {output}[/green]")
    else:
        console.print("\n[bold]Generated content[/bold]")
        console.print(result.content)


@app.command("diagnose")
def diagnose(
    spec_file: Path | None = typer.Argument(
        None,
        help="Path to an OpticalSpec JSON file. Defaults to --spec or outputs/my_spec.json.",
    ),
    spec_option: Path | None = typer.Option(
        None,
        "--spec",
        help="Path to an OpticalSpec JSON file.",
    ),
    output_dir: Path = typer.Option(
        Path("outputs"),
        "--output-dir",
        help="Directory for mesh_report.csv, flux_report.csv, execution_diagnostics.json, and diagnostic_preview.png",
    ),
    run_dir: Path | None = typer.Option(
        None,
        "--run-dir",
        help="Optional directory containing Meep execution artifacts from meep-run",
    ),
    create_demo_spec_if_missing: bool = typer.Option(
        False,
        "--create-demo-spec-if-missing",
        help="Create a traceable core Meep demo spec if the spec path is missing.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print structured JSON output"),
):
    """Generate post-hoc physical diagnostics for a spec and optional Meep artifacts."""
    from optical_spec_agent.analysis import (
        generate_physical_diagnostics,
        prepare_diagnostic_spec,
    )

    requested_spec = spec_option or spec_file or Path("outputs/my_spec.json")
    initial_warnings: list[str] = []
    if spec_option is not None and spec_file is not None:
        initial_warnings.append("--spec was provided; it takes precedence over positional SPEC_PATH.")
    try:
        spec_path, created_demo = prepare_diagnostic_spec(
            requested_spec,
            create_demo_spec_if_missing=create_demo_spec_if_missing,
        )
    except FileNotFoundError as exc:
        if json_output:
            typer.echo(json.dumps(_diagnose_error_payload(
                error=str(exc),
                spec_path=requested_spec,
                output_dir=output_dir,
            ), indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    if created_demo:
        initial_warnings.append(f"Created demo spec from core hero task: {spec_path}")

    try:
        result = generate_physical_diagnostics(
            spec_path=spec_path,
            output_dir=output_dir,
            artifact_dir=run_dir,
            initial_warnings=initial_warnings,
        )
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps(_diagnose_error_payload(
                error=f"Could not generate diagnostics: {exc}",
                spec_path=spec_path,
                output_dir=output_dir,
            ), indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Error:[/red] Could not generate diagnostics: {exc}")
        raise typer.Exit(1)

    if json_output:
        typer.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        if result.status == "error":
            raise typer.Exit(1)
        return

    _print_diagnostics_result(result)
    if result.status == "error":
        raise typer.Exit(1)


# ---- workflow orchestration ----

@app.command("workflow-plan")
def workflow_plan(
    text: str = typer.Argument(..., help="Natural language task description"),
    parser_name: str = typer.Option("rule", "--parser", help="Parser mode: rule, llm, or hybrid"),
    llm_provider: str = typer.Option("mock", "--llm-provider", help="LLM provider: mock or disabled"),
    tool: str = typer.Option("auto", "--tool", help="Adapter tool: auto, meep, mpb, gmsh, elmer, optiland"),
    output: Path | None = typer.Option(None, "--output", help="Write workflow_plan.json"),
    json_output: bool = typer.Option(False, "--json", help="Print plan as JSON"),
):
    """Plan a synchronous local workflow without generating solver input."""
    from optical_spec_agent.workflows import plan_workflow

    try:
        text, request_options = _resolve_text_request(text)
        parser_name = request_options.get("parser", parser_name)
        llm_provider = request_options.get("llm_provider", llm_provider)
        tool = request_options.get("tool", tool)
        plan = plan_workflow(
            text,
            parser=parser_name,
            llm_provider=llm_provider,
            tool=tool,
            output=output,
        )
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Workflow plan error:[/red] {exc}")
        raise typer.Exit(1)

    payload = plan.model_dump(mode="json")
    if json_output:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    console.print("[bold]Workflow plan[/bold]")
    console.print(f"Parser: {plan.parser_mode}")
    console.print(f"Selected tool: {plan.selected_tool}")
    console.print("Planned steps: " + ", ".join(plan.planned_steps))
    console.print("Expected artifacts:")
    for item in plan.expected_artifacts:
        console.print(f"  - {item}")
    if output:
        console.print(f"[dim]Plan written to {output}[/dim]")
    if plan.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in plan.warnings:
            console.print(f"  - {warning}")


@app.command("workflow-run")
def workflow_run(
    text: str = typer.Argument(..., help="Natural language task description"),
    parser_name: str = typer.Option("rule", "--parser", help="Parser mode: rule, llm, or hybrid"),
    llm_provider: str = typer.Option("mock", "--llm-provider", help="LLM provider: mock or disabled"),
    tool: str = typer.Option("auto", "--tool", help="Adapter tool: auto, meep, mpb, gmsh, elmer, optiland"),
    output_dir: Path = typer.Option(Path("outputs/workflows/demo"), "--output-dir", help="Workflow output directory"),
    no_execute: bool = typer.Option(False, "--no-execute", help="Do not execute solvers; this is the default"),
    execute_meep: bool = typer.Option(False, "--execute-meep", help="Allow optional local Meep execution"),
    strict: bool = typer.Option(False, "--strict", help="Stop on step errors"),
    strict_execution: bool = typer.Option(False, "--strict-execution", help="Treat Meep execution failure as an error"),
    continue_on_warning: bool = typer.Option(True, "--continue-on-warning/--fail-on-warning", help="Continue when a step warns"),
    run_diagnostics: bool = typer.Option(True, "--run-diagnostics/--no-diagnostics", help="Run post-hoc diagnostics when applicable"),
    run_eval: bool = typer.Option(False, "--run-eval", help="Run lightweight workflow evaluation"),
    json_output: bool = typer.Option(False, "--json", help="Print workflow_run.json as JSON"),
):
    """Run a synchronous local workflow and write workflow_run.json."""
    from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig

    allow_execute = bool(execute_meep and not no_execute)
    config = WorkflowRunnerConfig(
        parser=parser_name,
        llm_provider=llm_provider,
        tool=tool,
        output_dir=output_dir,
        allow_execute=allow_execute,
        strict=strict,
        strict_execution=strict_execution,
        continue_on_warning=continue_on_warning,
        run_diagnostics=run_diagnostics,
        run_eval=run_eval,
    )
    try:
        result = WorkflowRunner(config).run(text)
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Workflow run error:[/red] {exc}")
        raise typer.Exit(1)

    payload = result.model_dump(mode="json")
    if json_output:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        if result.status == "error":
            raise typer.Exit(1)
        return

    _print_workflow_run_summary(payload)
    if result.status == "error":
        raise typer.Exit(1)


@app.command("workflow-replay")
def workflow_replay(
    workflow_run_json: Path = typer.Argument(..., help="Path to workflow_run.json"),
    output_dir: Path = typer.Option(Path("outputs/workflows/replay"), "--output-dir", help="Replay output directory"),
    json_output: bool = typer.Option(False, "--json", help="Print replay report JSON"),
):
    """Replay a workflow_run.json with deterministic local settings."""
    from optical_spec_agent.workflows import replay_workflow

    try:
        report = replay_workflow(workflow_run_json, output_dir=output_dir)
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Workflow replay error:[/red] {exc}")
        raise typer.Exit(1)

    payload = report.model_dump(mode="json")
    if json_output:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    console.print("[bold]Workflow replay[/bold]")
    console.print(f"Original run: {report.original_run_id}")
    console.print(f"Replay run: {report.replay_run_id}")
    console.print(f"Deterministic match: {'yes' if report.deterministic_match else 'no'}")
    console.print(f"[dim]Replay report written under {output_dir / 'replay' / 'replay_report.json'}[/dim]")


@app.command("workflow-report")
def workflow_report(
    workflow_run_json: Path = typer.Argument(..., help="Path to workflow_run.json"),
    report_format: str = typer.Option("markdown", "--format", help="Report format: markdown or json"),
    output: Path | None = typer.Option(None, "--output", help="Write report to file"),
    json_output: bool = typer.Option(False, "--json", help="Print report payload as JSON"),
):
    """Render a workflow_run.json as Markdown or JSON."""
    from optical_spec_agent.workflows import load_workflow_run, render_workflow_report, write_workflow_report

    try:
        workflow = load_workflow_run(workflow_run_json)
        rendered = render_workflow_report(workflow, fmt=report_format)
        if output:
            write_workflow_report(workflow_run_json, output=output, fmt=report_format)
    except Exception as exc:
        if json_output:
            typer.echo(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, ensure_ascii=False))
        else:
            console.print(f"[red]Workflow report error:[/red] {exc}")
        raise typer.Exit(1)

    if json_output:
        typer.echo(json.dumps(rendered, indent=2, ensure_ascii=False) if isinstance(rendered, dict) else json.dumps({"report": rendered}, indent=2, ensure_ascii=False))
        return
    if output:
        console.print(f"[green]Workflow report written to {output}[/green]")
    else:
        console.print_json(json.dumps(rendered, ensure_ascii=False)) if isinstance(rendered, dict) else console.print(rendered)


def _print_workflow_run_summary(payload: dict) -> None:
    status_style = {"success": "green", "warning": "yellow", "error": "red"}.get(
        payload["status"],
        "white",
    )
    console.print(f"[{status_style}]Status: {payload['status']}[/{status_style}]")
    console.print(f"Run ID: {payload['run_id']}")
    console.print(f"Parser: {payload['parser_mode']}")
    console.print(f"Selected tool: {payload['selected_tool']}")
    console.print(f"Output dir: {payload['output_dir']}")
    console.print("[green]Artifacts:[/green]")
    for name, artifact in payload.get("artifacts", {}).items():
        console.print(f"  - {name}: {artifact['path']}")
    if payload.get("warnings"):
        console.print("[yellow]Warnings:[/yellow]")
        for warning in payload["warnings"]:
            console.print(f"  - {warning}")
    if payload.get("errors"):
        console.print("[red]Errors:[/red]")
        for error in payload["errors"]:
            console.print(f"  - {error}")


def _diagnose_error_payload(*, error: str, spec_path: Path, output_dir: Path) -> dict:
    from optical_spec_agent.analysis import DIAGNOSTICS_SCHEMA_VERSION

    return {
        "schema_version": DIAGNOSTICS_SCHEMA_VERSION,
        "status": "error",
        "spec_path": str(spec_path),
        "output_dir": str(output_dir),
        "run_dir": None,
        "generated_at": "",
        "generated_outputs": {},
        "warnings": [],
        "errors": [error],
        "missing_artifacts": [],
        "nan_detected": False,
        "inf_detected": False,
        "timeout_detected": False,
        "notes": ["Diagnostics did not run."],
    }


def _load_spec_file(path: Path) -> OpticalSpec:
    """Load raw OpticalSpec JSON or flat to_flat_dict JSON from disk."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if "task" not in data or not isinstance(data["task"], dict):
        raise ValueError("Invalid spec format: missing 'task' section")

    task_fields = data["task"]
    has_status = any(
        isinstance(value, dict) and "status" in value
        for value in task_fields.values()
    )
    if has_status:
        return _reconstruct_spec(data)
    return OpticalSpec.model_validate(data)


def _resolve_text_request(value: str) -> tuple[str, dict]:
    """Resolve a CLI text argument or a local request fixture file.

    JSON fixture files may provide `text` plus optional parser settings. Plain
    text files are read as the prompt body. Non-path arguments keep the original
    CLI behavior.
    """
    path = Path(value)
    if not path.exists():
        return value, {}

    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() != ".json":
        text = raw.strip()
        if not text:
            raise ValueError(f"Input file is empty: {path}")
        return text, {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON request file {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"JSON request file must contain an object: {path}")

    text = data.get("text") or data.get("request") or data.get("description")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"JSON request file must contain a non-empty text field: {path}")

    options = {
        key: data[key]
        for key in ("parser", "llm_provider", "llm_model", "tool")
        if isinstance(data.get(key), str) and data[key]
    }
    return text.strip(), options


def _adapter_readiness(adapter, spec: OpticalSpec, *, mesh: Path | None):
    """Call adapter validate_ready with optional mesh when supported."""
    try:
        return adapter.validate_ready(spec, mesh_path=mesh)
    except TypeError:
        return adapter.validate_ready(spec)


def _adapter_error_payload(error: str, *, spec_file: Path, tool: str) -> dict:
    return {
        "status": "error",
        "selected_adapter": tool,
        "spec_file": str(spec_file),
        "output_path": None,
        "language": None,
        "missing_required": [],
        "warnings": [],
        "errors": [error],
        "defaults_applied": [],
        "limitations": [],
    }


def _adapter_report_payload(
    *,
    status: str,
    adapter,
    output: Path | None,
    result,
    missing_required: list[str],
    warnings: list[str],
    errors: list[str],
    defaults_applied: list[str],
    allow_preview_defaults: bool,
) -> dict:
    metadata = adapter.metadata().model_dump()
    return {
        "status": status,
        "selected_adapter": adapter.tool_name,
        "display_name": metadata["display_name"],
        "output_path": str(output) if output else None,
        "language": metadata["output_language"],
        "output_extension": metadata["output_extension"],
        "missing_required": missing_required,
        "warnings": list(dict.fromkeys(warnings)),
        "errors": errors,
        "defaults_applied": list(dict.fromkeys(defaults_applied)),
        "limitations": metadata["limitations"],
        "allow_preview_defaults": allow_preview_defaults,
        "generated_files": result.generated_files if result else {},
    }


def _print_adapter_generation_summary(payload: dict) -> None:
    status_style = {
        "success": "green",
        "warning": "yellow",
        "error": "red",
    }.get(payload["status"], "white")
    console.print(f"[{status_style}]Status: {payload['status']}[/{status_style}]")
    console.print(f"Selected adapter: {payload['selected_adapter']}")
    console.print(f"Language: {payload['language']}")
    if payload.get("output_path"):
        console.print(f"Output path: {payload['output_path']}")
    if payload["missing_required"]:
        console.print("[yellow]Missing required:[/yellow]")
        for item in payload["missing_required"]:
            console.print(f"  - {item}")
    if payload["defaults_applied"]:
        console.print("[yellow]Defaults / placeholders:[/yellow]")
        for item in payload["defaults_applied"]:
            console.print(f"  - {item}")
    if payload["warnings"]:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in payload["warnings"]:
            console.print(f"  - {warning}")
    if payload["errors"]:
        console.print("[red]Errors:[/red]")
        for error in payload["errors"]:
            console.print(f"  - {error}")
    if payload["limitations"]:
        console.print("[dim]Limitations:[/dim]")
        for limitation in payload["limitations"]:
            console.print(f"  - {limitation}")


def _print_diagnostics_result(result) -> None:
    status_style = {
        "success": "green",
        "warning": "yellow",
        "error": "red",
    }.get(result.status, "white")
    console.print(f"[{status_style}]Status: {result.status}[/{status_style}]")
    console.print(f"Schema version: {result.schema_version}")
    console.print(f"Generated at: {result.generated_at}")
    console.print(f"Spec: {result.spec_path}")
    console.print(f"Output dir: {result.output_dir}")
    if result.run_dir:
        console.print(f"Run dir: {result.run_dir}")
    console.print("[green]Generated artifacts:[/green]")
    for name, path in result.generated_outputs.items():
        console.print(f"  - {name}: {path}")
    if result.missing_artifacts:
        console.print("[yellow]Missing run artifacts:[/yellow]")
        for item in result.missing_artifacts:
            console.print(f"  - {item}")
    if result.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"  - {warning}")
    if result.errors:
        console.print("[red]Errors:[/red]")
        for error in result.errors:
            console.print(f"  - {error}")


def _print_execution_result(result) -> None:
    console.print(f"Success: {'yes' if result.success else 'no'}")
    console.print(f"Meep available: {'yes' if result.available else 'no'}")
    console.print(f"Schema version: {result.schema_version}")
    console.print(f"Run ID: {result.run_id}")
    console.print(f"Created at: {result.created_at}")
    console.print(f"Expected mode: {result.expected_mode}")
    console.print(f"Workdir: {result.workdir}")
    if result.command:
        console.print(f"Command: {' '.join(result.command)}")
    if result.returncode is not None:
        console.print(f"Return code: {result.returncode}")
    if result.outputs:
        console.print("[green]Outputs:[/green]")
        for name, path in result.outputs.items():
            console.print(f"  - {name}: {path}")
    if result.missing_outputs:
        console.print("[red]Missing outputs:[/red]")
        for name in result.missing_outputs:
            console.print(f"  - {name}")
    artifact_paths = [
        Path(result.workdir) / "execution_result.json",
        Path(result.workdir) / "run_manifest.json",
    ]
    existing_artifacts = [path for path in artifact_paths if path.exists()]
    if existing_artifacts:
        console.print("[green]Execution artifacts:[/green]")
        for path in existing_artifacts:
            console.print(f"  - {path.name}: {path}")
    if result.errors:
        console.print("[red]Errors:[/red]")
        for error in result.errors:
            console.print(f"  - {error}")
    if result.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"  - {warning}")


def _reconstruct_spec(flat: dict) -> OpticalSpec:
    """Reconstruct an OpticalSpec from a flat-dict (to_flat_dict output).

    The flat-dict format has sections with {value, status, note} StatusField entries.
    Structured sub-models (SourceSetting, ParticleInfo, etc.) are serialized as dicts
    and need to be deserialized back to their Pydantic types.
    """
    from optical_spec_agent.models.base import (
        StatusField,
        BoundaryConditionSetting,
        GeometryDefinition,
        MaterialSystem,
        MeshSetting,
        MonitorSetting,
        ParticleInfo,
        SourceSetting,
        StabilitySetting,
        SubstrateOrFilmInfo,
        SweepPlan,
        SymmetrySetting,
    )

    # Map field dotted paths to their Pydantic model classes
    _STRUCTURED_FIELDS = {
        "geometry_material.geometry_definition": GeometryDefinition,
        "geometry_material.material_system": MaterialSystem,
        "geometry_material.substrate_or_film_info": SubstrateOrFilmInfo,
        "geometry_material.particle_info": ParticleInfo,
        "simulation.sweep_plan": SweepPlan,
        "simulation.source_setting": SourceSetting,
        "simulation.boundary_condition": BoundaryConditionSetting,
        "simulation.symmetry_setting": SymmetrySetting,
        "simulation.mesh_setting": MeshSetting,
        "simulation.stability_setting": StabilitySetting,
        "simulation.monitor_setting": MonitorSetting,
    }

    spec = OpticalSpec()

    section_fields = {
        "task": ["task_name", "task_type", "research_goal"],
        "physics": ["physical_system", "physical_mechanism", "model_dimension", "structure_type"],
        "geometry_material": [
            "geometry_definition", "material_system", "material_model",
            "substrate_or_film_info", "particle_info", "gap_medium", "key_parameters",
        ],
        "simulation": [
            "solver_method", "software_tool", "sweep_plan", "excitation_source",
            "source_setting", "polarization", "incident_direction",
            "boundary_condition", "symmetry_setting", "mesh_setting",
            "stability_setting", "monitor_setting",
        ],
        "output": ["output_observables", "postprocess_target"],
    }

    for section_name, field_names in section_fields.items():
        section_data = flat.get(section_name, {})
        section = getattr(spec, section_name)
        for fname in field_names:
            entry = section_data.get(fname)
            if entry is None:
                continue

            if isinstance(entry, dict) and "status" in entry:
                raw_val = entry["value"]

                # Deserialize structured sub-models from dicts
                dotted = f"{section_name}.{fname}"
                model_cls = _STRUCTURED_FIELDS.get(dotted)
                if model_cls and isinstance(raw_val, dict):
                    try:
                        raw_val = model_cls.model_validate(raw_val)
                    except Exception:
                        pass  # keep as dict if validation fails

                sf = StatusField(
                    value=raw_val,
                    status=entry["status"],
                    note=entry.get("note", ""),
                )
            else:
                # Plain field (e.g. task_id)
                sf = entry
            setattr(section, fname, sf)

    return spec
