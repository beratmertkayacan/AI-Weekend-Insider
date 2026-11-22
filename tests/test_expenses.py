from typing import Any

import pytest
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


def test_update_expense_returns_updated_expense(client: TestClient) -> None:
    created = client.post("/expenses", json={"description": "Simit", "amount": 15})
    expense_id = created.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={"description": "Pide", "amount": 180.5, "category": "food"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": expense_id,
        "description": "Pide",
        "amount": 180.5,
        "category": "food",
    }


def test_update_expense_is_persisted(client: TestClient) -> None:
    created = client.post("/expenses", json={"description": "Simit", "amount": 15})
    expense_id = created.json()["id"]
    client.put(
        f"/expenses/{expense_id}",
        json={"description": "Pide", "amount": 180.5, "category": "food"},
    )

    fetched = client.get(f"/expenses/{expense_id}")
    assert fetched.json() == {
        "id": expense_id,
        "description": "Pide",
        "amount": 180.5,
        "category": "food",
    }
    assert len(client.get("/expenses").json()) == 1


def test_update_expense_keeps_same_id_and_other_expenses_untouched(client: TestClient) -> None:
    first = client.post("/expenses", json={"description": "Simit", "amount": 15}).json()
    second = client.post(
        "/expenses", json={"description": "Ferry", "amount": 40, "category": "transport"}
    ).json()

    response = client.put(
        f"/expenses/{first['id']}", json={"description": "Pide", "amount": 180.5}
    )

    assert response.status_code == 200
    assert response.json()["id"] == first["id"]
    assert client.get(f"/expenses/{second['id']}").json() == second


def test_update_expense_resets_omitted_category_to_default(client: TestClient) -> None:
    created = client.post(
        "/expenses", json={"description": "Pide", "amount": 180, "category": "food"}
    )
    expense_id = created.json()["id"]

    response = client.put(f"/expenses/{expense_id}", json={"description": "Pide", "amount": 180})

    assert response.status_code == 200
    assert response.json()["category"] == "other"


def test_update_unknown_expense_returns_404(client: TestClient) -> None:
    response = client.put("/expenses/999", json={"description": "Pide", "amount": 180})

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}
    assert client.get("/expenses").json() == []


def test_update_expense_rejects_invalid_body(client: TestClient) -> None:
    created = client.post("/expenses", json={"description": "Simit", "amount": 15})
    original = created.json()
    expense_id = original["id"]

    empty_description = client.put(
        f"/expenses/{expense_id}", json={"description": "", "amount": 10}
    )
    zero_amount = client.put(f"/expenses/{expense_id}", json={"description": "x", "amount": 0})

    assert empty_description.status_code == 422
    assert zero_amount.status_code == 422
    assert client.get(f"/expenses/{expense_id}").json() == original


@pytest.mark.parametrize(
    "body",
    [
        {"description": "x" * 201, "amount": 1},
        {"amount": 1},
        {"description": "x"},
        {"description": "x", "amount": -1},
    ],
    ids=["description_too_long", "missing_description", "missing_amount", "negative_amount"],
)
def test_update_expense_rejects_invalid_body_cases(
    client: TestClient, body: dict[str, Any]
) -> None:
    original = client.post("/expenses", json={"description": "Simit", "amount": 15}).json()

    response = client.put(f"/expenses/{original['id']}", json=body)

    assert response.status_code == 422
    assert client.get(f"/expenses/{original['id']}").json() == original


def test_update_expense_accepts_description_of_200_chars(client: TestClient) -> None:
    expense_id = client.post("/expenses", json={"description": "Simit", "amount": 15}).json()["id"]
    description = "x" * 200

    response = client.put(f"/expenses/{expense_id}", json={"description": description, "amount": 1})

    assert response.status_code == 200
    assert response.json()["description"] == description


def test_update_expense_rejects_non_integer_id(client: TestClient) -> None:
    response = client.put("/expenses/abc", json={"description": "Pide", "amount": 180})

    assert response.status_code == 422
