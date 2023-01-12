from typing import Tuple

from fastapi_pagination.bases import AbstractParams

__all__ = ["get_limit_offset"]


def get_limit_offset(params: AbstractParams) -> Tuple[int, int]:
    raw_params = params.to_raw_params()
    limit, offset = raw_params.limit, raw_params.offset
    return limit, offset
