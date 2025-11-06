from flask import Blueprint
from app.src.handlers.campaignHandler import CampaignHandler

class CampaignRouter:
    def __init__(self, handler: CampaignHandler):
        self.handler = handler
        self.router = Blueprint("campaign", __name__)
        self._registerRoutes()

    def _registerRoutes(self):
        self.router.route(
            "",
            methods=["GET"],
            endpoint="get_campaign_list"
        )(lambda: self.handler.getList())

        self.router.route(
            "/<campaignId>",
            methods=["GET"],
            endpoint="get_campaign_by_id"
        )(lambda campaignId: self.handler.getById(campaignId))

        self.router.route(
            "",
            methods=["POST"],
            endpoint="create_campaign"
        )(lambda: self.handler.create())

        self.router.route(
            "/<campaignId>",
            methods=["PUT"],
            endpoint="update_campaign"
        )(lambda campaignId: self.handler.update(campaignId))

        self.router.route(
            "/<campaignId>",
            methods=["DELETE"],
            endpoint="delete_campaign"
        )(lambda campaignId: self.handler.delete(campaignId))

    def getRouter(self):
        return self.router