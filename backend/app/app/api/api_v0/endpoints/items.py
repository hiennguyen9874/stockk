from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.default import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api.api_v0 import deps
from app.schemas.response import Status, SuccessfulResponse
from app.utils import get_limit_offset

router = APIRouter()


@router.post("/", response_model=SuccessfulResponse[schemas.Item])
async def create_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return SuccessfulResponse(data=item, status=Status.success)


@router.get("/", response_model=SuccessfulResponse[Page[schemas.Item]])
async def read_items(
    db: AsyncSession = Depends(deps.get_db),
    params: Params = Depends(),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    params = resolve_params(params)  # type: ignore
    limit, offset = get_limit_offset(params)

    items, total = await crud.item.get_multi_count(db, offset=offset, limit=limit)
    return SuccessfulResponse(data=create_page(items, total, params), status=Status.success)


@router.get("/{id}", response_model=SuccessfulResponse[schemas.Item])
async def read_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return SuccessfulResponse(data=item, status=Status.success)


@router.put("/{id}", response_model=SuccessfulResponse[schemas.Item])
async def update_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item = await crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return SuccessfulResponse(data=item, status=Status.success)


@router.delete("/{id}", response_model=SuccessfulResponse[schemas.Item])
async def delete_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    # TODO: Two time query

    item = await crud.item.get(db=db, id=id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item = await crud.item.remove(db=db, id=id)

    return SuccessfulResponse(data=item, status=Status.success)
