from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationRequest:
    resource_type: str
    resource_name: str
    attributes: dict[str, Any]


@dataclass
class ValidationResult:
    policy_id: str
    status: str
    reason: str