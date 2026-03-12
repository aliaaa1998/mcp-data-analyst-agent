import logging

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, inspect, text

from app.core.config import get_settings
from mcp_servers.sql_server.safety import assert_read_only_sql

settings = get_settings()
app = FastAPI(title="MCP SQL Server")
logger = logging.getLogger(__name__)
engine = create_engine(settings.database_url, pool_pre_ping=True)


class InvokeRequest(BaseModel):
    tool: str
    arguments: dict = Field(default_factory=dict)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/tools")
def tools() -> dict:
    return {"tools": ["list_tables", "describe_table", "run_sql_readonly"]}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict:
    try:
        if payload.tool == "list_tables":
            insp = inspect(engine)
            return {"ok": True, "result": {"tables": insp.get_table_names()}}
        if payload.tool == "describe_table":
            table = payload.arguments.get("table")
            if not table:
                raise ValueError("table is required")
            insp = inspect(engine)
            columns = insp.get_columns(table)
            return {"ok": True, "result": {"columns": columns}}
        if payload.tool == "run_sql_readonly":
            sql = payload.arguments.get("sql", "")
            limit = int(payload.arguments.get("limit", 200))
            assert_read_only_sql(sql)
            query = f"SELECT * FROM ({sql}) AS subq LIMIT {min(limit, 500)}"
            with engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            logger.info("sql_query_executed", extra={"rows": len(df)})
            return {"ok": True, "result": {"rows": df.to_dict(orient="records"), "count": len(df)}}
        raise ValueError("Unknown tool")
    except Exception as exc:  # noqa: BLE001
        logger.exception("sql_tool_error")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
