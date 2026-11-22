from pydantic import BaseModel, Field


class ExpenseIn(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0, description="Amount in TRY.")
    category: str = "other"


class Expense(ExpenseIn):
    id: int


class ExpenseTotal(BaseModel):
    count: int
    total: float


class CategorySummary(BaseModel):
    category: str
    count: int
    total: float


class HealthStatus(BaseModel):
    status: str
