from app.src.repositories.transactionRepository import TransactionRepository
from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams

class TransactionService:
    def __init__(self, transactionRepository: TransactionRepository):
        self.transactionRepo = transactionRepository

    def getById(self, id: str) -> Transaction | None:
        return self.transactionRepo.getById(id)

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        return self.transactionRepo.getList(params)

    def createTransaction(self, payload: dict):
        tx = Transaction(
            id=self.repo.get_next_id(),
            user_id=payload["user_id"],
            campaign_id=payload["campaign_id"],
            amount=payload["amount"],
            status="PENDING",
            message=payload.get("message"),
            receipt_url=payload.get("receipt_url"),
            timestamp=datetime.utcnow()
        )

        self.repo.insert(tx)
        return tx
