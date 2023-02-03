from typing import Optional

import pandas as pd
import requests
from loguru import logger

from app import crud, deps, schemas
from app.worker import app

__all__ = ["task_crawl_ticker"]


@app.task(name="task_crawl_ticker")
def task_crawl_ticker() -> None:  # noqa: C901
    # Get list of tickers from ssi

    try:
        tickers = requests.get(
            "https://fiin-core.ssi.com.vn/Master/GetListOrganization?language=vi"
        ).json()["items"]
        tickers_df = pd.DataFrame(tickers)
    except Exception as e:
        logger.error("Error when getting tickers from ssi: {error}", error=str(e))
        return

    with deps.sync_get_db() as db:
        tickers_db = crud.ticker.get_all_sync(db=db)

        # Save ticker not has in database
        ticker_must_create = set(tickers_df["ticker"].tolist()).difference(
            {ticker.ticker for ticker in tickers_db}
        )
        if not ticker_must_create:
            return

        tickers_df_must_create = tickers_df[tickers_df["ticker"].isin(ticker_must_create)]

        def mapComGroupCodeToExchange(comGroupCode: str) -> Optional[schemas.TickerExchange]:
            if comGroupCode == "UpcomIndex":
                return schemas.TickerExchange.UPCOM
            if comGroupCode == "HNXIndex":
                return schemas.TickerExchange.HNX
            if comGroupCode == "VNINDEX":
                return schemas.TickerExchange.HOSE
            return None

        for _, row in tickers_df_must_create.iterrows():
            try:
                crud.ticker.create_sync(
                    db=db,
                    obj_in=schemas.TickerCreate(
                        ticker=row["ticker"],
                        exchange=mapComGroupCodeToExchange(row["comGroupCode"]),
                        name=row["ticker"],
                        full_name=row["organName"],
                        short_name=row["organShortName"],
                        type=schemas.TickerType.vn_stock,
                    ),
                )
            except Exception:
                logger.error("Error when creating ticker: {error}", row["ticker"])
