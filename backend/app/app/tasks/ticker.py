from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import pandas as pd
import requests
from celery import shared_task
from loguru import logger

from app import crud, deps, schemas

__all__ = ["task_crawl_ticker"]


@shared_task(name="task_crawl_ticker")
def task_crawl_ticker() -> None:
    # Get list of tickers from ssi

    # try:
    #     tickers = requests.get(
    #         "https://fiin-core.ssi.com.vn/Master/GetListOrganization?language=vi"
    #     ).json()["items"]
    #     tickers_df = pd.DataFrame(tickers)
    # except Exception as e:
    #     logger.error("Error when getting tickers from ssi: {error}", error=str(e))
    #     return

    # with deps.sync_get_db() as db:
    #     tickers_db = crud.ticker.get_all_sync(db=db)

    #     # Save ticker not has in database
    #     ticker_must_create = set(tickers_df["ticker"].tolist()).difference(
    #         {ticker.ticker for ticker in tickers_db}
    #     )
    #     if not ticker_must_create:
    #         return

    #     tickers_df_must_create = tickers_df[tickers_df["ticker"].isin(ticker_must_create)]

    #     def get_ticker_info(ticker: str) -> Optional[dict]:
    #         try:
    #             ticker_info = requests.get(
    #                 f"https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{ticker}/overview"
    #             ).json()
    #         except Exception as e:
    #             logger.error(
    #                 "Error when getting ticker: {ticker} info from tcbs: {error}",
    #                 ticker=ticker,
    #                 error=str(e),
    #             )
    #             return None
    #         return ticker_info

    #     with ThreadPoolExecutor(max_workers=20) as executor:
    #         tickers_info = executor.map(get_ticker_info, ticker_must_create)

    #     tickers_info = list(filter(lambda ticker_info: ticker_info is not None, tickers_info))
    #     tickers_info = pd.DataFrame(tickers_info)

    #     industies = tickers_info[["industryID", "industry", "industryEn"]]

    #     for _, (id, name, enName) in industies.iterrows():
    #         crud.industry.get_or_create_sync(db=db, id=id, name=name, enName=enName)

    #     tickers_df_must_create = pd.merge(
    #         tickers_df_must_create, tickers_info, left_on="ticker", right_on="ticker", how="inner"
    #     )

    #     for _, row in tickers_df_must_create.iterrows():
    #         try:
    #             crud.ticker.create_with_industry_id_sync(
    #                 db=db,
    #                 obj_in=schemas.TickerCreate(
    #                     ticker=row["ticker"],
    #                     companyName=row["organName"],
    #                     shortName=row["organShortName"],
    #                     exchange=row["exchange"],
    #                 ),
    #                 industry_id=row["industryID"],
    #             )
    #         except Exception:
    #             logger.error("Error when creating ticker: {error}", row["ticker"])
    pass
