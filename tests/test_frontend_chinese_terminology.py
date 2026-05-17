from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_chinese_terminology_doc_preserves_contract_names():
    path = ROOT / "docs" / "frontend_chinese_terminology.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "spec",
        "规格",
        "parse",
        "本地解析",
        "validate",
        "验证规格",
        "adapter",
        "适配器",
        "adapter matrix",
        "适配器矩阵",
        "workflow plan",
        "工作流计划",
        "artifact preview",
        "适配器产物预览",
        "validation evidence",
        "验证证据",
        "readiness",
        "readiness / 就绪状态",
        "external solver",
        "外部求解器",
        "external LLM",
        "外部 LLM",
        "production-grade physical validation",
        "生产级物理验证",
        "formal convergence proof",
        "形式化收敛证明",
        "material library",
        "材料库",
        "example gallery",
        "示例库",
        "agent trace timeline",
        "多智能体协作轨迹",
        "sub-agent collaboration",
        "子智能体协作",
        "API 字段名保持英文",
        "API JSON keys 保持英文稳定",
        "Adapter tool names are not translated",
        "`meep`, `gmsh`, `mpb`, `elmer`, `optiland` 不翻译",
        "材料 ID",
        "SpecAgent",
        "MaterialAgent",
    ]
    for phrase in required:
        assert phrase in text
