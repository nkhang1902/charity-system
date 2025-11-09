from app.src.repositories.transactionRepository import TransactionRepository
from app.src.models.transaction import Transaction

class WebhookService:
    def __init__(self, transactionRepository: TransactionRepository):
        self.transactionRepo = transactionRepository

    def commitTransaction(self, payload: dict):
        tx = Transaction(
            id=self.repo.get_next_id(),
            user_id=payload["user_id"],
            campaign_id=payload["campaign_id"],
            amount=payload["amount"],
            status=payload["status"],
            message=payload.get("message"),
            receipt_url=payload.get("receipt_url"),
            timestamp=datetime.utcnow()
        )

        self.repo.insert(tx)
        return tx
