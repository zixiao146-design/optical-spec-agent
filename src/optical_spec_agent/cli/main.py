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
