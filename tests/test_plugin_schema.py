import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA_PATH = ROOT / "schemas" / "plugin.schema.json"
PLUGIN_REGISTRY_PATH = ROOT / "registry" / "plugins.yaml"


def load_plugin_schema() -> dict[str, Any]:
    return json.loads(PLUGIN_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_plugin_registry(data: dict[str, Any]) -> None:
    Draft202012Validator(load_plugin_schema()).validate(data)


def valid_plugin_registry_with_item() -> dict[str, Any]:
    return {
        "version": 1,
        "plugins": [
            {
                "id": "example-plugin",
                "name": "Example Plugin",
                "version": "0.1.0",
                "status": "draft",
                "description": "Example plugin entry for schema validation.",
                "publisher": {
                    "name": "platform",
                    "contact": "platform@example.com",
                },
                "source": {
                    "type": "internal",
                    "repository": None,
                    "license": "MIT",
                },
                "contents": {
                    "skills": [],
                    "mcp_servers": [],
                    "hooks": [],
                    "commands": [],
                },
                "compatibility": {
                    "agents": ["claude-code", "codex"],
                    "environments": ["ubuntu-24.04", "windows-11-wsl2"],
                },
                "governance": {
                    "risk_tier": "low",
                    "trust_tier": "internal",
                    "review_status": "not-reviewed",
                },
            }
        ],
    }


def test_plugin_registry_file_is_valid_yaml_and_matches_schema() -> None:
    registry_data = yaml.safe_load(PLUGIN_REGISTRY_PATH.read_text(encoding="utf-8"))

    assert registry_data == {"version": 1, "plugins": []}
    validate_plugin_registry(registry_data)


def test_empty_plugins_array_is_valid() -> None:
    validate_plugin_registry({"version": 1, "plugins": []})


def test_valid_plugin_item_is_valid() -> None:
    validate_plugin_registry(valid_plugin_registry_with_item())


def test_plugin_item_missing_required_publisher_is_invalid() -> None:
    registry_data = valid_plugin_registry_with_item()
    del registry_data["plugins"][0]["publisher"]

    with pytest.raises(ValidationError, match="publisher"):
        validate_plugin_registry(registry_data)


def test_plugins_array_defines_typed_items_schema() -> None:
    schema = load_plugin_schema()
    plugins_schema = schema["properties"]["plugins"]
    item_schema = plugins_schema.get("items")

    assert plugins_schema["type"] == "array"
    assert item_schema is not None
    assert item_schema["type"] == "object"
    assert "properties" in item_schema
    assert set(item_schema["required"]) == {
        "id",
        "name",
        "version",
        "status",
        "description",
        "publisher",
        "source",
        "contents",
        "compatibility",
        "governance",
    }


def test_plugins_array_is_not_generic_untyped_array() -> None:
    schema = load_plugin_schema()
    item_schema = schema["properties"]["plugins"].get("items")

    assert item_schema != {}
    assert item_schema is not True
    assert item_schema["additionalProperties"] is False

    registry_data = deepcopy(valid_plugin_registry_with_item())
    registry_data["plugins"].append("not-a-plugin-object")

    with pytest.raises(ValidationError, match="not of type 'object'"):
        validate_plugin_registry(registry_data)
