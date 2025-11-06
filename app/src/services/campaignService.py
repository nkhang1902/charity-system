from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign
from app.src.models.campaign import CampaignQueryParams

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository):
        self.campaignRepo = campaignRepository

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