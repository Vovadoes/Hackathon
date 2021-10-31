import datetime
from pprint import pprint

import branca
# from PyQt5.QtWidgets import QApplication, QWidget
import sqlite3
import sys
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit, \
    QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.plugins import MarkerCluster


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
    def __init__(self):
        super().__init__()
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

        conection = sqlite3.connect('test.sqlite')
        cur = conection.cursor()
        problems = cur.execute("""SELECT * from problems""").fetchall()
        streets = {i[1]: i[0] for i in cur.execute("""SELECT * from streets""").fetchall()}
        pprint(f'{problems=}')
        pprint(f'{streets=}')

        # m = folium.Map([56.135690, 47.245953], zoom_start=13)
        html = open(r'./htmls/1.html', mode='r', encoding='UTF-8').read()

        group = folium.FeatureGroup(name='Проблемы', show=False)

        cluster = MarkerCluster(name='cluster',
                                popups='123',
                                show=False,
                                )

        for i in problems:
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
            # marker.add_to(m)
            # group.add_child(marker)
        # group.add_to(m)
        cluster.add_to(m)
        # folium.LayerControl(collapsed=True).add_to(m)

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
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Хаккатон задание')

        self.btn = QPushButton('Показать карту', self)
        self.btn.resize(200, 40)
        self.btn.move(20, 30)
        self.btn.clicked.connect(self.run)

        self.combo = QComboBox(self)
        self.combo.addItems(['1', '2', '3', '4'])
        self.combo.move(20, 100)
        self.combo.resize(200, 30)
        self.combo.activated[str].connect(self.onActivated)

        self.new_combo = QComboBox(self)
        self.new_combo.addItems(['лошадь', 'морж', 'свинка', 'пепел'])
        self.new_combo.move(20, 150)
        self.new_combo.resize(200, 30)

        self.button = QPushButton(self)
        self.button.setText('Сообщить о проблеме')
        self.button.resize(200, 30)
        self.button.move(20, 230)
        self.button.clicked.connect(self.error)

    def error(self):
        self.gg = Error()
        self.gg.show()

    def onActivated(self, text):
        print(text)

    def run(self):
        self.k = Map()
        self.k.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
