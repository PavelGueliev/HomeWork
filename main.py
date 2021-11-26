from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox, QWidget
import sys
import sqlite3
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main.ui', self)
        self.update_result_table()
        self.con = sqlite3.connect("coffee.sqlite")

    def update_result_table(self):
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()

        result = cur.execute('''
           SELECT coffes.id,
           name,
           title,
           state,
           description,
           cost,
           volume
           FROM coffes
           JOIN
           degrees_of_roastings ON degrees_of_roastings.id = coffes.degree_of_roasting;''').fetchall()

        self.tableWidget.setRowCount(len(result))

        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget.setColumnCount(len(result[0]))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки',
                                                    'молотый/в зернах', 'описание вкуса',
                                                    'цена', 'объем упаковки'])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.excepthook = except_hook
    exit(app.exec())