from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from temporalio.client import Client
from typing import List

from app.database import get_db
from app.models.request import CustomerRequest
from app.schemas.request import RequestResponse
from app.temporal.workflows import ApprovalWorkflow

router = APIRouter(prefix="/api/owner", tags=["Owner"])

@router.get("/requests", response_model=List[RequestResponse])
def get_all_requests(db: Session = Depends(get_db)):
    return db.query(CustomerRequest).order_by(CustomerRequest.created_at.desc()).all()

@router.post("/requests/{request_id}/approve")
async def approve_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(CustomerRequest).filter(CustomerRequest.id == request_id).first()
    if not req or not req.temporal_workflow_id:
        raise HTTPException(status_code=404, detail="Request or Workflow not found")
    
    # TEMPORAL INTEGRATION: Send an "APPROVED" signal to the waiting workflow
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(req.temporal_workflow_id)
    await handle.signal(ApprovalWorkflow.submit_decision, "APPROVED")
    
    return {"message": "Approval signal sent to Temporal", "id": request_id}

@router.post("/requests/{request_id}/reject")
async def reject_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(CustomerRequest).filter(CustomerRequest.id == request_id).first()
    if not req or not req.temporal_workflow_id:
        raise HTTPException(status_code=404, detail="Request or Workflow not found")
    
    # TEMPORAL INTEGRATION: Send a "REJECTED" signal to the waiting workflow
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(req.temporal_workflow_id)
    await handle.signal(ApprovalWorkflow.submit_decision, "REJECTED")
    
    return {"message": "Rejection signal sent to Temporal", "id": request_id}