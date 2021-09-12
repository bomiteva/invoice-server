from starlette.testclient import TestClient

from app.main import app
# Use the TestClient object the same way as you do with requests. Allows to send HTTP/1.1 requests easily.
client = TestClient(app)


def test_get_invoice():
    """Tests GET endpoint with buyer Axtronics and target type - xml"""
    response = client.get("/invoice/1630952140/Axtronics?target_type=xml")
    assert response.status_code == 200
    assert response.text == "<root><invoice><buyer>Axtronics</buyer><image_name>f1.png</image_name><invoice_due_date>2020-10-23</invoice_due_date><invoice_number>AA-C56790</invoice_number><invoice_amount>305.45</invoice_amount><invoice_currency>USD</invoice_currency><invoice_status>NEW</invoice_status><supplier>Silver Logistics</supplier></invoice></root>"


def test_get_invalid_type_invoice():
    """Tests GET endpoint with buyer Axtronics and invalid target type - txt"""
    response = client.get("/invoice/1630952140/Axtronics?target_type=txt")
    assert response.status_code == 422


def test_post_invoice():
    """Tests POST endpoint with invoice file"""
    response = client.post("/invoice", files={"file": ("invoice.csv", open("invoices.csv", "rb"), "text/csv")})
    assert response.status_code == 200
    assert "upload_id" in response.json()


def test_post_invalid_invoice():
    """Tests POST endpoint with invalid invoice file"""
    response = client.post("/invoice", files={"file": ("invoice.html", open("invoices.csv", "rb"), "text/html")})
    assert response.status_code == 422


def test_invalid_endpoint():
    """Tests server with invalid endpoint"""
    response = client.get("/invoice/99")
    assert response.status_code == 404
