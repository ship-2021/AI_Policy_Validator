from app.models import ValidationRequest, ValidationResult


def validate_database_public_access(
        request: ValidationRequest
) -> ValidationResult:

    public_access = request.attributes.get("public_access", False)

    if public_access:
        return ValidationResult(
            policy_id="DB-001",
            status="FAIL",
            reason="Production databases must not be publicly accessible."
        )

    return ValidationResult(
        policy_id="DB-001",
        status="PASS",
        reason="Database is not publicly accessible."
    )