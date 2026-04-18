# Optics Extraction Workflow — Design Document

> Status: Design phase — no implementation yet.

This document defines a "web search → optical structure extraction" data workflow
for collecting natural-language optical task descriptions from the web and converting
them into structured JSON that feeds `optical-spec-agent`'s benchmark and training
pipeline.

---

## 1. Search MCP Integration

### 1.1 Current available tools

The Claude Code session already has these search MCP tools:

| Tool | Type | Capability |
|------|------|------------|
| `WebSearch` | Built-in | General web search, returns titles + URLs |
| `mcp__web-search-prime__web_search_prime` | MCP | Web search with summary, domain filter, recency |
| `mcp__web-reader__webReader` / `mcp__web_reader__webReader` | MCP | Fetch URL → markdown/text, with image/links summary |

These are **sufficient for the extraction workflow** today. No additional MCP is
required to start.

### 1.2 Brave Search MCP (optional upgrade)

Brave Search offers better API rate limits and privacy. Setup for macOS:

```bash
# 1. Get API key from https://brave.com/search/api/ (free tier: 2000 queries/month)
# 2. Add to Claude Code:
claude mcp add-json brave-search '{
  "command": "npx",
  "args": ["-y", "brave-search-mcp-server"],
  "env": {"BRAVE_API_KEY": "YOUR_KEY_HERE"}
}'
```

Verification after adding:

```
# In Claude Code session, ask:
"Use the brave_search tool to search for 'FDTD nanoparticle on film simulation'"
```

### 1.3 Minimal test search task

Use the already-available tools to verify the pipeline:

```
Step 1 — Search:
  mcp__web-search-prime__web_search_prime("FDTD simulation gold nanoparticle gap plasmon scattering spectrum")

Step 2 — Read top result:
  mcp__web-reader__webReader(url="<top result URL>")

Step 3 — Extract structured fields from the page content
```

---

## 2. Extraction Schema

### 2.1 Target output format

Each extracted record should conform to this schema:

```json
{
  "query": "original search query string",
  "source_url": "https://...",
  "source_title": "page title",
  "extraction_timestamp": "2026-04-18T12:00:00Z",
  "task_text": "the natural-language optical task description extracted from the page",
  "spec": {
    "physical_system": "nanoparticle_on_film | single_particle | waveguide | grating | metasurface | ...",
    "structure_type": "sphere_on_film | cross_structure | waveguide | gratings | array | ...",
    "materials": ["Au", "SiO2", "Ag", ...],
    "physical_mechanism": "gap_plasmon | plasmon | scattering | waveguide | resonance | ...",
    "solver_hints": ["fdtd", "fem", "rcwa", ...],
    "output_observables": ["scattering_spectrum", "field_distribution", "FWHM", ...],
    "postprocess_target": ["lorentzian_fit", "fwhm_extraction", "T2_extraction", ...]
  },
  "evidence_span": "the exact sentence(s) from the source that justify the extraction",
  "confidence": "high | medium | low",
  "notes": "free-text notes about extraction quality"
}
```

### 2.2 Field definitions

| Field | Required | Description |
|-------|----------|-------------|
| `query` | yes | The search query that found this page |
| `source_url` | yes | Canonical URL |
| `source_title` | yes | Page title |
| `extraction_timestamp` | yes | ISO 8601 |
| `task_text` | yes | 1-5 sentences describing an optical simulation/analysis task |
| `spec.physical_system` | no | Maps to `PhysicalSystem` enum |
| `spec.structure_type` | no | Maps to `StructureType` enum |
| `spec.materials` | no | List of material names |
| `spec.physical_mechanism` | no | Maps to `PhysicalMechanism` enum |
| `spec.solver_hints` | no | Solver methods mentioned (fdtd, fem, etc.) |
| `spec.output_observables` | no | List of output types |
| `spec.postprocess_target` | no | List of post-processing targets |
| `evidence_span` | yes | Exact text from source justifying the extraction |
| `confidence` | yes | `high` = all spec fields populated with clear evidence; `medium` = some fields inferred; `low` = ambiguous or partial |
| `notes` | no | Extraction quality notes |

### 2.3 Confidence levels

- **high**: task_text is a complete simulation/analysis description; ≥4 spec fields populated with direct evidence
- **medium**: task_text is partial or mixed with non-simulation content; 2-3 spec fields populated
- **low**: only tangentially related to optical simulation; <2 spec fields; kept for coverage but not for benchmark

### 2.4 Alignment with optical-spec-agent

The `spec` sub-object deliberately mirrors the stable fields defined in
`docs/schema_stability.md`. A future converter can transform an extracted record
into an `OpticalSpec` JSON by mapping:

