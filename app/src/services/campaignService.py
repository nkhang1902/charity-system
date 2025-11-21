from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.services.interactionService import InteractionService
from app.src.constants.userInteraction import TargetType
from app.src.jobs.writeEmbedding import write_embedding
from app.src.jobs.writeEmbedding import get_all_embedding_from_dynamodb

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository, interactionService: InteractionService):
        self.campaignRepo = campaignRepository
        self.interactionService = interactionService

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        return self.campaignRepo.getList(params)

    def create(self, payload: dict):
        data = self.campaignRepo.create(payload)
        write_embedding({
            "entityType": "campaign",
            "id": str(data.id),
            "isDeleted": False,
            "data":  {"title": data.title, "description": data.description}
        })
        return data

    def update(self, id: str, payload: dict):
        data = self.campaignRepo.update(id, payload)
        write_embedding({
            "entityType": TargetType.CAMPAIGN,
            "id": str(id),
            "isDeleted": False,
            "data":  {"title": data.title, "description": data.description}
        })
        return data

    def delete(self, id: str):
        data = self.campaignRepo.delete(id)
        write_embedding({
            "entityType": TargetType.CAMPAIGN,
            "id": str(id),
            "isDeleted": True,
            "data":  {"title": data.title, "description": data.description}
        })
        return data

    def getRecommendedCampaigns(self, user_id, k, params: CampaignQueryParams | None = None) -> list[Campaign]:
        target_embeddings = get_all_embedding_from_dynamodb(TargetType.CAMPAIGN)
        user_embedding = self.interactionService.compute_user_embedding(int(user_id), TargetType.CAMPAIGN, target_embeddings)
        print("user_embedding", user_embedding)
        if user_embedding != None:
            target_emb_dict = {item["target_id"]: item["embedding"] for item in target_embeddings}
            recommendations = self.interactionService.get_top_k_recommendations(user_embedding, target_emb_dict, int(k))
            ids = [r["target_id"].split("_")[1] for r in recommendations]
            print("recommendations", ids)
            return self.campaignRepo.getList(params, ids)
        else:
            return self.campaignRepo.getList(params)