from pydantic import BaseModel
from datetime import datetime

# Schema for returning data to the frontend
class RequestResponse(BaseModel):
    id: int
    customer_name: str
    description: str
    file_path: str
    status: str
    created_at: datetime
    
    class Config:
        # Tells Pydantic to read data even if it is not a standard dict (like a SQLAlchemy model)
        from_attributes = True