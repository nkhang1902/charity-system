from app.src.repositories.transactionRepository import TransactionRepository
from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams
from app.src.models.commitTransaction import CommitTransaction
from app.src.services.coreClientSerivce import CoreClientSerivce
from app.src.services.smartContractService import SmartContractService
from app.src.services.campaignService import CampaignService
from datetime import datetime
from app.src.constants.transactionStatus import TransactionStatus
from dotenv import load_dotenv
import os
from app.src.constants.campaignStatus import CampaignStatus

class TransactionService:
    def __init__(self, transactionRepository: TransactionRepository, campaignService: CampaignService):
        load_dotenv()

        self.explorer_tx_prefix: str = os.getenv("EXPLORER_TX_PREFIX")
        self.campaignService = campaignService
        self.transactionRepo = transactionRepository
        self.coreClientService = CoreClientSerivce()
        self.smartContractService = SmartContractService()

    def getById(self, id: str) -> Transaction | None:
        return self.transactionRepo.getById(id)

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        return self.transactionRepo.getList(params)

    def createTransaction(self, payload: dict) -> Transaction:
        # Step 0: Validate Campaign
        campaign = self.campaignService.getById(payload.get("campaign_id"))
        if campaign is None or campaign.status != CampaignStatus.IN_PROGRESS:
            raise ValueError("Campaign is not in progress")

        # Step 1: Create in DB
        tx = self.createNewTransaction(payload)
        tx.campaign = campaign

        # Step 2: Process Core
        tx = self.processCorePayment(tx)

        # If core failed → stop
        if tx.status != TransactionStatus.SUCCESS:
            return tx

        # Step 3: Commit blockchain
        tx = self.commitOnChain(tx)

        # Step 4: Commit campaign
        campaign.current_amount = campaign.current_amount + tx.amount
        self.campaignService.update(campaign.id, campaign.toDict())

        return tx

    def createNewTransaction(self, payload: dict) -> Transaction:
        tx_data = {
            "user_id": payload.get("user_id"),
            "campaign_id": payload["campaign_id"],
            "amount": payload["amount"],
            "status": TransactionStatus.NEW,
            "message": payload.get("message"),
            "timestamp": datetime.utcnow()
        }

        if tx_data["user_id"] is None:
            raise ValueError("user_id is required to create a transaction")
        try:
            new_id = self.transactionRepo.create(tx_data)
            tx = Transaction(id=new_id, **tx_data)

            print(f"[DB] Created transaction {tx.id} (status={tx.status})")
            return tx
        except Exception as e:
            print("[DB][ERROR] Create failed:", str(e))
            raise e

    def processCorePayment(self, tx: Transaction):
        try:
            result = self.coreClientService.handleTransaction(tx)

            if result.get("success"):
                tx.status = TransactionStatus.SUCCESS
                print(f"[CORE] Payment Successfully for tx {tx.id}")
            else:
                tx.status = TransactionStatus.FAILED
                print(f"[CORE] Payment FAILED for tx {tx.id}: {tx.message}")

        except Exception as e:
            tx.status = TransactionStatus.FAILED
            print(f"[CORE] Exception during core payment: {e}")

        self.transactionRepo.update(id=tx.id, payload=tx.toDict())
        return tx

    def commitOnChain(self, tx: Transaction):
        try:
            commitTx = CommitTransaction(
                user_id=tx.user_id,
                campaign_id=tx.campaign_id,
                transaction_id=tx.id,
                amount=tx.amount,
                status=tx.status,
                message=tx.message or ""
            )
            tx_hash = self.smartContractService.commitTransaction(commitTx)

            explorer_prefix = self.explorer_tx_prefix.rstrip("/")

            tx.status = TransactionStatus.COMMITTED
            tx.blockchain_hash = tx_hash
            tx.receipt_url = f"{explorer_prefix}/{tx_hash}"

            print(f"[CHAIN] Smart contract committed tx {tx.id}: {tx_hash}")

        except Exception as e:
            tx.status = TransactionStatus.UNCOMMITTED
            tx.message = f"Blockchain error: {e}"
            print(f"[CHAIN] Commit FAILED for tx {tx.id}: {e}")

        self.transactionRepo.update(
            id=tx.id, payload=tx.toDict()
        )
        print(f"[CHAIN] Successfully commit transaction")

        return tx
