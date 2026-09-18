.PHONY: install test run demo-insecure demo-secure

install:
	python -m pip install -e ".[dev]"

test:
	pytest -q

run:
	uvicorn aegistwin.main:app --reload

demo-insecure:
	python scripts/security_gate.py --variant insecure --output insecure-report.md

demo-secure:
	python scripts/security_gate.py --variant secure --output secure-report.md

