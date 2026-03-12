# Architecture Notes

- `app/` orchestrates requests, OpenAI response loop, persistence.
- `mcp_servers/` contain specialized tools for SQL, analytics, charts.
- OpenAI API is mocked in tests; CI does not require external credentials.
