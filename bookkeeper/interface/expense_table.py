from PySide6 import QtCore, QtWidgets


class ExpensesTable(QtWidgets.QTableWidget):
    columns = ["Дата", "Сумма", "Категория", "Комментарий"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setColumnCount(len(self.columns))
        self.setRowCount(20)
        self.setHorizontalHeaderLabels(self.columns)

        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.verticalHeader().hide()

    def fill_table(self, exp_repo):

        expenses = exp_repo.get_all()

        row_count = self.rowCount()

        for i, expense in enumerate(expenses):
            if i >= row_count:
                self.insertRow(i)
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(expense.added_date))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(expense.amount)))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(str(expense.category)))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(expense.comment))

