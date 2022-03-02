import datetime

import branca
# from PyQt5.QtWidgets import QApplication, QWidget
import sqlite3
import io

# import cluster as cluster
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.plugins import MarkerCluster

from settings import way_db


def filt_s(a: str = '', lst=None):
    if lst is None:
        lst = ["'", '.', ',']
    for j in lst:
        a = ''.join(a.split(j))
    return a


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

        conection = sqlite3.connect(way_db)
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
