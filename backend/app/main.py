from fastapi import FastAPI

from app.api.routes.transactions import router as transaction_router


app = FastAPI(
    title="FraudLens API",
    description="Explainable real-time fraud risk detection API",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "FraudLens API"
    }


app.include_router(transaction_router)