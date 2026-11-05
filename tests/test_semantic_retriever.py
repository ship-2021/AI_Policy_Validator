from app.semantic_retriever import SemanticPolicyRetriever


def test_semantic_search_finds_public_access_policy():

    retriever = SemanticPolicyRetriever()

    results = retriever.search(
        "Can a production database be exposed to the internet?"
    )

    assert len(results) > 0
    assert results[0]["id"] == "DB-001"