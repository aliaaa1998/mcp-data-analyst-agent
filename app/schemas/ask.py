from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=1000)
    allowed_tools: list[str] | None = None
    generate_markdown: bool = True


class Source(BaseModel):
    type: str
    name: str


class ChartRef(BaseModel):
    chart_id: str
    title: str
    path: str


class ToolCall(BaseModel):
    server: str
    tool: str
    status: str


class AskResponse(BaseModel):
    question: str
    executive_summary: str
    key_findings: list[str]
    methodology: list[str]
    assumptions: list[str]
    sources: list[Source]
    charts: list[ChartRef]
    warnings: list[str]
    model: str
    tool_calls: list[ToolCall]
    usage: dict | None = None
    request_id: str
    markdown_summary: str | None = None
