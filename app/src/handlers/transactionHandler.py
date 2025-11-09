from flask import request, jsonify, make_response
from app.src.utils.handlerWrapper import handle_api_exceptions
from app.src.utils.request import splitArg
from app.src.models.transaction import TransactionQueryParams
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.models.exception import ApiException
from app.src.services.transactionService import TransactionService
from app.src.models.createTransaction import CreateTransaction

class TransactionHandler:
    def __init__(self, TransactionService: TransactionService):
        self.service = TransactionService

    @handle_api_exceptions
    def getList(self):
        args = request.args
        params = TransactionQueryParams(
            user_id=splitArg(args, "user_id"),
            campaign_id=splitArg(args, "campaign_id"),
            status=splitArg(args, "status"),
            min_amount=args.get("min_amount"),
            max_amount=args.get("max_amount"),
            from_timestamp=args.get("from_timestamp"),
            to_timestamp=args.get("to_timestamp")
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
    def createTransaction(self, payload: CreateTransaction):
        tx = self.service.createTransaction(vars(payload))

        if tx is None:
            raise ApiException(API_ERROR_CODE.INTERNAL_SERVER_ERROR, 500)

        return make_response(tx.viewDict(), 201)
