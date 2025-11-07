from flask import Blueprint
from app.src.handlers.transactionHandler import TransactionHandler

class TransactionRouter:
    def __init__(self, handler: TransactionHandler):
        self.handler = handler
        self.router = Blueprint("transaction", __name__)
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

    def getRouter(self):
        return self.router