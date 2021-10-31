from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel
import sqlite3
import sys


class Error(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ошибка')
        self.window_width, self.window_height = 500, 500
        self.setMinimumSize(self.window_width, self.window_height)

        self.gg = QComboBox(self)
        conection = sqlite3.connect('hahaton (1).sqlite')
        cur = conection.cursor()
        problems = cur.execute("""SELECT * from MainCriterion""").fetchall()
        problems = [i[1] for i in problems]
        self.my_dict = {}
        self.text = problems[0]
        print(problems[0])
        count = 2
        for i in range(len(problems)):
            k = cur.execute(f"""SELECT * from SecondaryCriterion
    WHERE MainCriterionId = (
SELECT id from MainCriterion
    WHERE Name = '{problems[i]}')""").fetchall()
            count += 1
            k = [mk[-1] for mk in k]
            self.my_dict[problems[i]] = []
            for j in range(len(k)):
                for hj in k[j].split(', '):
                    self.my_dict[str(problems[i])].append(hj)
        self.gg.addItems(problems)
        self.gg.activated[str].connect(self.onActivated)

        self.hh = QComboBox(self)
        self.hh.move(0, 50)
        self.hh.resize(400, 30)
        self.hh.addItems(self.my_dict[self.text])

    def onActivated(self, text):
        self.hh.clear()
        self.hh.addItems(self.my_dict[text])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Error()
    ex.show()
    sys.exit(app.exec())
