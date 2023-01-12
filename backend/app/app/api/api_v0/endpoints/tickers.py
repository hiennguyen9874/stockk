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


@router.post("/", response_model=SuccessfulResponse[schemas.Ticker])
async def create_ticker(
    *,
    db: AsyncSession = Depends(deps.get_db),
    ticker_in: schemas.TickerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new ticker.
    """
    ticker = await crud.ticker.create(db=db, obj_in=ticker_in)
    return SuccessfulResponse(data=ticker, status=Status.success)


@router.get("/", response_model=SuccessfulResponse[Page[schemas.Ticker]])
async def read_tickers(
    db: AsyncSession = Depends(deps.get_db),
    params: Params = Depends(),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tickers.
    """
    params = resolve_params(params)  # type: ignore
    limit, offset = get_limit_offset(params)

    tickers, total = await crud.ticker.get_multi_count(db, offset=offset, limit=limit)
    return SuccessfulResponse(data=create_page(tickers, total, params), status=Status.success)


@router.get("/{id}", response_model=SuccessfulResponse[schemas.Ticker])
async def read_ticker(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ticker by ID.
    """
    ticker = await crud.ticker.get(db=db, id=id)
    if not ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    return SuccessfulResponse(data=ticker, status=Status.success)


@router.put("/{id}", response_model=SuccessfulResponse[schemas.Ticker])
async def update_ticker(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    ticker_in: schemas.TickerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an ticker.
    """
    ticker = await crud.ticker.get(db=db, id=id)
    if not ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    ticker = await crud.ticker.update(db=db, db_obj=ticker, obj_in=ticker_in)
    return SuccessfulResponse(data=ticker, status=Status.success)


@router.delete("/{id}", response_model=SuccessfulResponse[schemas.Ticker])
async def delete_ticker(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an ticker.
    """
    # TODO: Two time query

    ticker = await crud.ticker.get(db=db, id=id)

    if not ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")

    ticker = await crud.ticker.remove(db=db, id=id)

    return SuccessfulResponse(data=ticker, status=Status.success)
