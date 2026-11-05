from app.policy_loader import load_policies


def find_policy(resource_type: str, policies: list[dict]) -> list[dict]:

    return [
        policy
        for policy in policies
        if policy.get("resource_type") == resource_type
    ]


def get_policies_for_resource(resource_type: str) -> list[dict]:

    policies = load_policies()

    return find_policy(resource_type, policies)