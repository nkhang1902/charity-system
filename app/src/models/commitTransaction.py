from dataclasses import dataclass
from typing import Optional
from app.src.constants.transactionStatus import TransactionStatus

@dataclass
class CommitTransaction:
    user_id: int
    campaign_id: int
    transaction_id: int
    amount: float
    payment_ref: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None

    def toSmartContractArgs(self):
        return (
            int(self.user_id),
            int(self.campaign_id),
            int(self.transaction_id),
            int(self.amount),
            str(self.status.value),
            self.message or ""
        )

    def execute(self):
        print(
            f"[SmartContract] Executing commit for tx={self.transaction_id}, "
            f"user={self.user_id}, campaign={self.campaign_id}, amount={self.amount}"
        )
        return {"status": "success", "transaction_id": self.transaction_id}
