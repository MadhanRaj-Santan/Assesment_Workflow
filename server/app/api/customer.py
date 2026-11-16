from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from temporalio.client import Client
import os
import shutil
from typing import List

from app.database import get_db
from app.models.request import CustomerRequest
from app.schemas.request import RequestResponse
from app.temporal.workflows import ApprovalWorkflow

router = APIRouter(prefix="/api/customer", tags=["Customer"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/requests", response_model=RequestResponse)
async def submit_request(
    customer_name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Save the file and database record (Same as before)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_request = CustomerRequest(
        customer_name=customer_name,
        description=description,
        file_path=file_path,
        status="PENDING"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # 2. TEMPORAL INTEGRATION: Generate a unique ID and save it to the DB
    temporal_workflow_id = f"approval-workflow-{new_request.id}"
    new_request.temporal_workflow_id = temporal_workflow_id
    db.commit()

    # 3. TEMPORAL INTEGRATION: Connect to Temporal and start the workflow
    client = await Client.connect("localhost:7233")
    await client.start_workflow(
        ApprovalWorkflow.run,
        new_request.id,  # Pass the database ID into the workflow
        id=temporal_workflow_id,
        task_queue="approval-task-queue"
    )
    
    return new_request

@router.get("/requests", response_model=List[RequestResponse])
def get_all_customer_requests(db: Session = Depends(get_db)):
    return db.query(CustomerRequest).order_by(CustomerRequest.created_at.desc()).all()