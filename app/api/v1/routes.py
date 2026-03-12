from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.agent.openai_agent import OpenAIAnalystAgent
from app.core.config import get_settings
from app.db.session import get_db
from app.repositories.question_runs import QuestionRunRepository
from app.schemas.ask import AskRequest, AskResponse
from app.schemas.common import HealthResponse, ToolRegistryResponse
from app.services.data_loader import load_sample_data
from app.services.mcp_client import MCPClient

router = APIRouter()
settings = get_settings()


def mcp_client() -> MCPClient:
    return MCPClient(
        {
            "sql": settings.mcp_sql_server_url,
            "analytics": settings.mcp_analytics_server_url,
            "charts": settings.mcp_chart_server_url,
        }
    )


@router.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/readyz", response_model=HealthResponse)
def readyz(db: Session = Depends(get_db)) -> HealthResponse:
    db.execute(text("SELECT 1"))
    return HealthResponse(status="ready")


@router.post("/api/v1/ask", response_model=AskResponse)
async def ask(payload: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    agent = OpenAIAnalystAgent(mcp_client())
    response = await agent.answer_question(payload.question, payload.allowed_tools)
    QuestionRunRepository(db).create(response)
    if not payload.generate_markdown:
        response.markdown_summary = None
    return response


@router.get("/api/v1/questions/history")
def history(db: Session = Depends(get_db)) -> list[dict]:
    runs = QuestionRunRepository(db).list_recent()
    return [{"id": r.id, "request_id": r.request_id, "question": r.question, "created_at": r.created_at} for r in runs]


@router.get("/api/v1/tools", response_model=ToolRegistryResponse)
async def tools() -> ToolRegistryResponse:
    return ToolRegistryResponse(servers=await mcp_client().list_tools())


@router.post("/api/v1/demo/load-data")
def demo_load_data(db: Session = Depends(get_db)) -> dict:
    counts = load_sample_data(db)
    return {"status": "loaded", "counts": counts}


@router.get("/api/v1/charts/{chart_id}")
def get_chart(chart_id: str) -> FileResponse:
    path = Path(settings.charts_dir) / f"{chart_id}.png"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    return FileResponse(path)
