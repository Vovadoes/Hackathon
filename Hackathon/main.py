import datetime
from pprint import pprint

import branca
# from PyQt5.QtWidgets import QApplication, QWidget
import sqlite3
import sys
import io

# import cluster as cluster
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit, \
    QLabel, QCheckBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.plugins import MarkerCluster

from mywindow import Mywindow


def filt_s(a: str = '', lst=None):
    if lst is None:
        lst = ["'", '.', ',']
    for j in lst:
        a = ''.join(a.split(j))
    return a


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


class Map(QWidget):
    def __init__(self, txt, stat, more):
        super().__init__()
        self.txt = txt
        self.stat = stat
        self.more = more
        self.setWindowTitle('Карта Чебоксар')
        self.window_width, self.window_height = 1280, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (56.135690, 47.245953)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=11,
            location=coordinate
        )

        conection = sqlite3.connect('hakaton.sqlite')
        cur = conection.cursor()
        streets = {i[1]: i[0] for i in cur.execute("""SELECT * from streets""").fetchall()}
        my_list = []
        if self.stat:
            problems = cur.execute(f"""select * from problems""")
        elif self.txt == 'Все':
            problems = cur.execute(
                f'''SELECT Name from SecondaryCriterion
                        WHERE MainCriterionId = (
                        select id from MainCriterion
                            WHERE Name = '{self.more}')'''
            ).fetchall()
            print(self.more)
            print(problems)
            my_list = []
            for hj in problems:
                k = cur.execute(
                    f"""SELECT ProblemId from Main
                            where SecondaryCriterionId = (
                            SELECT id from SecondaryCriterion
                                where Name = '{hj[0]}')"""
                ).fetchall()
                for i in k:
                    my_list.append(cur.execute(
                        f"""select * from problems
                                where id = {i[0]}"""
                    ).fetchall()[0])
                problems = my_list
        else:
            problems = cur.execute(
                f"""SELECT ProblemId from Main
                        where SecondaryCriterionId = (
                        SELECT id from SecondaryCriterion
                            where Name = '{self.txt}')"""
            ).fetchall()
            for i in problems:
                my_list.append(cur.execute(
                    f"""select * from problems
                            where id = {i[0]}"""
                ).fetchall()[0])

            problems = my_list
        # m = folium.Map([56.135690, 47.245953], zoom_start=13)
        html = open(r'./htmls/1.html', mode='r', encoding='UTF-8').read()

        cluster = MarkerCluster(
            name='cluster',
            popups='123',
            show=False,
        )
        n = 0
        for i in problems:
            n += 1
            date = datetime.date(*([int(i) for i in i[5].split('.')]))

            html_new = html.format(
                problems=filt_s(' '.join(i[6].split())),
                street=streets[i[1]],
                house=i[2],
                date=date.__format__('%Y.%m.%d')
            )

            iframe = branca.element.IFrame(html=html_new, width=450, height=200)
            popup = folium.Popup(iframe, max_width=500)
            marker = folium.Marker(
                location=[float(i[3]), float(i[4])],
                popup=popup,
            )

            cluster.add_child(marker)
        cluster.add_to(m)
        # folium.LayerControl(collapsed=True).add_to(m)

        print(f'{n=}')
        conection.close()

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 375)
        self.setWindowTitle('Хаккатон задание')

        self.btn = QPushButton('Показать карту', self)
        self.btn.resize(200, 40)
        self.btn.move(20, 30)
        self.btn.clicked.connect(self.run)

        self.btn = QPushButton('Загрузить таблицу', self)
        self.btn.resize(200, 30)
        self.btn.move(20, 325)
        self.btn.clicked.connect(self.load_table)

        self.gg = QComboBox(self)
        self.gg.resize(250, 30)
        self.gg.move(20, 100)
        conection = sqlite3.connect('hakaton.sqlite')
        cur = conection.cursor()
        problems = cur.execute("""SELECT * from MainCriterion""").fetchall()
        problems = [i[1] for i in problems]
        self.my_dict = {}
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
        self.hh.addItems(self.my_dict[self.text])
        self.hh.activated[str].connect(self.on)

        self.push = QPushButton('Сообщить о проблеме', self)
        self.push.clicked.connect(self.error)
        self.push.move(20, 250)
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

        self.button = QPushButton(self)
        self.button.setText('Сообщить о проблеме')
        self.button.resize(200, 30)
        self.button.move(20, 230)
        self.button.clicked.connect(self.error)

    def error(self):
        self.gg = Error()
        self.gg.show()

    def run(self):
        self.k = Map(self.textt, self.status, self.text)
        self.k.show()

    def load_table(self):
        self.mywindow = Mywindow()
        self.mywindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
