.PHONY: install lint test coverage

install:
	uv sync

lint:
	flake8 src tests

test:
	pytest tests/

test-coverage:
	pytest --cov=gendiff --cov-report=xml tests/

.PHONY: check
check: lint test
