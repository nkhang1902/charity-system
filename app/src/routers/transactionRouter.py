from flask import Blueprint, request
from app.src.handlers.transactionHandler import TransactionHandler
from app.src.models.createTransaction import CreateTransaction

class TransactionRouter:
    def __init__(self, handler: TransactionHandler):
        self.handler = handler
        self.router = Blueprint("transactions", __name__)
        self._registerRoutes()

    def _registerRoutes(self):
        self.router.route(
            "",
            methods=["GET"],
            endpoint="get_transaction_list"
        )(lambda: self.handler.getList())

        self.router.route(
            "/<id>",
            methods=["GET"],
            endpoint="get_transaction_by_id"
        )(lambda id: self.handler.getById(id))

        @self.router.route("", methods=["POST"], endpoint="create_transaction")
        def create_transaction():
            data = request.get_json()
            payload = CreateTransaction(**data)
            return self.handler.createTransaction(payload)

    def getRouter(self):
        return self.router