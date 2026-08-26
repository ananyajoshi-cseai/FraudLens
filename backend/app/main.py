from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes.transactions import router as transaction_router
from app.core.database import connect_db, close_db

app = FastAPI(
    title="FraudLens API",
    description="Explainable real-time fraud risk detection API",
    version="0.1.0"
)

# -------------------------
# App Lifecycle (MongoDB Setup)
# -------------------------
@app.on_event("startup")
def startup_event():
    connect_db()

@app.on_event("shutdown")
def shutdown_event():
    close_db()

# -------------------------
# API Routes
# -------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "FraudLens API"
    }

app.include_router(transaction_router)

# -------------------------
# Frontend
# -------------------------
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
def screen_1():
    return FileResponse("../static/index.html")

@app.get("/screen2")
def screen_2():
    return FileResponse("../static/index2.html")

@app.get("/screen3")
def screen_3():
    return FileResponse("../static/index3.html")

@app.get("/screen4")
def screen_4():
    return FileResponse("../static/index4.html")