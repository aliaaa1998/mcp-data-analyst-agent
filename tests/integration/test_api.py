from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


def _fake_db():
    class Dummy:
        def close(self):
            pass

    yield Dummy()


def test_healthz():
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200


def test_ask_mocked(monkeypatch):
    from app.api.v1 import routes

    async def fake_answer(self, question, allowed_tools=None):
        from app.schemas.ask import AskResponse

        return AskResponse(
            question=question,
            executive_summary="Summary",
            key_findings=["A"],
            methodology=["Used tools"],
            assumptions=[],
            sources=[{"type": "table", "name": "sales"}],
            charts=[],
            warnings=[],
            model="test-model",
            tool_calls=[{"server": "sql", "tool": "run_sql_readonly", "status": "success"}],
            usage=None,
            request_id="req_test",
            markdown_summary="ok",
        )

    monkeypatch.setattr(routes.OpenAIAnalystAgent, "answer_question", fake_answer)
    monkeypatch.setattr(routes.QuestionRunRepository, "create", lambda self, response: None)
    app.dependency_overrides[get_db] = _fake_db

    client = TestClient(app)
    resp = client.post("/api/v1/ask", json={"question": "Top products by revenue?"})
    assert resp.status_code == 200
    assert resp.json()["executive_summary"] == "Summary"
    app.dependency_overrides.clear()
