from pydantic import BaseModel


class PredictionItem(BaseModel):
    date: str
    predicted_price: float
