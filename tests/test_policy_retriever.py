from app.policy_retriever import get_policies_for_resource


def test_database_policies_are_retrieved():

    policies = get_policies_for_resource("database")

    assert len(policies) == 3
    assert policies[0]["id"] == "DB-001"


def test_unknown_resource_returns_no_policies():

    policies = get_policies_for_resource("unknown")

    assert policies == []