from fastapi import APIRouter, HTTPException, Query

from app.models.prediction import PredictionItem
from app.services.predictor import predict_future

router = APIRouter()


@router.get("/api/gold/predict", response_model=list[PredictionItem])
def predict_gold_prices(
    days: int = Query(default=7, ge=1, le=30, description="Number of days to predict"),
):
    try:
        return predict_future(days)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
