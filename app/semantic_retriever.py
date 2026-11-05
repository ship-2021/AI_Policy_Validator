from sklearn.metrics.pairwise import cosine_similarity

from app.embeddings import EmbeddingService
from app.policy_loader import load_policies


class SemanticPolicyRetriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.policies = load_policies()

        self.policy_texts = [
            policy["description"]
            for policy in self.policies
        ]

        self.policy_embeddings = (
            self.embedding_service.generate_embeddings(
                self.policy_texts
            )
        )

    def search(
            self,
            query: str,
            top_k: int = 2
    ):

        query_embedding = (
            self.embedding_service.generate_embeddings(
                [query]
            )
        )

        similarities = cosine_similarity(
            query_embedding,
            self.policy_embeddings
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            policy = self.policies[index].copy()

            policy["similarity"] = float(
                similarities[index]
            )

            results.append(policy)

        return results