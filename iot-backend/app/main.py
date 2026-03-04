from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.router import api_router

app = FastAPI(title="IoT Backend API")

# include all routers
app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/Health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "IoT Backend API running. Visit /docs"}