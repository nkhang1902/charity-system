import jwt
import datetime
from typing import Any, Dict
from app.src.core.config import settings

def jwtGenerate(payload: Dict[str, Any]) -> str:
    def convert_datetimes(obj):
        if isinstance(obj, dict):
            return {k: convert_datetimes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_datetimes(item) for item in obj]
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return obj

    exp_hours = settings.JWTExpiredHours
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=exp_hours)

    payload = {
        "data": convert_datetimes(payload),
        "exp": int(exp_time.replace(tzinfo=datetime.timezone.utc).timestamp())
    }

    token = jwt.encode(payload, settings.JWTSecret, algorithm="HS256")
    return token
