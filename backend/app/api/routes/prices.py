from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.data_fetcher import get_current_gold_price

router = APIRouter()


class GoldPriceResponse(BaseModel):
    price: float
    currency: str
    timestamp: str


@router.get("/api/gold/current-price", response_model=GoldPriceResponse)
def current_gold_price():
    try:
        price = get_current_gold_price()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    return GoldPriceResponse(
        price=price,
        currency="USD",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
