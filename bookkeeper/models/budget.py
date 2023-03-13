"""
модуль с моделью бюджета
"""
from dataclasses import dataclass


@dataclass
class Budget:

    budget: int = 0
    cur_sum: int = 0
    pk: int = 0

    def register_purchase(self, cost):
        self.cur_sum += cost