from PySide6 import QtWidgets


class BudgetTable(QtWidgets.QTableWidget):
    columns = ["Сумма", "Бюджет"]
    rows = ['День', 'Неделя', 'Месяц']

    def __init__(self, budget_repo, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setColumnCount(len(self.columns))
        self.setRowCount(len(self.rows))
        self.setHorizontalHeaderLabels(self.columns)
        self.setVerticalHeaderLabels(self.rows)

        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)

        vert_header = self.verticalHeader()
        vert_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        vert_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        vert_header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

        self.budget_repo = budget_repo

        budgets = self.budget_repo.get_all()

        for i in range(len(self.rows)):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(budgets[i].remaining_sum)))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(budgets[i].budget)))

        self.setEditTriggers(
            QtWidgets.QTableWidget.DoubleClicked)

        self.cellChanged.connect(self.handleCellChanged)

    def handleCellChanged(self, row, column):

        new_value = self.item(row, column).text()
        pk = row + 1
        changed_row = self.budget_repo.get(pk)

        if column == 0:
            changed_row.remaining_sum = new_value
        elif column == 1:
            changed_row.budget = new_value

        self.budget_repo.update(changed_row)