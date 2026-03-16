# ==============================================================================
# OdooAI — Makefile
# ==============================================================================
# Standard commands for every developer. Run `make help` to see all options.
# ==============================================================================

.PHONY: help install lint typecheck test test-coverage security-scan run clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---- Setup ----

install: ## Install all dependencies
	pip install -e ".[dev]"

# ---- Quality ----

lint: ## Run linter (ruff)
	ruff check odooai/ tests/
	ruff format --check odooai/ tests/

lint-fix: ## Auto-fix lint issues
	ruff check --fix odooai/ tests/
	ruff format odooai/ tests/

typecheck: ## Run type checker (mypy)
	mypy odooai/ --strict

# ---- Testing ----

test: ## Run all tests
	pytest tests/ -v

test-coverage: ## Run tests with coverage report
	pytest tests/ -v --cov=odooai --cov-report=html --cov-report=term

# ---- Security ----

security-scan: ## Run security scanner (bandit)
	bandit -r odooai/ -ll

# ---- Run ----

run: ## Run the application (development)
	uvicorn odooai.main:app --reload --port 8000

# ---- All Checks (run before PR) ----

check: lint typecheck test security-scan ## Run ALL checks (lint + types + tests + security)
	@echo "✅ All checks passed"

# ---- Clean ----

clean: ## Remove build artifacts and cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete 2>/dev/null || true
	@echo "🧹 Cleaned"
