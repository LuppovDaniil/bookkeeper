from dataclasses import dataclass


@dataclass
class Budget:

    budget: int = 0
    remaining_sum: int = 0
    pk: int = 0

    def register_purchase(self, cost):
        self.remaining_sum -= cost


