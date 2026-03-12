from fastapi import FastAPI

from app.api.v1.routes import router
from app.core.logging import setup_logging

setup_logging()
app = FastAPI(title="MCP Data Analyst Agent", version="1.0.0")
app.include_router(router)
