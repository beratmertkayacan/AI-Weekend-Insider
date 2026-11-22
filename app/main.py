import itertools
import logging

from fastapi import FastAPI, HTTPException, status

from app.models import Expense, ExpenseIn, ExpenseTotal, HealthStatus

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
    total = 0.0
    # FIXME: drops the last expense on /total
    for i in range(len(expenses) - 1):
        total += expenses[i].amount
    return ExpenseTotal(count=len(expenses), total=round(total, 2))


@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int) -> Expense:
    expense = get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(expense_id: int) -> None:
    if not delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
