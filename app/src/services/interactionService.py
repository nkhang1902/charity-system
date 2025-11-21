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
        """
        user_interactions: list of dicts {target_id, weight}
        target_embeddings: dict {target_id: np.array([...])}
        """
        user_interactions = self.interactionRepo.getByUserId(user_id, target_type)
        print("user_interactions", user_interactions)
        vectors = []
        weights = []
        for inter in user_interactions:
            print("inter", inter)
            tid = f"{inter["target_type"]}_{inter["target_id"]}"
            w = inter["weight"]
            if tid in target_embeddings:
                vectors.append(target_embeddings[tid] * w)
                weights.append(w)
        if not vectors:
            return None  # user has no interactions with known targets
        return np.sum(vectors, axis=0) / np.sum(weights)

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