```
spec.physical_system  → physics.physical_system (StatusField)
spec.structure_type   → physics.structure_type
spec.materials        → geometry_material.material_system
spec.physical_mechanism → physics.physical_mechanism
spec.solver_hints     → simulation.solver_method
spec.output_observables → output.output_observables
spec.postprocess_target → output.postprocess_target
```

Fields not present in the extraction (e.g., sweep_plan, boundary_condition) will
remain `missing` — this is expected since web pages rarely specify full simulation
configurations.

---

## 3. Search Query Templates

### 3.1 Template structure

Each template is parameterized. `{lang}` can be `cn` or `en`.

### 3.2 Templates by physical system

#### nanoparticle_on_film / gap plasmon

```
# CN
"{material}纳米{shape}-{film_material}膜 gap plasmon FDTD {observable}"
"间隙等离激元 {shape} 颗粒 薄膜 散射谱 {solver}"
"gap plasmon 仿真 {material}纳米颗粒 金膜 共振波长 FWHM"
"{shape} on film simulation scattering spectrum gap plasmon"

# EN
"gap plasmon {material} {shape} on {film_material} film FDTD scattering"
"nanoparticle on mirror simulation gap plasmon resonance wavelength FWHM"
"{material} nanosphere on {film_material} film gap dependent scattering FDTD"
```

Parameters: `{material}` ∈ {Au, Ag, Al}, `{shape}` ∈ {sphere, cube, rod, cross},
`{film_material}` ∈ {Au, Ag, Al}, `{observable}` ∈ {散射谱, 吸收谱, 场增强, 远场},
`{solver}` ∈ {Meep, Lumerical, CST}

#### waveguide / mode analysis

```
# CN
"脊波导 模式分析 {material} 有效折射率 {solver}"
"光波导 FEM 模场分布 {wavelength} 偏振"
"硅光波导 COMSOL 模式计算 TE TM 有效折射率"

# EN
"ridge waveguide mode analysis {material} effective index {solver}"
"photonic waveguide FEM mode profile {wavelength} polarization"
"silicon waveguide COMSOL mode analysis effective index"
```

Parameters: `{material}` ∈ {Si, Si3N4, SiO2}, `{solver}` ∈ {COMSOL, Meep, Lumerical},
`{wavelength}` ∈ {1.55μm, 1550nm, 1.31μm}

#### grating

```
# CN
"亚波长光栅 {solver} 透射谱 反射谱 {material} 周期"
"衍射光栅 RCWA 波长范围 偏振 透射率"

# EN
"subwavelength grating {solver} transmission reflection {material} period"
"diffraction grating RCWA spectral response polarization"
```

#### metasurface

```
# CN
"介质超表面 {material}柱 透射谱 共振 偏振 {solver}"
"超表面单元结构 RCWA 反射谱 相位调控"

# EN
"dielectric metasurface {material} pillar transmission resonance {solver}"
"metasurface unit cell RCWA reflection phase control polarization"
```

#### FDTD / FEM general

```
# CN
"FDTD仿真 {observable} {material}纳米颗粒 波长范围"
"有限元 {solver} {physical_system} 场分布 模式分析"
"Meep FDTD 散射截面 吸收截面 {shape} {material}"

# EN
"FDTD simulation {observable} {material} nanoparticle wavelength range"
"FEM {solver} {physical_system} field distribution mode analysis"
"Meep FDTD cross section absorption {shape} {material}"
```

#### FWHM / T2 / Lorentzian

```
# CN
"Lorentzian拟合 散射谱 FWHM T2 退相干时间 {material}"
"共振线宽 半高全宽 拟合 Q因子 品质因子 {shape}"

# EN
"Lorentzian fitting scattering spectrum FWHM dephasing time {material}"
"resonance linewidth FWHM Q factor fitting {shape}"
```

#### scattering / field / mode

```
# CN
"散射谱计算 {physical_system} {solver} 偏振 波长扫描"
"场分布 近场 远场 {shape} 共振 {material}"
"模式分析 有效折射率 群速度 波导 {material}"

# EN
"scattering spectrum {physical_system} {solver} polarization wavelength sweep"
"field distribution near field far field {shape} resonance {material}"
"mode analysis effective index group velocity waveguide {material}"
```

### 3.3 Query expansion strategy

For each template, generate concrete queries by substituting parameters:

```python
materials = ["Au", "Ag", "Si", "Si3N4", "TiO2"]
shapes = ["sphere", "cube", "rod", "cross"]
solvers = ["FDTD", "FEM", "RCWA", "Meep", "COMSOL", "Lumerical"]
observables = ["scattering spectrum", "absorption spectrum", "field distribution",
               "transmission", "reflection", "FWHM"]
```

