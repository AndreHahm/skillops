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

health-no-write:
    uv run skillops health --no-write

list:
    uv run skillops list

inspect skill:
    uv run skillops inspect {{skill}}

docs-test:
    uv run pytest tests/test_docs_structure.py tests/test_llm_wiki.py

agent-test:
    uv run pytest tests/test_agent_setup.py tests/test_hooks.py tests/test_mcp_examples.py

cli-test:
    uv run pytest tests/test_cli_validate.py tests/test_cli_health.py tests/test_cli_list.py tests/test_cli_inspect.py

ci:
    uv run ruff check .
    uv run pytest
    uv run skillops validate
    uv run skillops health
