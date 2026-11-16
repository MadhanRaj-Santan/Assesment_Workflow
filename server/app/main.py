from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import request
from app.api import customer,owner

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Approval System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Connect the customer routes to the main application
app.include_router(customer.router)
app.include_router(owner.router)

@app.get("/")
async def root():
    return {"message": "Customer Approval System API is running"}