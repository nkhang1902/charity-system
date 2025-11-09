from flask import Blueprint, request
from app.src.handlers.webhookHandler import WebhookHandler

class WebhookRouter:
    def __init__(self, handler: WebhookHandler):
        self.handler = handler
        self.router = Blueprint("webhook", __name__)
        self._registerRoutes()

    def _registerRoutes(self):
        @self.router.route("/commit-transaction", methods=["POST"], endpoint="commit_transaction")
        def commit_transaction():
            data = request.get_json()
            payload = CommitTransactionRequest(**data)
            return self.handler.commitTransaction(payload)


    def getRouter(self):
        return self.router
