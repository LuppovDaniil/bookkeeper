from PySide6 import QtWidgets, QtCore

from bookkeeper.models.expense import Expense


class AmountInput(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('Сумма')
        self.input = QtWidgets.QLineEdit('0')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def amount(self):
        return int(self.input.text())


class CategoryInput(QtWidgets.QWidget):

    def __init__(self, cat_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cat_repo = cat_repo
        self.layout = QtWidgets.QFormLayout()
        self.label = QtWidgets.QLabel('Категория')
        self.input = QtWidgets.QComboBox()

        cats = self.cat_repo.get_all()

        features_list = [cat.name for cat in cats]

        self.input.addItems(features_list)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def category(self):
        return self.input.currentText()

    @QtCore.Slot()
    def categories_edited_response(self):
        cats = self.cat_repo.get_all()
        features_list = [cat.name for cat in cats]
        self.input.addItems(features_list)


class AddPurchase(QtWidgets.QWidget):
    data_updated = QtCore.Signal()

    def __init__(self, cat_repo, exp_repo, budget_repo, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.budget_repo = budget_repo

        self.category_input = CategoryInput(self.cat_repo)
        self.amount_input = AmountInput()
        self.submit_button = QtWidgets.QPushButton('Добавить')

        self.submit_button.clicked.connect(self.submit)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.category_input)
        self.vbox.addWidget(self.amount_input)
        self.vbox.addWidget(self.submit_button)
        self.setLayout(self.vbox)

    @QtCore.Slot()
    def budget_update_response(self):

        budgets = self.budget_repo.get_all()
        flag = []
        for budget in budgets:
            flag.append(budget.cur_sum <= budget.budget)

        self.submit_button.setEnabled(all(flag))
        self.submit_button.setText('Добавить' if all(flag) else 'Бюджет исчерпан!')

    def submit(self):

        category = self.cat_repo.get_all(where={'name': self.category_input.category()})[0].pk
        added_exp = Expense(category=category,
                            amount=self.amount_input.amount())
        self.exp_repo.add(added_exp)

        budgets = self.budget_repo.get_all()

        for budget in budgets:
            budget.register_purchase(self.amount_input.amount())
            self.budget_repo.update(budget)

        self.data_updated.emit()
