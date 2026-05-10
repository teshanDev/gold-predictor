# Gold Price Predictor

A full-stack web application that fetches live gold futures prices and uses machine learning to forecast prices for up to 30 days into the future. Built with a FastAPI backend and a React frontend.

## Live Demo

| | URL |
|---|---|
| Frontend | [gold-predictor-mu.vercel.app](https://gold-predictor-mu.vercel.app) |
| Backend API | [gold-predictor-production-7ebf.up.railway.app](https://gold-predictor-production-7ebf.up.railway.app) |

## Tech Stack

**Backend**
- Python 3.13, FastAPI, Uvicorn
- scikit-learn (Linear Regression)
- pandas, NumPy
- httpx (Yahoo Finance data fetching)
- Deployed on Railway

**Frontend**
- React 18, Vite
- Recharts (price forecast chart)
- Axios
- Deployed on Vercel

## How It Works

1. **Data fetching** — the backend calls the Yahoo Finance API for the `GC=F` (COMEX gold front-month futures) ticker, retrieving up to 365 days of daily closing prices.
2. **Feature engineering** — each trading day is converted to an integer ordinal (days elapsed since the first row), giving the model a simple numeric time axis.
3. **Model training** — a Linear Regression is fit on the full history at request time, capturing the overall price trend.
4. **Forecasting** — the trained model extrapolates forward for the requested number of days, returning a list of `{ date, predicted_price }` objects.
5. **Rendering** — the React frontend plots predictions as a line chart (Recharts) and displays them in a sortable table, with a live spot price shown in the header.

## Features

- Live gold spot price fetched from Yahoo Finance on every load
- Adjustable forecast horizon: 3, 7, 14, or 30 days
- Interactive line chart of predicted prices
- Detailed prediction table with formatted USD values
- REST API with automatic OpenAPI docs at `/docs`
- CORS-configured for both local development and the production Vercel domain

## How to Run Locally

### Prerequisites

- Python 3.13+
- Node.js 18+

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

To point the frontend at a different backend, create a `.env.local` file in the `frontend/` folder:

```
VITE_API_URL=http://localhost:8000
```

### API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/gold/current-price` | Live gold spot price (USD) |
| `GET` | `/api/gold/predict?days=7` | Predicted prices for the next N days (1–30) |
