from PySide6 import QtWidgets


class ExpensesTable(QtWidgets.QTableWidget):
    columns = ["Дата", "Сумма", "Категория", "Комментарий"]

    def __init__(self, exp_repo, *args, **kwargs):

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
            QtWidgets.QTableWidget.DoubleClicked)

        self.verticalHeader().hide()

        self.exp_repo = exp_repo

        self.cellChanged.connect(self.handleCellChanged)

        self.pk_row_dict = {}

    def handleCellChanged(self, row, column):
        # Retrieve the new value from the table
        new_value = self.item(row, column).text()

        pk = self.pk_row_dict[row]

        changed_row = self.exp_repo.get(pk)

        if column == 0:
            changed_row.added_date = new_value
        elif column == 1:
            changed_row.amount = new_value
        elif column == 2:
            changed_row.category = new_value
        else:
            changed_row.comment = new_value

        self.exp_repo.update(changed_row)

    def fill_table(self):

        expenses = self.exp_repo.get_all()

        replace_dict = {}

        table.cellChanged.disconnect()
        row_count = self.rowCount()

        for i, expense in enumerate(expenses):
            if i >= row_count:
                self.insertRow(i)
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(expense.added_date))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(expense.amount)))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(str(expense.category)))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(expense.comment))
            self.pk_row_dict[i] = expense.pk

        self.cellChanged.connect(self.handleCellChanged)

