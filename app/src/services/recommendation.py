import os
import numpy as np
import joblib

class RecommendationService:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(__file__),
            "..", "resource", "lightfm_model.pkl"
        )

        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print(f" Loaded resource from {model_path}")
            except Exception as e:
                print(f" Failed to load resource: {e}")
                self.model = None
        else:
            print(" No pretrained resource found, using random scorer.")
            self.model = None

    def getRecommendedCampaigns(self, user_id: int, campaigns: list[dict]):
        if not campaigns:
            return []

        campaign_ids = [c["id"] for c in campaigns]

        if self.model is not None:
            try:
                scores = np.random.rand(len(campaign_ids))  # fake tạm
            except Exception:
                scores = np.random.rand(len(campaign_ids))
        else:
            scores = np.random.rand(len(campaign_ids))

        ranked = sorted(
            [{**c, "score": float(s)} for c, s in zip(campaigns, scores)],
            key=lambda x: x["score"],
            reverse=True
        )
        return ranked
