"""
Модуль с кнопкой для редактирования списка категорий
"""

from PySide6 import QtCore, QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SqliteRepository


class CategoryTable(QtWidgets.QTableWidget):
    """
    Виджет с таблицей категорий
    """
    data_updated = QtCore.Signal()

    columns = ['pk', 'имя', 'родитель']

    def __init__(self, cat_repo: SqliteRepository, *args, **kwargs) -> None:
        """

        Parameters
        ----------
        cat_repo - репозиторий с категориями расходов
        args
        kwargs
        """

        super().__init__(*args, **kwargs)

        self.cat_repo = cat_repo
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)

        self.verticalHeader().hide()

        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        cats = cat_repo.get_all()

        self.setRowCount(len(cats) + 1)
        self.rows_len = len(cats) + 1
        self.pk_dict = {}

        for i, cat in enumerate(cats):
            pk_item = QtWidgets.QTableWidgetItem(str(cat.pk))
            pk_item.setFlags(pk_item.flags() & ~QtCore.Qt.ItemIsEditable)

            name_item = QtWidgets.QTableWidgetItem(cat.name)
            parent_item = QtWidgets.QTableWidgetItem(str(cat.parent) if cat.parent else '')
            self.setItem(i, 0, pk_item)
            self.setItem(i, 1, name_item)
            self.setItem(i, 2, parent_item)
            self.pk_dict[i] = cat.pk

        self.setEditTriggers(
            QtWidgets.QTableWidget.DoubleClicked)

        self.cellChanged.connect(self.handleCellChanged)

    def handleCellChanged(self, row, column) -> None:

        """
        Перезапись базы данных в ответ на действие пользователя
        Parameters
        ----------
        row - строка, на которую воздействовал пользователь
        column - столбец, на которую воздействовал пользователь


        """

        new_name = self.item(row, 1).text()
        if self.item(row, 2):
            new_parent = int(self.item(row, 2).text())
        else:
            new_parent = None

        if row == self.rows_len - 1:
            new_value = Category(new_name, new_parent)
            self.cat_repo.add(new_value)
        else:
            pk = self.pk_dict[row]
            edited_value = self.cat_repo.get(pk)
            edited_value.name = new_name
            edited_value.parent = new_parent
            self.cat_repo.update(edited_value)

        self.data_updated.emit()


class AddCategory(QtWidgets.QWidget):
    """
    Кнопка для возова окна редактирования категорий
    """

    def __init__(self, cat_repo: SqliteRepository, *args, **kwargs) -> None:
        """

        Parameters
        ----------
        cat_repo - repository with categories
        args
        kwargs
        """
        super().__init__(*args, **kwargs)

        self.cat_repo = cat_repo
        self.add_button = QtWidgets.QPushButton('Категории')

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.add_button)
        self.setLayout(self.vbox)

        self.add_button.clicked.connect(self.submit)

        self.category_table = CategoryTable(self.cat_repo)

    def submit(self) -> None:
        """
        Реакция на нажатие кнопки пользователем
        """
        category_window = self.category_table
        category_window.setWindowTitle("Категории расходов")
        category_window.show()
