from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)


@dataclass
class MCPToolResult:
    server: str
    tool: str
    status: str
    output: dict
    latency_ms: int


class MCPClient:
    def __init__(self, server_urls: dict[str, str], timeout_seconds: int = 30) -> None:
        self.server_urls = server_urls
        self.timeout_seconds = timeout_seconds

    async def list_tools(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            for server, base_url in self.server_urls.items():
                response = await client.get(f"{base_url}/tools")
                response.raise_for_status()
                out[server] = response.json()["tools"]
        return out

    async def invoke(self, server: str, tool: str, arguments: dict) -> MCPToolResult:
        if server not in self.server_urls:
            raise ValueError(f"Unknown server: {server}")
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                f"{self.server_urls[server]}/invoke",
                json={"tool": tool, "arguments": arguments},
            )
            payload = response.json()
        latency = int((time.perf_counter() - start) * 1000)
        status = "success" if response.status_code == 200 and payload.get("ok", False) else "error"
        logger.info(
            "mcp_tool_call",
            extra={"server": server, "tool": tool, "status": status, "latency_ms": latency},
        )
        return MCPToolResult(server=server, tool=tool, status=status, output=payload, latency_ms=latency)
