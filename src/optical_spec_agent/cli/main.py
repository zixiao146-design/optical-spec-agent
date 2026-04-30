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
):
    """Parse natural language into a validated spec."""
    svc = SpecService()
    spec = svc.process(text, task_id=task_id)

    if show_json:
        console.print_json(spec_to_json(spec))
    else:
        console.print(spec_to_summary(spec))

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(spec_to_json(spec), encoding="utf-8")
        console.print(f"\n[dim]JSON written to {output}[/dim]")


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
def meep_check():
    """Check whether Meep is importable in a supported Python environment."""
    from optical_spec_agent.execution import check_meep_available

    result = check_meep_available()
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
):
    """Run an existing generated Meep script and collect known outputs."""
    from optical_spec_agent.execution import run_meep_script

    result = run_meep_script(script_path=script_path, workdir=workdir, timeout=timeout)
    _print_execution_result(result)

    if result.postprocess_results is not None:
        console.print("\n[bold]postprocess_results.json[/bold]")
        console.print_json(json.dumps(result.postprocess_results, ensure_ascii=False))

    if not result.success:
        raise typer.Exit(1)


def _print_execution_result(result) -> None:
    console.print(f"Success: {'yes' if result.success else 'no'}")
    console.print(f"Meep available: {'yes' if result.available else 'no'}")
    console.print(f"Workdir: {result.workdir}")
    if result.command:
        console.print(f"Command: {' '.join(result.command)}")
    if result.returncode is not None:
        console.print(f"Return code: {result.returncode}")
    if result.outputs:
        console.print("[green]Outputs:[/green]")
        for name, path in result.outputs.items():
            console.print(f"  - {name}: {path}")
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
        MaterialEntry,
        MaterialSystem,
        MeshSetting,
        MonitorSetting,
        ParticleInfo,
        PostprocessTargetSpec,
        SourceSetting,
        StabilitySetting,
        SubstrateOrFilmInfo,
        SweepPlan,
        SymmetrySetting,
        confirmed,
        inferred,
        missing,
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
