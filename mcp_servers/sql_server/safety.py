import re

FORBIDDEN_PATTERNS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bCREATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bCOPY\b",
    r";",
]


def assert_read_only_sql(sql: str) -> None:
    statement = sql.strip().upper()
    if not statement.startswith("SELECT") and not statement.startswith("WITH"):
        raise ValueError("Only SELECT/CTE queries are allowed")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, statement):
            raise ValueError(f"Forbidden SQL pattern matched: {pattern}")
