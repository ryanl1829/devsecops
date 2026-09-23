"""Integration tests for web_service.

These hit a *real* Ollama instance (no mocking of the ollama client):
in CI, OLLAMA_URL points at the `ollama` service container and the
OLLAMA_MODEL has already been pulled into it before pytest runs. If
you run this locally, point OLLAMA_URL at an Ollama instance that
already has OLLAMA_MODEL available, or the /api/status and /chat
tests will fail against an empty or unreachable server.
"""


def test_api_status_reports_ollama_available(client):
    response = client.get("/api/status")
    assert response.status_code == 200

    body = response.get_json()
    assert body["status"] == "ok"
    assert body["ollama"]["status"] == "ok"
    assert body["ollama"]["model_available"] is True


def test_chat_with_empty_prompt_short_circuits(client):
    # No prompt -> no call to Ollama, just the fallback message.
    response = client.post("/chat", data={"prompt": ""})
    assert response.status_code == 200
    assert b"No message provided." in response.data


def test_chat_returns_a_real_model_response(client):
    response = client.post(
        "/chat", data={"prompt": "Reply with a short, one-sentence greeting."}
    )
    assert response.status_code == 200
    # Wording from a real model isn't deterministic, so just confirm
    # it took the real-answer branch rather than the empty-prompt one.
    assert b"No message provided." not in response.data


def test_api_visits_increments_monotonically(client):
    first = client.get("/api/visits").get_json()["visits"]
    second = client.get("/api/visits").get_json()["visits"]
    assert second == first + 1
