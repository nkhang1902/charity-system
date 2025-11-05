from flask import request, jsonify, make_response
from src.utils.handlerWrapper import handle_api_exceptions
from src.utils.dictValidate import validatePayload
from src.constants.errorCode import API_ERROR_CODE
from src.models.exception import ApiException
from src.models.campaign import Campaign
from src.services.campaignService import CampaignService

class CampaignHandler:
    def __init__(self, campaignService: CampaignService):
        self.service = campaignService

    @handle_api_exceptions
    def getList(self):
        data = self.service.getList()
        return make_response(jsonify(data), 200)

    @handle_api_exceptions
    def getById(self, id):
        data = self.service.getById(id)
        return make_response(jsonify(data), 200)

    @handle_api_exceptions
    def create(self):
        payload = validatePayload(Campaign, request.json)
        if payload is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        self.service.create(payload)
        return make_response({"success": True}, 201)

    @handle_api_exceptions
    def update(self, id):
        existedData = self.service.getById(id)
        if existedData is None:
            raise ApiException(API_ERROR_CODE.NOT_FOUND, 404)

        payload = validatePayload(Campaign, request.json)
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
