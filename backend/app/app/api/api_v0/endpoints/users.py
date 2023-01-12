from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.default import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api.api_v0 import deps
from app.schemas.response import Status, SuccessfulResponse
from app.utils import get_limit_offset

router = APIRouter()


@router.get("/", response_model=SuccessfulResponse[Page[schemas.User]])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    params: Params = Depends(),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    params = resolve_params(params)
    limit, offset = get_limit_offset(params)

    users, total = await crud.user.get_multi_count(db, offset=offset, limit=limit)
    return SuccessfulResponse(data=create_page(users, total, params), status=Status.success)


@router.put("/me", response_model=SuccessfulResponse[schemas.User])
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    full_name: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if full_name is not None:
        user_in.full_name = full_name
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return SuccessfulResponse(data=user, status=Status.success)


@router.get("/me", response_model=SuccessfulResponse[schemas.User])
async def read_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """

    return SuccessfulResponse(data=current_user, status=Status.success)


@router.get("/oidc_me", response_model=SuccessfulResponse[schemas.OIDCUser])
async def read_user_oidc_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: schemas.OIDCUser = Depends(deps.get_current_oidc_user),
) -> Any:
    """
    Get oidc user info.
    """
    return SuccessfulResponse(data=current_user, status=Status.success)


@router.get("/{user_id}", response_model=SuccessfulResponse[schemas.User])
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return SuccessfulResponse(data=user, status=Status.success)
    return SuccessfulResponse(data=user, status=Status.success)


@router.put("/{user_id}", response_model=SuccessfulResponse[schemas.User])
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return SuccessfulResponse(data=user, status=Status.success)
