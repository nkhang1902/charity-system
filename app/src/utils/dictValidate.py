from dataclasses import fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T")

def validatePayload(model: Type[T], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generic dataclass payload validator.
    Keeps only keys that match field names of the given dataclass.
    """
    if not is_dataclass(model):
        raise TypeError(f"{model.__name__} is not a dataclass")

    valid_fields = {f.name for f in fields(model)}
    return {k: v for k, v in payload.items() if k in valid_fields}
