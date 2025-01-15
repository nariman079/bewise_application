from typing import Annotated

from fastapi import Query


def pagination_params(
    limit: Annotated[int, Query(gt=1)] = 24 ,
    offset: Annotated[int, Query(gt=1)] = 1 
    ) -> dict:
    return {"limit": limit, "offset": offset}