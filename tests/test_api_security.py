"""Pruebas de cabeceras de seguridad, CORS y protección por JWT en rutas sensibles."""


def test_root_health_response_shape(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "data" in body
    assert body["data"]["docs"] == "/docs"


def test_security_headers_are_present(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "content-security-policy" in response.headers
    assert "permissions-policy" in response.headers


def test_cors_preflight_allows_localhost_4200(client):
    response = client.options(
        "/usuarios",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization,Content-Type",
        },
    )
    assert response.status_code in (200, 204)
    assert response.headers["access-control-allow-origin"] == "http://localhost:4200"
    assert "authorization" in response.headers["access-control-allow-headers"].lower()


def test_protected_endpoint_requires_bearer_token(client):
    response = client.get("/usuarios")
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["error"]["message"]
