from fastapi import FastAPI

from app.api.v1.test import router

app = FastAPI(
    title="Expense Tracker API"
)

app.include_router(router)
