from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.agent_execution import AgentExecution


class AgentTelemetryService:

    @staticmethod
    def log_execution(
        db: Session,
        *,
        user_id: str,
        workspace_id: str,
        agent_name: str,
        query: str,
        latency_ms: float,
        success: bool,
        start_time: datetime,
        end_time: datetime
    ):
        """
        Distributed Tracing Engine: Records granular performance latency spikes, 
        agent naming metadata states, and query parameters cleanly into database records.
        """
        try:
            execution_log = AgentExecution(
                id=str(uuid4()),
                user_id=user_id,
                workspace_id=workspace_id,
                agent_name=agent_name,
                query=query,
                latency_ms=int(latency_ms),
                success=success,
                start_time=start_time,
                end_time=end_time,
                created_at=datetime.now(timezone.utc)
            )
            db.add(execution_log)
            db.commit()
            db.refresh(execution_log)
            return execution_log
        except Exception as e:
            db.rollback()
            print(f"--- Warning: Failed to persist agent telemetry trace log: {e} ---")
            return None
