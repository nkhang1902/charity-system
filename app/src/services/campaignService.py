from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.utils.publishEvent import publish_entity_event_for_embedding
from app.src.constants.userInteraction import TargetType

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository):
        self.campaignRepo = campaignRepository

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        return self.campaignRepo.getList(params)

    def create(self, payload: dict):
        data = self.campaignRepo.create(payload)
        print(publish_entity_event_for_embedding(TargetType.CAMPAIGN, data.id, {"title": data.title, "description": data.description}))
        return data

    def update(self, id: str, payload: dict):
        data = self.campaignRepo.update(id, payload)
        publish_entity_event_for_embedding(TargetType.CAMPAIGN, data.id, {"title": data.title, "description": data.description})
        return data

    def delete(self, id: str):
        publish_entity_event_for_embedding(TargetType.CAMPAIGN, id, is_deleted=True)
        return self.campaignRepo.delete(id)

    def getRecommendedCampaigns(self, user_id: str, params: CampaignQueryParams):
        campaigns = self.getList(params)
        campaign_dicts = [item.viewDict() for item in campaigns]
        return campaigns
