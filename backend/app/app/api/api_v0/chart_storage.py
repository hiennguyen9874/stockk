from typing import Dict, Union

from fastapi import APIRouter

from app.api.api_v0.endpoints import charts, drawing_templates, study_templates
from app.schemas.response import ErrorResponse, ValidationErrorResponse

api_router = APIRouter(
    responses={
        422: {
            "model": ValidationErrorResponse[Union[str, Dict]],
            "description": "Validation Error",
        }
    },
)

api_router.include_router(
    charts.router,
    prefix="/charts",
    tags=["charts"],
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
    study_templates.router,
    prefix="/study_templates",
    tags=["study_templates"],
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
    drawing_templates.router,
    prefix="/drawing_templates",
    tags=["drawing_templates"],
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
