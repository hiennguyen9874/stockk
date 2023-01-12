from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")
ErrorT = TypeVar("ErrorT")


__all__ = ["Error", "Status", "ErrorResponse", "SuccessfulResponse"]


class Error(BaseModel, Generic[ErrorT]):
    code: int
    message: ErrorT


class Status(str, Enum):
    success = "success"
    error = "error"


class ErrorResponse(GenericModel, Generic[ErrorT]):
    status: Status = Field(Status.error)
    error: Error[ErrorT] = Field(..., example=Error(code=400, message="Error message"))
    data: Optional[Any] = Field(None, example="null")


class ValidationErrorResponse(GenericModel, Generic[ErrorT]):
    status: Status = Field(Status.error)
    error: Error[ErrorT] = Field(
        ...,
        example=Error(code=422, message=[{"loc": ["string"], "msg": "string", "type": "string"}]),
    )
    data: Optional[Any] = Field(None, example="null")


class SuccessfulResponse(GenericModel, Generic[DataT]):
    status: Status = Field(Status.success)
    data: Optional[DataT] = None
    error: Optional[Any] = Field(None, example="null")
