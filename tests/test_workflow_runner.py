"""Workflow runner integration tests without external solvers."""

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig


def _run(tmp_path, text, tool):
    config = WorkflowRunnerConfig(
        parser="hybrid",
        llm_provider="mock",
        tool=tool,
        output_dir=tmp_path,
        allow_execute=False,
        strict=False,
        run_diagnostics=True,
    )
    return WorkflowRunner(config).run(text)


def test_full_mpb_workflow_writes_source_of_truth(tmp_path):
    workflow = _run(
        tmp_path,
        "用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。",
        "mpb",
    )
    assert workflow.status in {"success", "warning"}
    assert (tmp_path / "workflow_run.json").exists()
    assert (tmp_path / "artifacts/generated_input.py").exists()
    assert (tmp_path / "human_review_checklist.md").exists()


def test_meep_no_execute_workflow_generates_diagnostics(tmp_path):
    workflow = _run(
        tmp_path,
        "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，输出散射谱。",
        "meep",
    )
    assert workflow.status in {"success", "warning"}
    assert (tmp_path / "artifacts/execution_diagnostics.json").exists()
    assert (tmp_path / "artifacts/mesh_report.csv").exists()


def test_gmsh_workflow_generates_geo(tmp_path):
    workflow = _run(
        tmp_path,
        "用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格。",
        "gmsh",
    )
    assert workflow.status in {"success", "warning"}
    assert (tmp_path / "artifacts/generated_input.geo").exists()


def test_elmer_missing_mesh_records_warning(tmp_path):
    workflow = _run(tmp_path, "用 Elmer 做 Si3N4 波导 FEM 模式分析。", "elmer")
    assert workflow.status in {"success", "warning"}
    assert any("mesh" in warning.lower() for warning in workflow.warnings)
    assert (tmp_path / "artifacts/generated_input.sif").exists()


def test_optiland_workflow_records_scaffold_limitations(tmp_path):
    workflow = _run(
        tmp_path,
        "用 Optiland 设计一个简单单透镜成像系统，计算 spot diagram 和 MTF。",
        "optiland",
    )
    assert workflow.status in {"success", "warning"}
    assert (tmp_path / "artifacts/generated_input.py").exists()
    assert any("scaffold" in item.lower() for item in workflow.limitations)


def test_strict_mode_stops_after_error(tmp_path):
    config = WorkflowRunnerConfig(
        parser="hybrid",
        llm_provider="disabled",
        tool="mpb",
        output_dir=tmp_path,
        strict=True,
    )
    workflow = WorkflowRunner(config).run("用 MPB 计算 band diagram。")
    assert workflow.status == "error"
    assert not (tmp_path / "artifacts/generated_input.py").exists()
