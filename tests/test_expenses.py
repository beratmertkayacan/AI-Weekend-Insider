from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_get_and_delete_expense(client: TestClient) -> None:
    created = client.post("/expenses", json={"description": "Simit", "amount": 15})
    assert created.status_code == 201
    expense_id = created.json()["id"]

    fetched = client.get(f"/expenses/{expense_id}")
    assert fetched.json() == {
        "id": expense_id,
        "description": "Simit",
        "amount": 15.0,
        "category": "other",
    }

    assert client.delete(f"/expenses/{expense_id}").status_code == 204
    assert client.get(f"/expenses/{expense_id}").status_code == 404


def test_list_filters_by_category(client: TestClient) -> None:
    client.post("/expenses", json={"description": "Pide", "amount": 180, "category": "food"})
    client.post("/expenses", json={"description": "Ferry", "amount": 40, "category": "transport"})

    food = client.get("/expenses", params={"category": "food"}).json()
    assert [expense["description"] for expense in food] == ["Pide"]
    assert len(client.get("/expenses").json()) == 2


def test_total_sums_all_expenses(client: TestClient) -> None:
    for description, amount in [("Groceries", 12.5), ("Bus card", 7.25), ("Cinema", 30)]:
        client.post("/expenses", json={"description": description, "amount": amount})

    assert client.get("/expenses/total").json() == {"count": 3, "total": 49.75}
