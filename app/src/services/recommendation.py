import os
import numpy as np
import joblib
from lightfm import LightFM


class RecommendationService:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(__file__),
            "..", "model", "lightfm_model.pkl"
        )

        if os.path.exists(model_path):
            self.model: LightFM = joblib.load(model_path)
            print(f"Loaded LightFM model from {model_path}")
        else:
            print("No pretrained model found. Using empty model for demo.")
            self.model = LightFM(no_components=30, loss="warp")

    def getRecommendedCampaigns(self, user_id: int, campaigns: list[dict]):
        if not campaigns:
            return []

        campaign_ids = [c["id"] for c in campaigns]

        try:
            scores = self.model.predict(user_id, np.arange(len(campaign_ids)))
        except Exception:
            scores = np.random.rand(len(campaign_ids))

        ranked = sorted(
            [{**c, "score": float(s)} for c, s in zip(campaigns, scores)],
            key=lambda x: x["score"],
            reverse=True
        )
        return ranked
