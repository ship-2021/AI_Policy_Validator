import yaml


def load_policies(file_path: str = "policies/policies.yaml"):
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data.get("policies", [])