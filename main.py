import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from UI_main import Ui_MainWindow
from addEditCoffeeForm import Ui_AddWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.setColumnHidden(0, True)
        self.con = sqlite3.connect('data/coffee_db.sqlite')
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


class AddWidget(QMainWindow, Ui_AddWindow):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.setupUi(self)
            self.addbutton.clicked.connect(self.add_to_table)
            self.con = sqlite3.connect('data/coffee_db.sqlite')
        except Exception as e:
            print(e)

    def add_to_table(self):
        params = [self.name.text(), self.melt.text(), self.kind.text(), self.taste.text(),
                  self.cost.text(), self.storage.text()]
        cur = self.con.cursor()
        cur.execute('''INSERT INTO coffee (name, melt, gg, taste, price, storage) VALUES(?, ?, 
        ?, ?, ?, ?)''', (params[0], params[1],
                         params[2], params[3], params[4], params[5])).fetchall()
        self.con.commit()
        self.parent().update_result()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
