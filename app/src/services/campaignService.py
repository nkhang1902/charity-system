from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.services.recommendation import RecommendationService


class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository):
        self.campaignRepo = campaignRepository
        self.recommendation = RecommendationService()

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        return self.campaignRepo.getList(params)

    def create(self, payload: dict):
        return self.campaignRepo.create(payload)

    def update(self, id: str, payload: dict):
        return self.campaignRepo.update(id, payload)

    def delete(self, id: str):
        return self.campaignRepo.delete(id)

    def getRecommendedCampaigns(self, user_id: str, params: CampaignQueryParams):
        campaigns = self.getList(params)
        campaign_dicts = [item.viewDict() for item in campaigns]
        return self.recommendation.getRecommendedCampaigns(user_id, campaign_dicts)
