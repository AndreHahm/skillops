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

ci:
    uv run ruff check .
    uv run pytest
    uv run skillops validate
    uv run skillops health
