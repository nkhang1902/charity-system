from app.src.repositories.interactionRepository import InteractionRepository
from app.src.models.userInteraction import UserInteraction
import numpy as np

class InteractionService:
    def __init__(self, interactionRepository: InteractionRepository):
        self.interactionRepo = interactionRepository

    def getByUserId(self, user_id: int, target_type: str):
        return self.interactionRepo.getByUserId(user_id, target_type)

    def create(self, payload: dict):
        return self.interactionRepo.create(payload)

    def compute_user_embedding(self, user_id, target_type, target_embeddings):
        # Normalize list -> dict { "campaign_2": [...], ... }
        emb_dict = {
            item["target_id"]: item["embedding"]
            for item in target_embeddings
        }

        user_interactions = self.interactionRepo.getByUserId(user_id, target_type)

        vectors = []
        weights = []

        for inter in user_interactions:
            tid = f"{inter['target_type']}_{inter['target_id']}"  # e.g. campaign_2
            w = inter["weight"]

            if tid in emb_dict:
                vec = emb_dict[tid]
                vectors.append([v * w for v in vec])
                weights.append(w)

        if not vectors:
            return None

        # Compute weighted average WITHOUT numpy
        dimension = len(vectors[0])
        weighted_sum = [0] * dimension

        for vec in vectors:
            for i in range(dimension):
                weighted_sum[i] += vec[i]

        total_weight = sum(weights)

        return [x / total_weight for x in weighted_sum]


    def get_top_k_recommendations(user_embedding, target_embeddings, top_k=5):
        """
        target_embeddings: dict {target_id: np.array([...])}
        Returns list of top-k recommended target_ids with similarity score.
        """
        scores = []
        for tid, vec in target_embeddings.items():
            sim = 1 - cosine_similarity(user_embedding, vec)
            scores.append((tid, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [{"target_id": tid, "score": score} for tid, score in scores[:top_k]]


import math

def cosine_similarity(vec1, vec2):
    dot = sum(a*b for a,b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a*a for a in vec1))
    norm2 = math.sqrt(sum(b*b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)