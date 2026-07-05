import importlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.main as main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "customers.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    importlib.reload(main)
    main.init_db()
    with TestClient(main.app) as test_client:
        yield test_client


def test_create_and_list_customer(client):
    response = client.post(
        "/api/customers",
        json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "phone": "+1-555-1234",
            "company": "ACME",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Ada Lovelace"
    assert body["email"] == "ada@example.com"

    list_response = client.get("/api/customers")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_duplicate_email_returns_conflict(client):
    client.post(
        "/api/customers",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "+1-555-0000",
            "company": "Contoso",
        },
    )

    duplicate = client.post(
        "/api/customers",
        json={
            "name": "Alice 2",
            "email": "alice@example.com",
            "phone": "+1-555-0001",
            "company": "Contoso",
        },
    )

    assert duplicate.status_code == 409


def test_update_customer_updates_existing_record(client):
    created = client.post(
        "/api/customers",
        json={
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "phone": "+1-555-5678",
            "company": "Contoso",
        },
    )
    customer_id = created.json()["id"]

    updated = client.put(
        f"/api/customers/{customer_id}",
        json={
            "name": "Grace Hopper",
            "email": "grace.updated@example.com",
            "phone": "+1-555-5678",
            "company": "Contoso",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["email"] == "grace.updated@example.com"

    delete_response = client.delete(f"/api/customers/{customer_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/customers")
    assert list_response.json() == []


def test_update_customer_returns_not_found_for_missing_record(client):
    response = client.put(
        "/api/customers/999",
        json={
            "name": "Missing",
            "email": "missing@example.com",
            "phone": "+1-555-9999",
            "company": "Ghost",
        },
    )

    assert response.status_code == 404


def test_delete_customer_removes_record(client):
    created = client.post(
        "/api/customers",
        json={
            "name": "Linus Torvalds",
            "email": "linus@example.com",
            "phone": "+1-555-4321",
            "company": "Linux",
        },
    )
    customer_id = created.json()["id"]

    delete_response = client.delete(f"/api/customers/{customer_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/customers")
    assert list_response.json() == []


def test_delete_customer_returns_not_found_for_missing_record(client):
    response = client.delete("/api/customers/999")
    assert response.status_code == 404


def test_validation_rejects_invalid_payload(client):
    response = client.post(
        "/api/customers",
        json={
            "name": "",
            "email": "not-an-email",
            "phone": "",
            "company": "",
        },
    )

    assert response.status_code == 422


def pytest_configure(config: Any) -> None:
    config.addinivalue_line(
        "markers",
        "api: mark tests as API tests",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: Any) -> Any:
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        test_result = {
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": round(report.duration, 3),
        }
        results_path = Path(__file__).resolve().parent / "test-results.json"
        existing_results: list[dict[str, Any]] = []
        if results_path.exists():
            existing_results = json.loads(results_path.read_text())
        existing_results = [r for r in existing_results if r.get("nodeid") != test_result["nodeid"]]
        existing_results.append(test_result)
        results_path.write_text(json.dumps(existing_results, indent=2))
