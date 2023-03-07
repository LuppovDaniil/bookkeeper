from PySide6 import QtWidgets


class AmmountInput(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('Сумма')
        self.input = QtWidgets.QLineEdit('0')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def ammount(self):
        return self.input.text()


class CategoryInput(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QFormLayout()
        self.label = QtWidgets.QLabel('Категория')
        self.input = QtWidgets.QComboBox()
        self.input.addItems(["Feature 1", "Feature 2", "Feature 3"])
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def category(self):
        return self.input.currentText()


class AddPurchase(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.category_input = CategoryInput()
        self.amount_input = AmmountInput()
        self.submit_button = QtWidgets.QPushButton('Добавить')

        self.submit_button.clicked.connect(self.submit)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.category_input)
        self.vbox.addWidget(self.amount_input)
        self.vbox.addWidget(self.submit_button)
        self.setLayout(self.vbox)

    def submit(self):
        print(self.category_input.category(), self.amount_input.ammount())