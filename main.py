import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('espresso/main.ui', self)
        self.tableWidget.setColumnHidden(0, True)
        self.con = sqlite3.connect('espresso/coffee_db.sqlite')
        self.update_result()
        self.pushButton.clicked.connect(self.add_new)

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute('''SELECT id, name, melt, gg, taste, price, storage FROM coffee''').fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_new(self):
        add_window = AddWidget(self)
        add_window.show()


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('espresso/addEditCoffeeForm.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
