from app.src.repositories.transactionRepository import TransactionRepository
from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams
from app.src.models.commitTransaction import CommitTransaction
from app.src.services.coreClientSerivce import CoreClientSerivce
from app.src.services.smartContractService import SmartContractService
from datetime import datetime
from app.src.constants.transactionStatus import TransactionStatus

class TransactionService:
    def __init__(self, transactionRepository: TransactionRepository):
        self.transactionRepo = transactionRepository
        self.coreClientService = CoreClientSerivce()
        self.smartContractService = SmartContractService()

    def getById(self, id: str) -> Transaction | None:
        return self.transactionRepo.getById(id)

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        return self.transactionRepo.getList(params)

    def createTransaction(self, payload: dict) -> Transaction:
        tx_data = {
            "user_id": payload["user_id"],
            "campaign_id": payload["campaign_id"],
            "amount": payload["amount"],
            "status": TransactionStatus.NEW,
            "message": payload.get("message"),
            "timestamp": datetime.utcnow(),
        }

        new_id = self.transactionRepo.create(tx_data)
        tx = Transaction(id=new_id, **tx_data)
        print(f"Created transaction {tx.id} (status={tx.status})")

        try:
            commit_tx = CommitTransaction(
                user_id=tx.user_id,
                campaign_id=tx.campaign_id,
                transaction_id=tx.id,
                amount=tx.amount,
                message=tx.message,
                status=tx.status
            )
            print(
                f"Created transaction {tx.id} (status={tx.status})"
            )
            result = commit_tx.execute()
            print(f"Core transaction successful for tx {tx.id}")

        except Exception as e:
            print(f"Smart contract commit failed for tx {tx.id}: {e}")

        return tx

    def createNewTransaction(self, payload: dict) -> Transaction:
        tx_data = {
            "user_id": payload.get("user_id"),  # <-- đảm bảo có
            "campaign_id": payload["campaign_id"],
            "amount": payload["amount"],
            "status": TransactionStatus.NEW,
            "message": payload.get("message"),
            "timestamp": datetime.utcnow()
        }

        if tx_data["user_id"] is None:
            raise ValueError("user_id is required to create a transaction")

        new_id = self.transactionRepo.create(tx_data)
        tx = Transaction(id=new_id, **tx_data)
        print(f"Created transaction {tx.id} (status={tx.status})")
        return tx

    def processCorePayment(self, tx: Transaction):
        try:
            result = self.coreClientService.handleTransaction(tx)
            if result.get("success"):
                print(f"Core transaction successful for tx {tx.id}")
                tx.status = TransactionStatus.SUCCESS
            else:
                tx.status = TransactionStatus.FAILED
                tx.message = result.get("error", "Core transaction failed")
                print(f"Core service failed for tx {tx.id}: {tx.message}")
        except Exception as e:
            tx.status = TransactionStatus.FAILED
            tx.message = f"Core error: {e}"
            print(f"Exception during core payment: {e}")

    def commitOnChain(self, tx: Transaction):
        try:
            commitTx = CommitTransaction(
                user_id=tx.user_id,
                campaign_id=tx.campaign_id,
                transaction_id=tx.id,
                amount=tx.amount,
                message=tx.message or ""
            )

            txHash = self.smartContractService.commitTransaction(commitTx)

            tx.status = TransactionStatus.COMMITTED
            tx.blockchain_hash = txHash
            tx.message = f"Committed on-chain: {txHash}"

            print(f"Smart contract committed tx {tx.id}: {txHash}")

        except Exception as e:
            tx.status = TransactionStatus.UNCOMMITTED
            tx.message = f"Smart contract error: {e}"
            print(f"Smart contract commit failed for tx {tx.id}: {e}")