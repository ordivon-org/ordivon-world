from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
import json
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT202012

_CONTRACT_NAMES = (
    "browser-manifest",
    "browser-request",
    "edge-capabilities",
    "edge-receipt",
    "fetch-request",
    "network-observation",
    "world-observation",
    "world-prepared-dispatch",
)


class ContractError(ValueError):
    pass


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict[str, Any]:
    if name not in _CONTRACT_NAMES:
        raise ContractError(f"unknown contract schema: {name}")
    resource = files("ordivon_world").joinpath(
        "contracts",
        f"{name}.schema.json",
    )
    value = json.loads(resource.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"contract schema is not an object: {name}")
    Draft202012Validator.check_schema(value)
    return value


@lru_cache(maxsize=1)
def contract_registry() -> Registry[dict[str, Any]]:
    pairs: list[tuple[str, dict[str, Any]]] = []
    for name in _CONTRACT_NAMES:
        schema = load_schema(name)
        identifier = schema.get("$id")
        if not isinstance(identifier, str) or not identifier:
            raise ContractError(f"contract schema has no absolute $id: {name}")
        pairs.append((identifier, schema))
    return Registry().with_contents(
        pairs,
        default_specification=DRAFT202012,
    )


def validate_contract(name: str, value: Any) -> None:
    validator = Draft202012Validator(
        load_schema(name),
        registry=contract_registry(),
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(value),
        key=lambda item: list(item.absolute_path),
    )
    if not errors:
        return
    error = errors[0]
    path = ".".join(str(item) for item in error.absolute_path) or "$"
    raise ContractError(f"{name} contract failed at {path}: {error.message}")
