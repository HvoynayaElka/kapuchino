import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class Espresso(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.bd = None
        self.cursor = None
        self.load_table()
        self.pushButton.clicked.connect(self.openform)
        self.form = None

    def load_table(self):
        self.bd = sqlite3.connect('coffee.sqlite')
        self.cursor = self.bd.cursor()
        mass = self.cursor.execute("SELECT * FROM coffees").fetchall()
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                 'объем упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(mass):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if elem == '':
                    data = 'Пусто'
                else:
                    data = elem
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data)))
        self.tableWidget.resizeColumnsToContents()
        self.bd.close()

    def openform(self):
        self.form = AddChange(self.load_table)
        self.form.show()


class AddChange(QWidget):
    def __init__(self, func):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.bd = None
        self.cursor = None
        self.func = func
        self.add_btn.clicked.connect(self.add_to_bd)
        self.edit_btn.clicked.connect(self.edit_bd)

    def add_to_bd(self):
        self.errorlbl.setText('')
        try:
            self.bd = sqlite3.connect('coffee.sqlite')
            self.cursor = self.bd.cursor()
            if not self.id_ent.text().isdigit():
                raise Exception
            req = (f"Insert into coffees(name, st_ob, type, smell, price, V) values('{self.name.text()}', "
                   f"'{self.st.text()}', '{self.type.text()}', "
                   f"'{self.desc.text()}', '{self.price.text()}', '{self.v.text()}')")
            self.cursor.execute(req)
            self.bd.commit()
            self.bd.close()
            self.func()
            self.close()
        except Exception:
            self.errorlbl.setText('Некорректные данные')

    def edit_bd(self):
        self.errorlbl.setText('')
        try:
            self.bd = sqlite3.connect('coffee.sqlite')
            self.cursor = self.bd.cursor()
            self.errorlbl.setText('')
            req = (f"Update coffees SET name = '{self.name.text()}', "
                   f"st_ob = '{self.st.text()}', type = '{self.type.text()}', smell = '{self.desc.text()}', "
                   f"price = '{self.price.text()}', V = '{self.v.text()}' WHERE ID = {self.id_ent.text()}")
            self.cursor.execute(req)
            self.bd.commit()
            self.bd.close()
            self.func()
            self.close()
        except Exception:
            self.errorlbl.setText('Некорректные данные')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Espresso()
    w.show()
    sys.exit(app.exec())