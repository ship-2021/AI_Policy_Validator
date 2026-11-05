from app.llm_validator import LLMPolicyValidator
from app.semantic_retriever import SemanticPolicyRetriever
from app.validator import validate
from app.models import ValidationRequest


class PolicyValidationService:

    def __init__(self):
        self.retriever = SemanticPolicyRetriever()

    def validate_resource(
            self,
            request: ValidationRequest,
    ) -> dict:

        # Step 1: Run deterministic validation
        deterministic_result = validate(request)

        # If we have a known deterministic rule,
        # trust that result.
        if deterministic_result.policy_id != "UNKNOWN":
            return {
                "source": "deterministic_rule",
                "policy_id": deterministic_result.policy_id,
                "status": deterministic_result.status,
                "reason": deterministic_result.reason,
            }

        # Step 2: Retrieve relevant policies
        query = (
            f"{request.resource_type} "
            f"{request.resource_name} "
            f"{request.attributes}"
        )

        policies = self.retriever.search(
            query=query,
            top_k=2,
        )

        # Step 3: If no relevant policies were found,
        # request human review.
        if not policies:
            return {
                "source": "policy_retrieval",
                "status": "REVIEW",
                "reason": "No relevant policy was found.",
            }

        # Step 4: Use LLM for interpretation
        validator = LLMPolicyValidator()

        resource = {
            "resource_type": request.resource_type,
            "resource_name": request.resource_name,
            "attributes": request.attributes,
        }

        llm_result = validator.validate(
            resource=resource,
            policies=policies,
        )

        return {
            "source": "rag_llm",
            "results": llm_result["results"],
        }