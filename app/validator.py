from app.models import ValidationRequest, ValidationResult
from app.rules import validate_database_public_access


def validate(request: ValidationRequest) -> ValidationResult:

    if request.resource_type == "database":
        return validate_database_public_access(request)

    return ValidationResult(
        policy_id="UNKNOWN",
        status="REVIEW",
        reason="No validation rule exists for this resource type."
    )