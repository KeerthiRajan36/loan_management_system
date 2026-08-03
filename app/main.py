from fastapi import FastAPI

from app.database import *
from app.database import Base, engine
from app.routers.emis import router as emi_router
from app.routers.auth import router as auth_router
from app.routers.loans import router as loan_router
from app.routers.reports import router as report_router
from app.routers.customers import router as customer_router
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title="Loan Management & EMI Tracking System"
)


Base.metadata.create_all(bind=engine)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(loan_router)
app.include_router(emi_router)
app.include_router(report_router)


@app.get("/")
def home():

    return {
        "application": "Loan Management & EMI Tracking System"
    }

