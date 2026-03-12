import pytest

from mcp_servers.sql_server.safety import assert_read_only_sql


def test_allows_select():
    assert_read_only_sql("SELECT * FROM sales")


@pytest.mark.parametrize("query", [
    "DELETE FROM sales",
    "UPDATE sales SET revenue=0",
    "DROP TABLE sales",
    "SELECT * FROM sales; DROP TABLE x",
])
def test_rejects_dangerous_sql(query: str):
    with pytest.raises(ValueError):
        assert_read_only_sql(query)
