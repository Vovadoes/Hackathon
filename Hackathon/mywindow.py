import os

from threading import Thread

from PyQt5.QtWidgets import QFileDialog, QMainWindow
from Malina_code import Recognition
from Create_db import start
from qlabel import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.way_load = ''
        self.pushButton.clicked.connect(self.click)

    def click(self):
        self.way_load = QFileDialog.getOpenFileName(self, 'Загрузить xlsx файл')[0]

        filename, file_extension = os.path.splitext(self.way_load)
        if file_extension != '.xlsx':
            self.label.setText('Ошибка. Загрузите пожалуйста файл с расширением xlsx!')
            return None

        self.label.setText('Загрузка продолжается подождите')
        try:
            th = Thread(
                target=self.choosing_downloads,
                args=(
                    self.way_load,
                    self.checkBox.isChecked(),
                    self.checkBox_2.isChecked()
                )
            )
            th.start()
        except Exception as error:
            print(error.__class__.__name__)
            self.label.setText('Ошибка')

    def progress_check(self, num, len_max):
        self.label.setText(f'Создание базы данных {num + 1} / {len_max}')

    def choosing_downloads(self, way, create_table, create_db):
        self.label.setText('Создание таблицы')
        print(f"{create_table=}, {create_db=}")
        if create_table:
            way = Recognition(
                way,
                './output/table/output.xlsx'
            ).main(
                self.progress_check,
            )
        if create_db:
            self.label.setText('Создание базы данных')
            start(way)
            self.label.setText('База данных создана')

        self.label.setText('Готово.')
