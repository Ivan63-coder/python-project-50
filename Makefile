.PHONY: install lint test coverage

install:
	uv sync
	pip install flake8 flake8-pyproject pytest pytest-cov

lint:
	flake8 tests

test:
	pytest tests/

test-coverage:
	pytest --cov=gendiff --cov-report=xml tests/

.PHONY: check
check: lint test
