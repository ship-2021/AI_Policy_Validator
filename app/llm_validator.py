import json
import os

from openai import OpenAI


class LLMPolicyValidator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)

    def validate(
            self,
            resource: dict,
            policies: list[dict],
    ) -> dict:

        policy_context = "\n\n".join(
            [
                f"""
Policy ID: {policy["id"]}
Policy Name: {policy["name"]}
Description: {policy["description"]}
Severity: {policy["severity"]}
"""
                for policy in policies
            ]
        )

        prompt = f"""
You are a security policy validation assistant.

Evaluate the resource against the provided policies.

Resource:
{json.dumps(resource, indent=2)}

Policies:
{policy_context}

For each relevant policy, determine whether the resource:
- PASS: satisfies the policy
- FAIL: violates the policy
- REVIEW: insufficient information to make a reliable decision

Return ONLY valid JSON in this format:

{{
  "results": [
    {{
      "policy_id": "string",
      "status": "PASS | FAIL | REVIEW",
      "confidence": 0.0,
      "reason": "string"
    }}
  ]
}}

Do not invent facts that are not present in the resource or policy.
If there is insufficient information, use REVIEW.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise security policy validation "
                        "assistant. Follow the supplied policy context "
                        "and never invent missing information."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        return json.loads(content)