import os
import sys

from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.add_botton import AddPurchase
from bookkeeper.view.budget import BudgetTable
from bookkeeper.view.categorry_botton import AddCategory
from bookkeeper.view.expense_table import ExpensesTable


class MainWindow(QtWidgets.QWidget):

    def __init__(self, cat_repo, exp_repo, budget_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.budget_repo = budget_repo

        self.AddPurchase = AddPurchase(self.cat_repo, self.exp_repo, self.budget_repo)
        self.ExpensesTable = ExpensesTable(self.cat_repo, self.exp_repo)
        self.BudgetTable = BudgetTable(self.budget_repo)
        self.AddCategory = AddCategory(self.cat_repo)

        self.ExpensesTable.fill_table()
        self.BudgetTable.fill_table()

        self.AddPurchase.data_updated.connect(self.ExpensesTable.fill_table)
        self.AddPurchase.data_updated.connect(self.BudgetTable.fill_table)

        self.AddPurchase.BudgetTable = self.BudgetTable
        self.BudgetTable.budget_updated.connect(self.AddPurchase.budget_update_response)

        self.AddCategory.category_table.data_updated.connect(self.AddPurchase.category_input.categories_edited_response)

        self.ExpensesTable.fill_table()
        self.BudgetTable.fill_table()

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.ExpensesTable)
        self.vbox.addWidget(self.BudgetTable)
        self.vbox.addWidget(self.AddPurchase)
        self.vbox.addWidget(self.AddCategory)
        self.setLayout(self.vbox)


if __name__ == '__main__':

    cwd = os.getcwd()

    db_file = os.path.join(cwd, 'bookkeeper', 'repository', 'project_db.db')

    cat_repo = SqliteRepository(db_file=db_file, cls=Category)
    exp_repo = SqliteRepository(db_file=db_file, cls=Expense)
    budget_repo = SqliteRepository(db_file=db_file, cls=Budget)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(cat_repo, exp_repo, budget_repo)
    window.show()
    sys.exit(app.exec())
