from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.constants.userInteraction import TargetType
from app.src.jobs.writeEmbedding import write_embedding

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository):
        self.campaignRepo = campaignRepository

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        return self.campaignRepo.getList(params)

    def create(self, payload: dict):
        data = self.campaignRepo.create(payload)
        write_embedding({
            "entityType": "campaign",
            "id": str(id),
            "isDeleted": False,
            "data":  {"title": data.title, "description": data.description}
        }, None)
        return data

    def update(self, id: str, payload: dict):
        data = self.campaignRepo.update(id, payload)
        write_embedding({
            "entityType": "campaign",
            "id": str(id),
            "isDeleted": False,
            "data":  {"title": data.title, "description": data.description}
        }, None)
        return data

    def delete(self, id: str):
        data = self.campaignRepo.delete(id)
        write_embedding({
            "entityType": "campaign",
            "id": str(id),
            "isDeleted": True,
            "data":  {"title": data.title, "description": data.description}
        })
        return data

    def getRecommendedCampaigns(self, user_id: str, params: CampaignQueryParams):
        campaigns = self.getList(params)
        campaign_dicts = [item.viewDict() for item in campaigns]
        return campaigns
