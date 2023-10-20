from fastapi import FastAPI
from pdf_summary import router as pdf_summary_router

app = FastAPI()

app.include_router(pdf_summary_router)