from flask import Blueprint
from src.handlers.organizationHandler import OrganizationHandler

class OrganizationRouter:
    def __init__(self, handler: OrganizationHandler):
        self.handler = handler
        self.router = Blueprint("organization", __name__)
        self._registerRoutes()

    def _registerRoutes(self):
        self.router.route(
            "/",
            methods=["GET"],
            endpoint="get_organization_list"
        )(lambda: self.handler.getList())

        self.router.route(
            "/<orgId>",
            methods=["GET"],
            endpoint="get_organization_by_id"
        )(lambda orgId: self.handler.getById(orgId))

        self.router.route(
            "/",
            methods=["POST"],
            endpoint="create_organization"
        )(lambda: self.handler.create())

        self.router.route(
            "/<orgId>",
            methods=["PUT"],
            endpoint="update_organization"
        )(lambda orgId: self.handler.update(orgId))

        self.router.route(
            "/<orgId>",
            methods=["DELETE"],
            endpoint="delete_organization"
        )(lambda orgId: self.handler.delete(orgId))

    def getRouter(self):
        return self.router