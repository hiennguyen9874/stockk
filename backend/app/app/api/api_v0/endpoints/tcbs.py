import httpx
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.api.api_v0 import deps
from app.schemas.response import Status, SuccessfulResponse

router = APIRouter()


@router.get("/search", response_model=SuccessfulResponse[List[schemas.SearchSymbolResultItem]])
async def search(
    *,
    key: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search stock by key
    """

    headers = {
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "Accept-language": "vi",
        "sec-ch-ua-mobile": "?0",
        # "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhdXRoZW5fc2VydmljZSIsImV4cCI6MTY3MzYwNDM4MSwianRpIjoiIiwiaWF0IjoxNjczNTc1NTgxLCJzdWIiOiIwMDAxOTc3NjY3IiwiY3VzdG9keUlEIjoiMTA1Qzg3NzY2NyIsImVtYWlsIjoiaGllbm5ndXllbjk4NzRAZ21haWwuY29tIiwicm9sZXMiOlsiY3VzdG9tZXIiLCJBcHBsaWNhdGlvbi9DQUZGRUlORV9CRVRBX1VTRVJfQ1JFTUEiLCJBcHBsaWNhdGlvbi9DQUZGRUlORV9CRVRBX1VTRVJfQ1JFTUFfQksxIl0sInN0ZXB1cF9leHAiOjAsInNvdHBfc2lnbiI6IiIsImNsaWVudF9rZXkiOiJRcjMwa1JmaktjZTl3RzhNUEx5Y3ZNWHY0bUtucGtlSiIsInNlc3Npb25JRCI6IjczMWM1YjVmLWRiZWQtNDY3Yi04YzFiLWQ0YjYyMWUxNzI2MyIsImFjY291bnRfc3RhdHVzIjoiMSIsIm90cCI6IiIsIm90cFR5cGUiOiIiLCJvdHBTb3VyY2UiOiJUQ0lOVkVTVCIsIm90cFNlc3Npb25JZCI6IiJ9.faWICAX_kiXJe2RVafsQZYZj3La4yXUWOiKdZAzQdcne63bP6SibLSyPmkJEthcpTM6UC-VCXfMYLSmqVy25GwYja5Ia_7Q-UIpf1mtKR6qxZ2klI5jnUuuzh_LJXb8r1Pa2bloYpY8jAFrzM2nlVozZDKGY0Vo6qaAKpds2Tay5XBWdA2RXWfhKEf4uKkBYc4Gz4B-3W_Gi8EEJT0GvM8qBfS33Q04NdsREBk_OI46udGlSC9c0-UYY0hvbH9cjAsD2NvMbeUb1fWMlxM_FyGeAhO5OPFX0Z86cp7Rbc-b4WQupMNsrbeUHfOBV-pqWULUx17wJMB-ysn6TklZMZw",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "https://tcinvest.tcbs.com.vn/",
        "sec-ch-ua-platform": '"Linux"',
    }

    params = {
        "key": key,
    }

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            "https://apipubaws.tcbs.com.vn/stock-insight/v1/search", params=params, headers=headers
        )

        result = response.json()

        assert "status" in result and "data" in result and "msg" in result

        if result["status"] != 200:
            raise HTTPException(status_code=result["status"], detail=result["msg"])

        return SuccessfulResponse(
            data=list(map(lambda item: schemas.SearchSymbolResultItem(**item), result["data"])),
            status=Status.success,
        )
