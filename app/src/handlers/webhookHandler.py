from flask import request, jsonify, make_response
from app.src.utils.handlerWrapper import handle_api_exceptions
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.models.exception import ApiException
from app.src.services.webhookService import WebhookService
from app.src.models.commitTransaction import CommitTransaction

class WebhookHandler:
    def __init__(self, WebhookService: WebhookService):
        self.service = WebhookService

    @handle_api_exceptions
    def commitTransaction(self, payload: CommitTransaction):
        data = self.service.commitTransaction(vars(payload))
        if data is None:
            raise ApiException(API_ERROR_CODE.INTERNAL_ERROR, 500)
        return make_response(tx.viewDict(), 201)