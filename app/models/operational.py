from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class QuestionRun(Base):
    __tablename__ = "question_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    question: Mapped[str] = mapped_column(Text)
    response_json: Mapped[dict] = mapped_column(JSON)
    model: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GeneratedChart(Base):
    __tablename__ = "generated_charts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_run_id: Mapped[int] = mapped_column(ForeignKey("question_runs.id"), index=True)
    chart_id: Mapped[str] = mapped_column(String(128), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ToolCallLog(Base):
    __tablename__ = "tool_call_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_run_id: Mapped[int | None] = mapped_column(ForeignKey("question_runs.id"), nullable=True)
    server: Mapped[str] = mapped_column(String(64))
    tool: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32))
    latency_ms: Mapped[int] = mapped_column(Integer)
    output_summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
