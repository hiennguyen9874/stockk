from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.default import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse
from app.utils import get_limit_offset

router = APIRouter()


@router.post("/", response_model=SuccessfulResponse[schemas.Industry])
async def create_industry(
    *,
    db: AsyncSession = Depends(deps.get_db),
    industry_in: schemas.IndustryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new industry.
    """
    industry = await crud.industry.create(db=db, obj_in=industry_in)
    return SuccessfulResponse(data=industry, status=Status.ok)


@router.get("/", response_model=SuccessfulResponse[Page[schemas.Industry]])
async def read_industries(
    db: AsyncSession = Depends(deps.get_db),
    params: Params = Depends(),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve industries.
    """
    params = resolve_params(params)  # type: ignore
    limit, offset = get_limit_offset(params)

    industries, total = await crud.industry.get_multi_count(db, offset=offset, limit=limit)
    return SuccessfulResponse(data=create_page(industries, total, params), status=Status.ok)


@router.get("/{id}", response_model=SuccessfulResponse[schemas.Industry])
async def read_industry(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get industry by ID.
    """
    industry = await crud.industry.get(db=db, id=id)
    if not industry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Industry not found")
    return SuccessfulResponse(data=industry, status=Status.ok)


@router.put("/{id}", response_model=SuccessfulResponse[schemas.Industry])
async def update_industry(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    industry_in: schemas.IndustryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an industry.
    """
    industry = await crud.industry.get(db=db, id=id)
    if not industry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Industry not found")
    industry = await crud.industry.update(db=db, db_obj=industry, obj_in=industry_in)
    return SuccessfulResponse(data=industry, status=Status.ok)


@router.delete("/{id}", response_model=SuccessfulResponse[schemas.Industry])
async def delete_industry(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an industry.
    """
    # TODO: Two time query

    industry = await crud.industry.get(db=db, id=id)

    if not industry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Industry not found")

    industry = await crud.industry.remove(db=db, id=id)

    return SuccessfulResponse(data=industry, status=Status.ok)
