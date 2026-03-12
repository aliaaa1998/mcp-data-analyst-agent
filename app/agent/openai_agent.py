from __future__ import annotations

import json
import logging
from typing import Any

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.ask import AskResponse, ChartRef, Source, ToolCall
from app.services.mcp_client import MCPClient

logger = logging.getLogger(__name__)


class OpenAIAnalystAgent:
    def __init__(self, mcp_client: MCPClient):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.mcp_client = mcp_client

    async def answer_question(self, question: str, allowed_tools: list[str] | None = None) -> AskResponse:
        tool_registry = await self.mcp_client.list_tools()
        model_tools = self._build_model_tools(tool_registry, allowed_tools)
        tool_calls: list[ToolCall] = []
        methodology: list[str] = []

        response = await self.client.responses.create(
            model=self.settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior business data analyst. Use tools when needed. "
                        "Return final output as JSON with keys: executive_summary, key_findings, "
                        "methodology, assumptions, sources, warnings, charts"
                    ),
                },
                {"role": "user", "content": question},
            ],
            tools=model_tools,
            tool_choice="auto",
            temperature=0.2,
        )

        while True:
            function_calls = [i for i in response.output if i.type == "function_call"]
            if not function_calls:
                break

            outputs = []
            for fc in function_calls:
                args = json.loads(fc.arguments)
                server, tool = fc.name.split("__", 1)
                result = await self.mcp_client.invoke(server, tool, args)
                outputs.append({"type": "function_call_output", "call_id": fc.call_id, "output": result.output})
                tool_calls.append(ToolCall(server=server, tool=tool, status=result.status))
                methodology.append(f"Called {server}.{tool}")
            response = await self.client.responses.create(
                model=self.settings.openai_model,
                previous_response_id=response.id,
                input=outputs,
            )

        raw_text = response.output_text
        data = self._coerce_response(raw_text, question)
        charts = [ChartRef(**c) for c in data.get("charts", [])]
        return AskResponse(
            question=question,
            executive_summary=data.get("executive_summary", "No summary produced."),
            key_findings=data.get("key_findings", []),
            methodology=data.get("methodology", methodology),
            assumptions=data.get("assumptions", []),
            sources=[Source(**s) for s in data.get("sources", [])],
            charts=charts,
            warnings=data.get("warnings", []),
            model=self.settings.openai_model,
            tool_calls=tool_calls,
            usage=getattr(response, "usage", None),
            request_id=response.id,
            markdown_summary=self._to_markdown(data),
        )

    def _build_model_tools(self, tool_registry: dict[str, list[str]], allowed_tools: list[str] | None) -> list[dict]:
        tools: list[dict] = []
        allow = set(allowed_tools) if allowed_tools else None
        for server, server_tools in tool_registry.items():
            for tool in server_tools:
                qualified = f"{server}__{tool}"
                if allow and qualified not in allow:
                    continue
                tools.append(
                    {
                        "type": "function",
                        "name": qualified,
                        "description": f"MCP tool {tool} from {server}",
                        "parameters": {"type": "object", "additionalProperties": True},
                    }
                )
        return tools

    @staticmethod
    def _coerce_response(raw_text: str, question: str) -> dict[str, Any]:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            logger.warning("model_non_json_output")
            return {
                "executive_summary": raw_text[:500],
                "key_findings": [raw_text[:200]],
                "methodology": ["Model answered without strict JSON."],
                "assumptions": ["Fallback parser used."],
                "sources": [{"type": "question", "name": question}],
                "warnings": ["The model did not return strict JSON."],
                "charts": [],
            }

    @staticmethod
    def _to_markdown(data: dict[str, Any]) -> str:
        findings = "\n".join(f"- {item}" for item in data.get("key_findings", []))
        return f"## Executive Summary\n{data.get('executive_summary', '')}\n\n## Key Findings\n{findings}"
