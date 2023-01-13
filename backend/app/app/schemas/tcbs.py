from typing import Optional

from pydantic import BaseModel


class SearchSymbolResultItem(BaseModel):
    name: str
    value: str
    type: str
    exchange: str
    industry: Optional[str]
