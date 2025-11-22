from app.src.constants.campaignStatus import CampaignStatus
from app.src.repositories.campaignRepository import CampaignRepository
from app.src.models.campaign import Campaign, CampaignQueryParams
from app.src.services.interactionService import InteractionService
from app.src.constants.userInteraction import TargetType
from app.src.jobs.writeEmbedding import write_embedding
from app.src.jobs.writeEmbedding import get_all_embedding_from_dynamodb
from app.src.services.coreClientSerivce import CoreClientSerivce
from datetime import datetime

class CampaignService:
    def __init__(self, campaignRepository: CampaignRepository, interactionService: InteractionService):
        self.campaignRepo = campaignRepository
        self.interactionService = interactionService
        self.coreClientService = CoreClientSerivce()

    def getById(self, id: str) -> Campaign | None:
        return self.campaignRepo.getById(id)

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        return self.campaignRepo.getList(params)

    def create(self, payload: dict):
        # step 1: create new campaign with status draft
        payload["status"] = CampaignStatus.NEW
        data = self.campaignRepo.create(payload)

        # step 2: request core update status in_progress
        data = self.processCoreCamapignCreation(data)

        write_embedding({
            "entityType": "campaign",
            "id": str(data.id),
            "isDeleted": False,
            "data":  {"title": data.title, "description": data.description}
        })
        return data

    def processCoreCamapignCreation(self, tx: Campaign):
        try:
            result = self.coreClientService.handleCamapignCreation(tx)

            if result.get("success"):
                tx.status = CampaignStatus.IN_PROGRESS
                print(f"[CORE] Campaign created successfully for tx {tx.id}")
            else:
                tx.status = TransactionStatus.CANCELLED
                print(f"[CORE] Payment FAILED for tx {tx.id}: {tx.message}")

        except Exception as e:
            tx.status = TransactionStatus.CANCELLED
            print(f"[CORE] Exception during core payment: {e}")

        self.campaignRepo.update(id=tx.id, payload=tx.toDict())
        return tx

    def update(self, id: str, payload: dict):
        if payload.get("status") == CampaignStatus.CLOSED:
            cp = self.campaignRepo.getById(id)
            today = datetime.now().date()
            if cp.end_date is None or cp.end_date > today:
                payload["status"] = CampaignStatus.CANCELLED
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

    def getRecommendedCampaigns(self, user_id, k, offset, params: CampaignQueryParams | None = None) -> list[Campaign]:
        target_embeddings = get_all_embedding_from_dynamodb(TargetType.CAMPAIGN)
        user_embedding = self.interactionService.compute_user_embedding(int(user_id), TargetType.CAMPAIGN, target_embeddings)
        print("user_embedding", user_embedding)
        if user_embedding != None:
            target_emb_dict = {item["target_id"]: item["embedding"] for item in target_embeddings}
            recommendations = self.interactionService.get_top_k_recommendations(user_embedding, target_emb_dict, int(k), int(offset))
            ids = [r["target_id"].split("_")[1] for r in recommendations]
            print("recommendations", ids)
            return self.campaignRepo.getList(params, ids)
        else:
            return self.campaignRepo.getList(params)