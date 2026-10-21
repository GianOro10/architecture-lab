.PHONY: install test lint audit terraform docker

install:
	cd app && python -m pip install -e '.[dev]'

test:
	cd app && pytest

lint:
	cd app && ruff check src tests

audit:
	cd app && pip-audit

terraform:
	cd infra/terraform && terraform fmt -check -recursive && terraform init -backend=false && terraform validate

docker:
	docker build -f app/Dockerfile app
