from flask import Flask, make_response, jsonify

from src.providers.s3 import S3
from src.providers.mysql import MySQL

from src.models.exception import ApiException
from src.constants.errorCode import API_ERROR_CODE

from src.repositories.organizationRepository import OrganizationRepository
from src.repositories.campaignRepository import CampaignRepository

from src.services.organizationService import OrganizationService
from src.services.campaignService import CampaignService

from src.handlers.campaignHandler import CampaignHandler
from src.handlers.organizationHandler import OrganizationHandler

from src.routers.campaignRouter import CampaignRouter
from src.routers.organizationRouter import OrganizationRouter

app = Flask(__name__)

s3 = S3()
db = MySQL()

organizationRepository = OrganizationRepository(db)
organizationService = OrganizationService(organizationRepository)

campaignRepository = CampaignRepository(db)
campaignService = CampaignService(campaignRepository)

organizationHandler = OrganizationHandler(organizationService)
campaignHandler = CampaignHandler(campaignService)

organizationRouter = OrganizationRouter(organizationHandler)
campaignRouter = CampaignRouter(campaignHandler)

app.register_blueprint(
    organizationRouter.getRouter(),
    url_prefix="/organizations"
)

app.register_blueprint(
    campaignRouter.getRouter(),
    url_prefix="/campaigns"
)

# @app.before_request
# def applyMiddlewares():
#     path = request.path
#     if path == ("/login"):
#         return
#     jwtMiddleware()

@app.errorhandler(404)
def handle_undefined_route(e):
    error = ApiException(API_ERROR_CODE.BAD_REQUEST, 400)
    return error.to_response()

@app.errorhandler(405)
def handle_undefined_method(e):
    error = ApiException(API_ERROR_CODE.BAD_REQUEST, 400)
    return error.to_response()

@app.errorhandler(ApiException)
def handle_api_exception(error: ApiException):
    return error.to_response()

@app.errorhandler(Exception)
def handle_exception(error: Exception):
    print(str(error))
    return make_response(jsonify({"error": API_ERROR_CODE.INTERNAL_SERVER_ERROR}), 500)

if __name__ == "__main__":
    app.run(debug=False)