import traceback

from flask import make_response, jsonify
from functools import wraps
from src.models.exception import ApiException
from src.constants.errorCode import API_ERROR_CODE

def handle_api_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as ex:
            return ex.to_response()
        except Exception as ex:
            print(f"Error in {func.__name__}: {str(ex)}")
            print(traceback.format_exc())
            return make_response(
                jsonify({"error": API_ERROR_CODE.INTERNAL_SERVER_ERROR}),
                500
            )
    return wrapper
