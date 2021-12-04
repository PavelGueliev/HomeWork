from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from addEditCoffeeForm import Ui_MainWindow as Ui_CoffeeForm
from main_form import Ui_MainWindow
import sys
import sqlite3


class WindowInsertCoffe(QMainWindow, Ui_CoffeeForm):
    def __init__(self):
        super(WindowInsertCoffe, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_items)
        self.con = sqlite3.connect('data/coffee.sqlite')

    def add_items(self):
        if ((not self.lineEdit.text()) or (not self.lineEdit_2.text())
                or (not self.lineEdit_3.text()) or (not self.lineEdit_4.text()) or (not self.lineEdit_5.text())):
            self.statusBar().showMessage('Неверно заполнена форма')
            return
        self.statusBar().showMessage('')
        try:
            if not int(self.lineEdit_4.text()):
                self.statusBar().showMessage('Неверно заполнена форма')
                return
            self.save_results(self.lineEdit.text(), self.comboBox.currentText(),
                              self.lineEdit_2.text(), self.lineEdit_3.text(),
                              int(self.lineEdit_4.text()), self.lineEdit_5.text())
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            w.update_result_table()
            self.close()
        except Exception:
            self.statusBar().showMessage('Неверно заполнена форма')

    def save_results(self, name, degree_of_roasting, state, description, cost, volume):
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        cur = self.con.cursor()
        degree_of_roasting = cur.execute('SELECT id FROM degrees_of_roastings WHERE title = ?;',
                                         (degree_of_roasting,)).fetchone()[0]
        cur.execute("INSERT INTO coffes(name, degree_of_roasting, state, description, cost, volume) VALUES(?, ?, ?, "
                    "?, ?, ?);",
                    (name, degree_of_roasting, state, description, cost, volume))
        self.con.commit()


class WindowUpdateCoffe(QMainWindow, Ui_CoffeeForm):
    def __init__(self, id_coffee, name, degree_of_roasting, state, description, cost, volume):
        super(WindowUpdateCoffe, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_items)
        self.lineEdit.setText(name)
        self.comboBox.setCurrentText(degree_of_roasting)
        self.lineEdit_2.setText(state)
        self.lineEdit_3.setText(description)
        self.lineEdit_4.setText(cost)
        self.lineEdit_5.setText(volume)
        self.id = id_coffee
        self.con = sqlite3.connect('data/coffee.sqlite')

    def add_items(self):
        self.statusBar().showMessage('')
        if not self.lineEdit.text() or not self.lineEdit_2.text() or not self.lineEdit_3.text():
            self.statusBar().showMessage('Неверно заполнена форма')
            return
        self.statusBar().showMessage('')
        try:
            if int(self.lineEdit_2.text()) < 0 or int(self.lineEdit_3.text()) < 0 or int(self.lineEdit_2.text()) > 2021:
                self.statusBar().showMessage('Неверно заполнена форма')
                return
            self.save_results(self.lineEdit.text(), self.comboBox.currentText(),
                              self.lineEdit_2.text(), self.lineEdit_3.text(),
                              int(self.lineEdit_4.text()), self.lineEdit_5.text())
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            w.update_result_table()
            self.close()
        except Exception:
            self.statusBar().showMessage('Неверно заполнена форма')

    def save_results(self, name, degree_of_roasting, state, description, cost, volume):
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        cur = self.con.cursor()
        degree_of_roasting = cur.execute('SELECT id FROM degrees_of_roastings WHERE title = ?;',
                                         (degree_of_roasting,)).fetchone()[0]
        cur.execute("UPDATE films SET name = ?, degree_of_roasting = ?, state = ?, description = ?, cost = ?, "
                    "volume = ? WHERE id = ?;",
                    (name, degree_of_roasting, state, description, cost, volume, self.id))
        self.con.commit()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.update_result_table()
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.insert_coffee)
        self.pushButton_2.clicked.connect(self.update_coffee)

    def update_result_table(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
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

    def insert_coffee(self):
        self.statusBar().showMessage('')
        self.w = WindowInsertCoffe()
        self.update_result_table()
        self.w.show()

    def update_coffee(self):
        try:
            self.statusBar().showMessage('')
            id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            name = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
            degree_of_roasting = self.tableWidget.item(self.tableWidget.currentRow(), 2).text()
            state = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
            description = self.tableWidget.item(self.tableWidget.currentRow(), 4).text()
            cost = self.tableWidget.item(self.tableWidget.currentRow(), 5).text()
            volume = self.tableWidget.item(self.tableWidget.currentRow(), 6).text()
            self.w = WindowUpdateCoffe(id, name, degree_of_roasting, state, description, cost, volume)
            self.update_result_table()
            self.w.show()
        except Exception:
            self.statusBar().showMessage('Выберете ячейку!')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.excepthook = except_hook
    exit(app.exec())