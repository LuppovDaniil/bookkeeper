import pytest

from bookkeeper.models.budget import Budget

budget_test = Budget()


def test_budget_eq():
    budget_test.register_purchase(10)
    assert budget_test == Budget(budget=0, cur_sum=10)
