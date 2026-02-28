.PHONY: install lint test coverage

install:
	uv sync
	pip install pyyaml>=6.0
	pip install flake8 flake8-pyproject pytest pytest-cov


lint:
	flake8 tests

test:
	pytest tests/ -v

test-coverage:
	pytest --cov=gendiff --cov-report=xml --cov-report=term-missing tests/

test-nested:
	pytest tests/test_nested.py -v

.PHONY: check
check: lint test
