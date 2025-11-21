from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.services.interactionService import InteractionService
from app.src.constants.userInteraction import TargetType
from app.src.jobs.writeEmbedding import write_embedding

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
        user_embedding = self.interactionService.compute_user_embedding(int(user_id), TargetType.CAMPAIGN)
        recommendations = self.interactionService.get_top_k_recommendations(user_embedding, k)
        ids = [r["target_id"] for r in recommendations]
        return self.campaignRepo.getList(params, ids)