Expected yield: ~50-80 unique queries covering the full physical_system × solver ×
observable space.

---

## 4. Future Minimal MCP Server Design

### 4.1 Server name

`optics-extractor-mcp` — a lightweight MCP server that combines search + extraction.

### 4.2 Tools to expose

#### Tool 1: `search_optics_tasks`

Search the web for optical simulation task descriptions.

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query (supports both CN and EN)"
    },
    "max_results": {
      "type": "integer",
      "default": 5,
      "description": "Maximum number of results to return"
    },
    "language": {
      "type": "string",
      "enum": ["cn", "en", "any"],
      "default": "any"
    }
  },
  "required": ["query"]
}
```

**Output schema:**
```json
{
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "url": {"type": "string"},
          "title": {"type": "string"},
          "snippet": {"type": "string"}
        }
      }
    },
    "total_found": {"type": "integer"}
  }
}
```

#### Tool 2: `extract_optics_spec`

Read a URL and extract structured optical spec fields from the page content.

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "url": {
      "type": "string",
      "description": "URL of the page to extract from"
    },
    "context_query": {
      "type": "string",
      "description": "The original search query that led to this URL (for context)"
    }
  },
  "required": ["url"]
}
```

**Output schema:**
```json
{
  "type": "object",
  "properties": {
    "task_text": {"type": "string"},
    "spec": {
      "type": "object",
      "properties": {
        "physical_system": {"type": ["string", "null"]},
        "structure_type": {"type": ["string", "null"]},
        "materials": {"type": "array", "items": {"type": "string"}},
        "physical_mechanism": {"type": ["string", "null"]},
        "solver_hints": {"type": "array", "items": {"type": "string"}},
        "output_observables": {"type": "array", "items": {"type": "string"}},
        "postprocess_target": {"type": "array", "items": {"type": "string"}}
      }
    },
    "evidence_span": {"type": "string"},
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    "notes": {"type": "string"}
  }
}
```

#### Tool 3: `batch_search_and_extract`

End-to-end: search → read → extract → return structured records.

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "query_template": {
      "type": "string",
      "description": "Search query template (may contain {param} placeholders)"
    },
    "params": {
      "type": "array",
      "items": {
        "type": "object",
        "description": "Parameter substitutions for the template"
      },
      "description": "List of param dicts to expand the template"
    },
    "max_results_per_query": {
      "type": "integer",
      "default": 3
    },
    "min_confidence": {
      "type": "string",
      "enum": ["high", "medium", "low"],
      "default": "medium"
    }
  },
  "required": ["query_template"]
}
```

**Output schema:**
```json
{
  "type": "object",
  "properties": {
    "records": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/extraction_record"
      }
    },
    "stats": {
      "type": "object",
      "properties": {
        "queries_run": {"type": "integer"},
        "pages_read": {"type": "integer"},
        "records_extracted": {"type": "integer"},
        "by_confidence": {
          "type": "object",
          "properties": {
            "high": {"type": "integer"},
            "medium": {"type": "integer"},
            "low": {"type": "integer"}
          }
        }
      }
    }
  }
}
```

### 4.3 Integration with optical-spec-agent

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  optics-extractor   │     │  extraction records   │     │  optical-spec-agent │
│  MCP server         │────▶│  (JSONL file)         │────▶│  benchmark pipeline │
│                     │     │                       │     │  / training data    │
│  Tools:             │     │  Schema:              │     │                     │
│  - search_optics    │     │  - task_text          │     │  Uses:              │
│  - extract_spec     │     │  - spec.*             │     │  - golden_cases.json│
│  - batch_extract    │     │  - evidence_span      │     │  - parser training  │
│                     │     │  - confidence         │     │  - validation rules │
└─────────────────────┘     └──────────────────────┘     └─────────────────────┘

Data flow:
1. batch_search_and_extract → produces extraction_record JSONL
2. Filter by confidence >= medium
3. Convert spec.* fields to OpticalSpec via field mapping
4. Run through RuleBasedParser for comparison
5. High-quality extractions become new golden_cases
```

### 4.4 Implementation notes

- The MCP server can be implemented in Python using the `mcp` SDK
- Search can delegate to existing MCP tools (web-search-prime) or Brave Search API directly
- Extraction logic should use the same keyword tables as `RuleBasedParser` for field mapping
- The `batch_search_and_extract` tool adds rate limiting (1-2 sec between requests)
- Output is JSONL (one JSON object per line) for easy incremental collection
