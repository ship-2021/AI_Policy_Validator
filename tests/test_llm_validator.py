from unittest.mock import MagicMock

from app.llm_validator import LLMPolicyValidator


def test_llm_validator_returns_structured_result(monkeypatch):

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key"
    )

    validator = LLMPolicyValidator()

    mock_response = MagicMock()

    mock_response.choices[0].message.content = """
    {
        "results": [
            {
                "policy_id": "DB-001",
                "status": "FAIL",
                "confidence": 0.99,
                "reason": "The database is publicly accessible."
            }
        ]
    }
    """

    validator.client.chat.completions.create = MagicMock(
        return_value=mock_response
    )

    result = validator.validate(
        resource={
            "resource_type": "database",
            "resource_name": "customer-db",
            "attributes": {
                "public_access": True
            }
        },
        policies=[
            {
                "id": "DB-001",
                "name": "Production Database Public Access",
                "description": (
                    "Production databases must not be "
                    "publicly accessible."
                ),
                "severity": "critical",
            }
        ],
    )

    assert result["results"][0]["policy_id"] == "DB-001"
    assert result["results"][0]["status"] == "FAIL"