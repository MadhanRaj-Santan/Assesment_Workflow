from temporalio import activity
from app.database import SessionLocal
from app.models.request import CustomerRequest

@activity.defn
def update_request_status(data: dict) -> str:
    request_id = data["request_id"]
    new_status = data["status"]
    
    # We open a new database session manually for the background task
    db = SessionLocal()
    try:
        req = db.query(CustomerRequest).filter(CustomerRequest.id == request_id).first()
        if not req:
            raise Exception(f"Request {request_id} not found")
        
        # Update the status and boolean result
        req.status = new_status
        req.approval_result = (new_status == "APPROVED")
        db.commit()
        return f"Status updated to {new_status}"
    finally:
        db.close()