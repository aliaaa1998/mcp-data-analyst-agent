from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from mcp_servers.analytics_server.analytics import (
    calculate_growth,
    compare_periods,
    detect_anomalies,
    summarize_dataset,
)

app = FastAPI(title="MCP Analytics Server")


class InvokeRequest(BaseModel):
    tool: str
    arguments: dict = Field(default_factory=dict)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/tools")
def tools() -> dict:
    return {"tools": ["calculate_growth", "compare_periods", "summarize_dataset", "detect_anomalies"]}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict:
    args = payload.arguments
    try:
        if payload.tool == "calculate_growth":
            return {"ok": True, "result": calculate_growth(args["values"])}
        if payload.tool == "compare_periods":
            return {"ok": True, "result": compare_periods(args["current"], args["previous"])}
        if payload.tool == "summarize_dataset":
            return {"ok": True, "result": summarize_dataset(args["rows"])}
        if payload.tool == "detect_anomalies":
            return {"ok": True, "result": detect_anomalies(args["values"], args.get("threshold_std", 2.0))}
        raise ValueError("Unknown tool")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
