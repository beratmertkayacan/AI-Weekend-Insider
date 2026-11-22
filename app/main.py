import itertools
import logging

from fastapi import FastAPI, HTTPException, status

from app.models import (
    CategorySummary,
    Expense,
    ExpenseIn,
    ExpenseTotal,
    HealthStatus,
)

logger = logging.getLogger(__name__)

app = FastAPI(title="expense-api", version="0.1.0")

_expenses: dict[int, Expense] = {}
_ids = itertools.count(1)


def reset_storage() -> None:
    global _ids
    _expenses.clear()
    _ids = itertools.count(1)


def save_expense(data: ExpenseIn) -> Expense:
    expense = Expense(id=next(_ids), **data.model_dump())
    _expenses[expense.id] = expense
    return expense


def list_expenses(category: str | None = None) -> list[Expense]:
    expenses = list(_expenses.values())
    if category is not None:
        expenses = [expense for expense in expenses if expense.category == category]
    return expenses


def get_expense(expense_id: int) -> Expense | None:
    return _expenses.get(expense_id)


def delete_expense(expense_id: int) -> bool:
    return _expenses.pop(expense_id, None) is not None


def update_expense(expense_id: int, data: ExpenseIn) -> Expense | None:
    if expense_id not in _expenses:
        return None
    expense = Expense(id=expense_id, **data.model_dump())
    _expenses[expense_id] = expense
    return expense


@app.get("/health")
def read_health() -> HealthStatus:
    return HealthStatus(status="ok")


@app.get("/expenses")
def read_expenses(category: str | None = None) -> list[Expense]:
    return list_expenses(category)


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseIn) -> Expense:
    expense = save_expense(data)
    logger.info("created expense %s", expense.id)
    return expense


@app.get("/expenses/total")
def read_total() -> ExpenseTotal:
    expenses = list_expenses()
    total = sum(expense.amount for expense in expenses)
    return ExpenseTotal(count=len(expenses), total=round(total, 2))


@app.get("/expenses/summary")
def read_summary() -> list[CategorySummary]:
    counts: dict[str, int] = {}
    sums: dict[str, float] = {}
    for expense in list_expenses():
        counts[expense.category] = counts.get(expense.category, 0) + 1
        sums[expense.category] = sums.get(expense.category, 0.0) + expense.amount
    return [
        CategorySummary(category=name, count=counts[name], total=round(sums[name], 2))
        for name in sorted(counts)
    ]


@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int) -> Expense:
    expense = get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/expenses/{expense_id}")
def replace_expense(expense_id: int, data: ExpenseIn) -> Expense:
    expense = update_expense(expense_id, data)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    logger.info("updated expense %s", expense_id)
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(expense_id: int) -> None:
    if not delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
