from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational import GeneratedChart, QuestionRun, ToolCallLog
from app.schemas.ask import AskResponse


class QuestionRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, response: AskResponse) -> QuestionRun:
        run = QuestionRun(
            request_id=response.request_id,
            question=response.question,
            response_json=response.model_dump(mode="json"),
            model=response.model,
        )
        self.db.add(run)
        self.db.flush()

        for chart in response.charts:
            self.db.add(
                GeneratedChart(
                    question_run_id=run.id,
                    chart_id=chart.chart_id,
                    title=chart.title,
                    path=chart.path,
                )
            )
        for call in response.tool_calls:
            self.db.add(
                ToolCallLog(
                    question_run_id=run.id,
                    server=call.server,
                    tool=call.tool,
                    status=call.status,
                    latency_ms=0,
                    output_summary="",
                )
            )
        self.db.commit()
        self.db.refresh(run)
        return run

    def list_recent(self, limit: int = 20) -> list[QuestionRun]:
        stmt = select(QuestionRun).order_by(QuestionRun.id.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())
