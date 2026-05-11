.PHONY: install dev test check bench-key bench-semantic llm-check diagnostics test-cov lint example api schema clean tree

PYTHON ?= python
PIP ?= pip

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e ".[dev]"

test:
	pytest -v

check:
	pytest
	$(PYTHON) benchmarks/run_benchmark.py --mode key_fields
	$(PYTHON) benchmarks/run_semantic_benchmark.py

bench-key:
	$(PYTHON) benchmarks/run_benchmark.py --mode key_fields

bench-semantic:
	$(PYTHON) benchmarks/run_semantic_benchmark.py

llm-check:
	$(PYTHON) benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json

diagnostics:
	$(PYTHON) scripts/generate_physical_diagnostics.py --create-demo-spec-if-missing

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
