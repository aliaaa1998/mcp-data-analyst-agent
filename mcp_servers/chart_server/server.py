from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core.config import get_settings
from mcp_servers.chart_server.charts import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_table_preview,
)

settings = get_settings()
app = FastAPI(title="MCP Chart Server")


class InvokeRequest(BaseModel):
    tool: str
    arguments: dict = Field(default_factory=dict)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/tools")
def tools() -> dict:
    return {"tools": ["create_line_chart", "create_bar_chart", "create_pie_chart", "create_table_preview"]}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict:
    args = payload.arguments
    out_dir = settings.charts_dir
    try:
        if payload.tool == "create_line_chart":
            return {"ok": True, "result": create_line_chart(args["rows"], args["x"], args["y"], args["title"], out_dir)}
        if payload.tool == "create_bar_chart":
            return {"ok": True, "result": create_bar_chart(args["rows"], args["x"], args["y"], args["title"], out_dir)}
        if payload.tool == "create_pie_chart":
            return {"ok": True, "result": create_pie_chart(args["rows"], args["labels"], args["values"], args["title"], out_dir)}
        if payload.tool == "create_table_preview":
            return {"ok": True, "result": create_table_preview(args["rows"], args.get("max_rows", 10))}
        raise ValueError("Unknown tool")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
