import os
import requests
import numpy as np

class RecommendationService:
    def __init__(self):
        self.model_service_url = os.getenv("MODEL_SERVICE_URL", "http://lightfm:8000")

    def getRecommendedCampaigns(self, user_id: int, campaigns: list[dict]):
        if not campaigns:
            return []

        campaign_ids = [c["id"] for c in campaigns]

        try:
            response = requests.post(
                f"{self.model_service_url}/recommend",
                json={"user_id": user_id, "item_ids": campaign_ids},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                rec_ids = data.get("recommendations", [])
                ranked = [c for id_ in rec_ids for c in campaigns if c["id"] == id_]
                return ranked
            else:
                print(f"Model service returned {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error calling model service: {e}")

        scores = np.random.rand(len(campaigns))
        ranked = sorted(
            [{**c, "score": float(s)} for c, s in zip(campaigns, scores)],
            key=lambda x: x["score"],
            reverse=True
        )
        return ranked
