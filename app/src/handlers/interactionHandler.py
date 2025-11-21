from flask import request, jsonify, make_response
from app.src.utils.handlerWrapper import handle_api_exceptions
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.models.exception import ApiException
from app.src.utils.request import validatePayload
from app.src.models.userInteraction import UserInteraction
from app.src.services.interactionService import InteractionService


class InteractionHandler:
    def __init__(self, InteractionService: InteractionService):
        self.service = InteractionService

    @handle_api_exceptions
    def create(self):
        if request.headers.get("Content-Type") != "application/json" or request.json is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        payload = validatePayload(UserInteraction, request.json)
        if payload is None:
            raise ApiException(API_ERROR_CODE.BAD_REQUEST, 400)

        self.service.create(payload)
        return make_response({"success": True}, 201)
