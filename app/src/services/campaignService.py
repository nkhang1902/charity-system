from src.repositories.campaignRepository import CampaignRepository
from src.models.campaign import Campaign

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository):
        self.campaignRepo = campaignRepository

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self) -> list[Campaign]:
        return self.campaignRepo.getList()

    def create(self, payload: dict):
        return self.campaignRepo.create(payload)

    def update(self, id: str, payload: dict):
        return self.campaignRepo.update(id, payload)

    def delete(self, id: str):
        return self.campaignRepo.delete(id)