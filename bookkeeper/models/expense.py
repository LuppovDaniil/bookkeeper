"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: str = datetime.now().strftime("%H:%M, %d/%m/%Y")
    added_date: str = datetime.now().strftime("%H:%M, %d/%m/%Y")
    comment: str = ''
    pk: int = 0
