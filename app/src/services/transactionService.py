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