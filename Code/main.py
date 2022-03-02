import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextEdit, QLabel, \
    QCheckBox

from settings import way_db
from Create_db import default_db

from mywindow import MyWidget
from Map import Map


class Error(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ошибка')
        self.window_width, self.window_height = 500, 500
        self.setMinimumSize(self.window_width, self.window_height)

        self.text = QTextEdit(self)
        self.text.resize(400, 400)
        self.text.move(20, 100)

        self.lab = QLabel(self)
        self.lab.setText('Напишите нам!')
        self.lab.move(20, 50)

        self.push = QPushButton('отправить', self)
        self.push.move(200, 40)
        self.push.resize(100, 30)
        self.push.clicked.connect(self.run)

    def run(self):
        self.text.clear()
        self.lab.setText('Отправлено!')


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.mywindow = None
        self.k = None
        self.text = None
        self.status = None
        self.textt = None
        self.hh = None
        self.jhj = None
        self.check = None
        self.my_dict = None
        self.btn = None
        self.gg = None
        default_db()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Хакатон задание')

        self.btn = QPushButton('Показать карту', self)
        self.btn.resize(200, 40)
        self.btn.move(20, 30)
        self.btn.clicked.connect(self.run)

        self.btn = QPushButton('Загрузить таблицу', self)
        self.btn.resize(200, 30)
        self.btn.move(20, 230)
        self.btn.clicked.connect(self.load_table)

        self.gg = QComboBox(self)
        self.gg.resize(250, 30)
        self.gg.move(20, 100)
        conection = sqlite3.connect(way_db)
        cur = conection.cursor()
        problems = cur.execute("""SELECT * from MainCriterion""").fetchall()
        problems = [i[1] for i in problems]
        self.my_dict = {}
        if len(problems) != 0:
            self.text = problems[0]
            print(problems[0])
            count = 2
            for i in range(len(problems)):
                k = cur.execute(
                    f"""SELECT * from SecondaryCriterion
                            WHERE MainCriterionId = (
                            SELECT id from MainCriterion
                                WHERE Name = '{problems[i]}')"""
                ).fetchall()
                count += 1
                k = [mk[-1] for mk in k]
                self.my_dict[problems[i]] = []
                self.my_dict[str(problems[i])].append('Все')
                for j in range(len(k)):
                    for hj in k[j].split(', '):
                        self.my_dict[str(problems[i])].append(hj)
        self.gg.addItems(problems)
        self.gg.activated[str].connect(self.onActivated)

        self.check = QCheckBox(self)
        self.check.move(20, 200)
        self.check.stateChanged.connect(self.changeTitle)

        self.jhj = QLabel(self)
        self.jhj.setText('Все')
        self.jhj.move(50, 200)

        self.hh = QComboBox(self)
        self.hh.move(20, 150)
        self.hh.resize(250, 30)
        if self.my_dict:
            self.hh.addItems(self.my_dict[self.text])
        self.hh.activated[str].connect(self.on)

        # self.push = QPushButton('Сообщить о проблеме', self)
        # self.push.clicked.connect(self.error)
        # self.button.resize(200, 30)
        # self.button.move(20, 325)
        self.textt = 'Все'
        self.status = False

        self.text = 'дороги и транспорт'

    def changeTitle(self, status):
        print(bool(status))
        self.status = bool(status)

    def on(self, text):
        self.textt = text
        print(self.textt)

    def onActivated(self, text):
        self.hh.clear()
        self.hh.addItems(self.my_dict[text])
        self.text = text

    def error(self):
        self.gg = Error()
        self.gg.show()

    def run(self):
        self.k = Map(self.textt, self.status, self.text)
        self.k.show()

    def load_table(self):
        self.mywindow = MyWidget()
        self.mywindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
