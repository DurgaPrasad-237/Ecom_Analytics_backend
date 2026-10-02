import os
from pathlib import Path


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.routes import customer,products,sales,ai



app = FastAPI(
    title="Indian E-Commerce Analytics API",
    description="Backend API for e-commerce analytics",
    version="1.0.0",
)

origin = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.get("/")
def root():
    return {
        "message": "Indian E-Commerce Analytics API is running"
    }


app.include_router(customer.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(ai.router)
