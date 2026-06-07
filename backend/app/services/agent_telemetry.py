import time
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.agent_execution import AgentExecution


class AgentTelemetry:
    """
    High-Precision Monotonic Stopwatch Manager: Captures isolated execution metrics, 
    latencies, and success states across individual sub-agent nodes.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.start = time.perf_counter()

    def finish(self) -> dict:
        """
        Calculates total microsecond performance delta turnarounds 
        and bundles an operational telemetry analytics report dictionary.
        """
        end = time.perf_counter()
        return {
            "agent_name": self.agent_name,
            "latency_ms": round((end - self.start) * 1000, 2),
            "success": True
        }


class AgentTelemetryService:
    """
    Distributed Tracing Persistence Engine: Commits fine-grained sub-agent 
    operational rows straight into your PostgreSQL tracking databases.
    """
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
        Writes transactional trace logs to the database, ensuring network faults 
        or table delays fail gracefully without interrupting central execution pipelines.
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
