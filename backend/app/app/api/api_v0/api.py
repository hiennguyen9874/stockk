from typing import Dict, Union

from fastapi import APIRouter

from app.api.api_v0.endpoints import (
    industries,
    items,
    login,
    tickers,
    users,
    util,
    tradingview,
)
from app.schemas.response import ErrorResponse, ValidationErrorResponse

api_router = APIRouter(
    responses={
        422: {
            "model": ValidationErrorResponse[Union[str, Dict]],
            "description": "Validation Error",
        }
    }
)

api_router.include_router(
    login.router,
    prefix="/login",
    tags=["login"],
    responses={
        400: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Could not validate credentials",
        },
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
        404: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "User not found",
        },
    },
)

api_router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    responses={
        400: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Could not validate credentials",
        },
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
        404: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "User not found",
        },
    },
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    responses={
        400: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Could not validate credentials",
        },
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
        404: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "User not found",
        },
    },
)


api_router.include_router(util.router, prefix="/utils", tags=["utils"])


api_router.include_router(
    tickers.router,
    prefix="/tickers",
    tags=["tickers"],
    responses={
        400: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Could not validate credentials",
        },
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
        404: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "User not found",
        },
    },
)

api_router.include_router(
    industries.router,
    prefix="/industries",
    tags=["industries"],
    responses={
        400: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Could not validate credentials",
        },
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
        404: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "User not found",
        },
    },
)

api_router.include_router(tradingview.router, prefix="/tradingview", tags=["tradingview"])
