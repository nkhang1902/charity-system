from flask import request, jsonify, make_response
from app.src.utils.handlerWrapper import handle_api_exceptions
from app.src.utils.request import validatePayload, splitArg
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.models.exception import ApiException
from app.src.models.organization import Organization
from app.src.models.organization import OrganizationQueryParams
from app.src.services.organizationService import OrganizationService

class OrganizationHandler:
    def __init__(self, organizationService: OrganizationService):
        self.service = organizationService

    @handle_api_exceptions
    def getList(self):
        args = request.args
        params = OrganizationQueryParams(
            q=args.get("q"),
            id=splitArg(args, "id"),
            category=splitArg(args, "category")
        )
        data = self.service.getList(params)
        return make_response([item.viewDict() for item in data], 200)

    @handle_api_exceptions
    def getById(self, id):
        data = self.service.getById(id)
        if data is None:
            raise ApiException(API_ERROR_CODE.NOT_FOUND, 404)
        return make_response(data.viewDict(), 200)

    @handle_api_exceptions
    def create(self):
        if request.headers.get("Content-Type") != "application/json" or request.json is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        payload = validatePayload(Organization, request.json)
        if payload is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        self.service.create(payload)
        return make_response({"success": True}, 201)

    @handle_api_exceptions
    def update(self, id):
        existedData = self.service.getById(id)
        if existedData is None:
            raise ApiException(API_ERROR_CODE.NOT_FOUND, 404)

        if request.headers.get("Content-Type") != "application/json" or request.json is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        payload = validatePayload(Organization, request.json)
        if payload is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        self.service.update(id, payload)
        return make_response({"success": True}, 200)

    @handle_api_exceptions
    def delete(self, orgId):
        existedData = self.service.getById(orgId)
        if existedData is None:
            raise ApiException(API_ERROR_CODE.NOT_FOUND, 404)

        self.service.delete(orgId)
        return make_response({"success": True}, 200)
