.PHONY: install dev test benchmark semantic-check check bench-key bench-semantic llm-check workflow-check diagnostics docs-check cli-check release-check artifact-check build twine-check smoke quality testpypi-preflight test-cov lint example api schema clean tree

PYTHON ?= python
PIP ?= pip

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	pytest -q

benchmark:
	$(PYTHON) benchmarks/run_benchmark.py --mode key_fields

semantic-check:
	$(PYTHON) benchmarks/run_semantic_benchmark.py
	$(PYTHON) benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json

check:
	$(MAKE) test
	$(MAKE) benchmark
	$(MAKE) semantic-check
	$(MAKE) llm-check
	$(MAKE) workflow-check
	$(MAKE) docs-check
	$(MAKE) cli-check
	$(MAKE) artifact-check

bench-key:
	$(PYTHON) benchmarks/run_benchmark.py --mode key_fields

bench-semantic:
	$(PYTHON) benchmarks/run_semantic_benchmark.py

llm-check:
	$(PYTHON) benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json

workflow-check:
	$(PYTHON) benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json

diagnostics:
	$(PYTHON) scripts/generate_physical_diagnostics.py --create-demo-spec-if-missing

docs-check:
	$(PYTHON) scripts/check_docs_consistency.py

cli-check:
	$(PYTHON) scripts/check_cli_surface.py

release-check:
	$(PYTHON) scripts/check_release_readiness.py --report outputs/release_readiness_report.json

artifact-check:
	$(PYTHON) scripts/check_artifact_contracts.py --report outputs/artifact_contract_report.json

build:
	$(PYTHON) -m build

twine-check:
	twine check dist/*

smoke:
	optical-spec --help
	optical-spec parse "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，输出散射谱和 FWHM。" --output outputs/smoke_spec.json
	optical-spec validate outputs/smoke_spec.json
	optical-spec schema --output outputs/schema.json
	optical-spec meep-generate outputs/smoke_spec.json --mode preview --output outputs/smoke_meep.py
	optical-spec meep-check --json
	optical-spec diagnose outputs/smoke_spec.json --output-dir outputs --create-demo-spec-if-missing --json

quality:
	./scripts/run_quality_gates.sh

testpypi-preflight:
	./scripts/testpypi_preflight.sh

test-cov:
	pytest --cov=optical_spec_agent --cov-report=term-missing

lint:
	ruff check src/ tests/

example:
	optical-spec example all -o outputs

example-01:
	optical-spec example 01 -o outputs

schema:
	optical-spec schema -o optical_spec_schema.json

api:
	uvicorn optical_spec_agent.api.app:app --reload --port 8000

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

tree:
	@find . -not -path './.git/*' -not -path './__pycache__/*' -not -path './.pytest_cache/*' -not -path './src/*.egg-info/*' -not -path '*/node_modules/*' -not -name '*.pyc' | sort | head -80
