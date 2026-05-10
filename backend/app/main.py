from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import predictions, prices

app = FastAPI(title="Gold Price Predictor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://gold-predictor-mu.vercel.app",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(prices.router)
app.include_router(predictions.router)
