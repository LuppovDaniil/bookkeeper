"""
Модуль содержащий виджет для таблицы с бюджетом
"""

from PySide6 import QtWidgets, QtCore
from bookkeeper.repository.sqlite_repository import SqliteRepository


class BudgetTable(QtWidgets.QTableWidget):
    """
    Виджет для отображения таблицы с бюджетом
    """
    budget_updated = QtCore.Signal()

    columns = ["Сумма", "Бюджет"]
    rows = ['День', 'Неделя', 'Месяц']

    def __init__(self, budget_repo: SqliteRepository, *args, **kwargs) -> None:
        """

        Parameters
        ----------
        budget_repo - репозиторий с бюджетом
        args
        kwargs
        """

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

        self.setEditTriggers(
            QtWidgets.QTableWidget.DoubleClicked)

        self.cellChanged.connect(self.handleCellChanged)

    def fill_table(self) -> None:
        """
        Заполнение виджета данными из базы данных
        """

        budgets = self.budget_repo.get_all()

        for i in range(len(self.rows)):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(budgets[i].cur_sum)))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(budgets[i].budget)))
        self.budget_updated.emit()

    def handleCellChanged(self, row: int, column: int) -> None:
        """
        Регистрация изменения в таблице с бюджетом
        Parameters
        ----------
        row - измененная строка
        column - измененный столбец

        """

        new_value = self.item(row, column).text()
        pk = row + 1
        changed_row = self.budget_repo.get(pk)

        if column == 0:
            changed_row.cur_sum = new_value
        elif column == 1:
            changed_row.budget = new_value

        self.budget_repo.update(changed_row)

        self.budget_updated.emit()
