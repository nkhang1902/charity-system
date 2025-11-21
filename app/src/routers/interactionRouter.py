from flask import Blueprint, request
from app.src.handlers.interactionHandler import InteractionHandler

class InteractionRouter:
    def __init__(self, handler: InteractionHandler):
        self.handler = handler
        self.router = Blueprint("interactions", __name__)
        self._registerRoutes()

    def _registerRoutes(self):
        self.router.route(
            "",
            methods=["POST"],
            endpoint="create_interaction"
        )(lambda: self.handler.create())

    def getRouter(self):
        return self.router