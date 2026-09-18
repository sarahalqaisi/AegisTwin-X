from fastapi.testclient import TestClient

from aegistwin.main import app


client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "healthy"


def test_brand_logo_is_available_and_used_by_dashboard():
    dashboard = client.get("/")
    logo = client.get("/static/aegistwin-logo.png")
    assert dashboard.status_code == 200
    assert "aegistwin-logo.png" in dashboard.text
    assert logo.status_code == 200
    assert logo.headers["content-type"] == "image/png"


def test_demo_analysis_blocks_insecure_change():
    response = client.post("/api/analyses/demo?variant=insecure")
    assert response.status_code == 200
    assert response.json()["decision"] == "BLOCK"


def test_secure_invoice_endpoint_enforces_ownership():
    response = client.get("/api/twinshop/invoices/inv-2001", headers={"X-Demo-User": "customer-alex"})
    assert response.status_code == 403
