from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")
ErrorT = TypeVar("ErrorT")


__all__ = ["Status", "ErrorResponse", "SuccessfulResponse"]


class Status(str, Enum):
    ok = "ok"
    error = "error"


class ErrorResponse(GenericModel, Generic[ErrorT]):
    status: Status = Field(Status.error)
    message: ErrorT = Field(..., example="Error message")
    data: Optional[Any] = Field(None, example="null")


class ValidationErrorResponse(GenericModel, Generic[ErrorT]):
    status: Status = Field(Status.error)
    message: ErrorT = Field(..., example=[{"loc": ["string"], "msg": "string", "type": "string"}])
    data: Optional[Any] = Field(None, example="null")


class SuccessfulResponse(GenericModel, Generic[DataT]):
    status: Status = Field(Status.ok)
    data: Optional[DataT] = None
    error: Optional[Any] = Field(None, example="null")
