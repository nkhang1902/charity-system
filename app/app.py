from flask import Flask, make_response, jsonify

from app.src.providers.s3 import S3
from app.src.providers.mysql import MySQL

from app.src.models.exception import ApiException
from app.src.constants.errorCode import API_ERROR_CODE

from app.src.repositories.organizationRepository import OrganizationRepository
from app.src.repositories.campaignRepository import CampaignRepository

from app.src.services.organizationService import OrganizationService
from app.src.services.campaignService import CampaignService

from app.src.handlers.campaignHandler import CampaignHandler
from app.src.handlers.organizationHandler import OrganizationHandler

from app.src.routers.campaignRouter import CampaignRouter
from app.src.routers.organizationRouter import OrganizationRouter

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