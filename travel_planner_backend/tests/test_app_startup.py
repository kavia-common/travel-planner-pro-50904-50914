# PUBLIC_INTERFACE
def test_app_import_and_health():
    """Ensure the FastAPI app imports, OpenAPI schema generates, and health check returns OK."""
    from fastapi.testclient import TestClient
    from src.api.main import app

    # Generate OpenAPI schema to surface any Pydantic recursion during typing inspection
    schema = app.openapi()
    assert isinstance(schema, dict)
    assert schema.get("openapi")

    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("message") == "Healthy"
