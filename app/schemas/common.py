from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ToolRegistryResponse(BaseModel):
    servers: dict[str, list[str]]
