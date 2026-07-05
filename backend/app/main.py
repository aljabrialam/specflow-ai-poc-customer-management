import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

DB_PATH = os.getenv("DATABASE_PATH", "customers.db")
DB_FILE = Path(DB_PATH)
DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            company TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


init_db()


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    company: str

    @field_validator("name", "email", "phone", "company")
    @classmethod
    def validate_required_fields(cls, value: str, info: Any) -> str:
        if not value or not value.strip():
            raise ValueError(f"{info.field_name} is required")
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip()
        if "@" not in value or "." not in value:
            raise ValueError("email must be a valid email address")
        return value


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int


app = FastAPI(title="Customer Management Portal API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/customers", response_model=list[Customer])
def list_customers(search: str | None = Query(default=None, description="Search customers by name, email, or company")) -> list[dict[str, Any]]:
    with get_connection() as connection:
        if search:
            term = f"%{search.strip()}%"
            rows = connection.execute(
                "SELECT id, name, email, phone, company FROM customers WHERE name LIKE ? OR email LIKE ? OR company LIKE ? ORDER BY id DESC",
                (term, term, term),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT id, name, email, phone, company FROM customers ORDER BY id DESC"
            ).fetchall()
    return [dict(row) for row in rows]


@app.post("/api/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate) -> dict[str, Any]:
    with get_connection() as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO customers (name, email, phone, company) VALUES (?, ?, ?, ?)",
                (customer.name, customer.email, customer.phone, customer.company),
            )
            connection.commit()
        except sqlite3.IntegrityError as exc:
            raise HTTPException(status_code=409, detail="Customer with this email already exists") from exc

        customer_id = cursor.lastrowid
        row = connection.execute(
            "SELECT id, name, email, phone, company FROM customers WHERE id = ?",
            (customer_id,),
        ).fetchone()
    return dict(row)


@app.put("/api/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerCreate) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE customers SET name = ?, email = ?, phone = ?, company = ? WHERE id = ?",
            (customer.name, customer.email, customer.phone, customer.company, customer_id),
        )
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        try:
            row = connection.execute(
                "SELECT id, name, email, phone, company FROM customers WHERE id = ?",
                (customer_id,),
            ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise HTTPException(status_code=409, detail="Customer with this email already exists") from exc
    return dict(row)


@app.delete("/api/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int) -> Response:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
