import os

from threading import Thread

from PyQt5.QtWidgets import QFileDialog, QMainWindow
from Malina_code import main
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
                target=main, args=(
                    self.way_load,
                    './output/table/output.xlsx',
                    lambda: self.label.setText(
                        'Файл создается и помещается в корневой каталог проекта.')
                )
            )
            th.start()
        except Exception as error:
            print(error.__class__.__name__)
            self.label.setText('Error function')
