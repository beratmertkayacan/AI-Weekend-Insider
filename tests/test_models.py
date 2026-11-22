import pytest
from pydantic import ValidationError

from app.models import ExpenseIn


def test_amount_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        ExpenseIn(description="Refund?", amount=0)


def test_description_must_not_be_empty() -> None:
    with pytest.raises(ValidationError):
        ExpenseIn(description="", amount=10)


def test_category_defaults_to_other() -> None:
    assert ExpenseIn(description="Bus ticket", amount=20).category == "other"
