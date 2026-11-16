from temporalio import workflow
from datetime import timedelta

# Temporal runs workflows in a secure sandbox. We must tell it to allow our database imports.
with workflow.unsafe.imports_passed_through():
    from app.temporal.activities import update_request_status

@workflow.defn
class ApprovalWorkflow:
    def __init__(self) -> None:
        # State variable to hold the decision once it arrives
        self.decision = None

    @workflow.signal
    async def submit_decision(self, decision: str) -> None:
        # This function is called externally (from FastAPI) to inject data into the running workflow
        self.decision = decision

    @workflow.run
    async def run(self, request_id: int) -> bool:
        # 1. Pause execution completely until self.decision is no longer None
        await workflow.wait_condition(lambda: self.decision is not None)
        
        # 2. Once a decision is received, execute the database update activity
        await workflow.execute_activity(
            update_request_status,
            {"request_id": request_id, "status": self.decision},
            start_to_close_timeout=timedelta(minutes=1),
        )
        
        # 3. Return the final result
        return self.decision == "APPROVED"