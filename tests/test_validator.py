from app.models import ValidationRequest
from app.validator import validate


def test_public_database_fails():

    request = ValidationRequest(
        resource_type="database",
        resource_name="customer-db",
        attributes={
            "public_access": True
        }
    )

    result = validate(request)

    assert result.status == "FAIL"
    assert result.policy_id == "DB-001"


def test_private_database_passes():

    request = ValidationRequest(
        resource_type="database",
        resource_name="customer-db",
        attributes={
            "public_access": False
        }
    )

    result = validate(request)

    assert result.status == "PASS"