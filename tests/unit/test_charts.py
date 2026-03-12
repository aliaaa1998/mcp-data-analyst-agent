from pathlib import Path

from mcp_servers.chart_server.charts import create_bar_chart


def test_create_bar_chart(tmp_path: Path):
    rows = [{"month": "2025-01", "revenue": 10}, {"month": "2025-02", "revenue": 20}]
    output = create_bar_chart(rows, "month", "revenue", "Revenue", str(tmp_path))
    assert (tmp_path / f"{output['chart_id']}.png").exists()
