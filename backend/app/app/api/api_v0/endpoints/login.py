from datetime import timedelta
from typing import Any, Dict, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.settings import settings
from app.schemas.response import ErrorResponse

router = APIRouter()


@router.post(
    "/exchange-oidc-token",
    response_model=schemas.Token,
    responses={
        403: {
            "model": ErrorResponse[Union[str, Dict]],
            "description": "Inactive user or The user doesn't have enough privileges",
        },
    },
)
async def exchange_oidc_token(
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user_from_oidc),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password"
        )

    if not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post(
    "/test-token",
    response_model=schemas.User,
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
async def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token.
    """
    return current_user
