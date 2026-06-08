install:
    uv sync --all-packages --dev

lint:
    uv run ruff check .

test:
    uv run pytest

validate:
    uv run skillops validate

health:
    uv run skillops health

list:
    uv run skillops list

inspect skill:
    uv run skillops inspect {{skill}}

cli-test:
    uv run pytest tests/test_cli_validate.py tests/test_cli_health.py tests/test_cli_list.py tests/test_cli_inspect.py

ci:
    uv run ruff check .
    uv run pytest
    uv run skillops validate
    uv run skillops health
