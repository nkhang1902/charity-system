from dataclasses import is_dataclass, fields, MISSING
from typing import Type, TypeVar, Dict, Any
from app.src.models.exception import ApiException

T = TypeVar("T")

def validatePayload(model: Type[T], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates a payload for a given dataclass.
    """
    if not is_dataclass(model):
        raise TypeError(f"{model.__name__} is not a dataclass")

    filtered: Dict[str, Any] = {}
    missingFields = []

    for f in fields(model):
        fieldName = f.name
        hasDefault = not (f.default is MISSING and f.default_factory is MISSING)
        if fieldName in payload:
            filtered[fieldName] = payload[fieldName]
        else:
            if not hasDefault and fieldName != "id":
                missingFields.append(fieldName)

    if missingFields:
        raise ApiException(f"Missing required fields: {', '.join(missingFields)}", 400)

    if len(filtered) == 0:
        raise ApiException("Invalid payload", 400)

    return filtered

def splitArg(args: Dict[str, str], name: str):
    val = args.get(name)
    if not val:
        return None
    return [v.strip() for v in val.split(",") if v.strip()]