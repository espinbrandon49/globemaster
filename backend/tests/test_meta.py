def test_health_endpoint(client):
    resp = client.get("/meta/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"status": "ok"}


def test_ping_endpoint(client):
    resp = client.get("/meta/ping")
    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == "pong"


def test_categories_endpoint(client):
    resp = client.get("/meta/categories")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)

