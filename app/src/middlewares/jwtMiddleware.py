from flask import request, g
from app.src.models.exception import ApiException
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.services.userService import UserService
import jwt
from app.src.core.config import settings

class JwtMiddleware:
    def __init__(self, userService: UserService):
        self.secretKey = settings.JWTSecret
        self.userService = userService
        self.prefix = "Bearer"
        self.headerKey = "Authorization"

    def __call__(self):
        token = self._getToken(request)

        if token:
            try:
                payload = jwt.decode(token, self.secretKey, algorithms=["HS256"])
            except Exception:
                raise ApiException(API_ERROR_CODE.INVALID_TOKEN, 401)
            g.data = payload["data"]
        else:
            raise ApiException(API_ERROR_CODE.MISSING_TOKEN, 401)

    def _getToken(self, request):
        authHeader = request.headers.get(self.headerKey, "")
        if authHeader.startswith(f"{self.prefix} "):
            return authHeader[len(self.prefix)+1:]
        return None