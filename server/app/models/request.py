from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CustomerRequest(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    description = Column(String)
    file_path = Column(String)
    status = Column(String, default="PENDING")
    approval_result = Column(Boolean, nullable=True)
    temporal_workflow_id = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())