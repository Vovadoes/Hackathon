'''Этот код был написан под другой проект 2 года назад.'''

import os
from PyQt5 import QtWidgets
from qlabel import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
from Malina_code import main


class Mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.way_load = ''
        self.error_report = ''
        self.main()

    def main(self):
        # Меняем текст
        self.print_label("Please enter the path to the file")

        self.ui.pushButton.setText('Download')

        # Нажатие
        self.ui.pushButton.clicked.connect(self.ff)
        # while self.error_report != 'OK' and self.error_report != '':
        #     self.ui.pushButton.clicked.connect(self.ff)

    def ff(self):
        self.Click_actions()
        save = 'output.xlsx'
        if self.error_report == 'OK':
            try:
                self.ui.label.setText('The download is in progress wait')
                main(self.way_load)
                self.print_label('The file is generated and placed in the root of the project.')
            except Exception as error:
                print(error.__class__.__name__)
                self.print_label('Error function')
        else:
            self.ff1(save)
            return 0
        return -1

    def ff1(self, save):
        self.print_label(f'Путь сохранения: {save}')
        return 0

    def Click_actions(self):  # Действия при нажати
        self.way_load = QFileDialog.getOpenFileName(self, 'Загрузить xlsx файл')[0]

        print(self.way_load)
        self.error_report = self.check(self.way_load)
        self.print_label(self.error_report)
        if self.error_report != 'OK':
            return -1
        return 0

    def check(self, way):
        filename, file_extension = os.path.splitext(way)
        if file_extension != '.xlsx':
            return 'Ошибка. Загрузите пожалуйста файл с расширением xlsx!'
        return 'OK'

    def print_label(self, s, max_size=80):
        lst = s.split()
        if len(lst) != 0:
            lst_new = [lst[0]]
        else:
            lst_new = ['']
        x = 0
        for i in range(1, len(lst)):
            if len(lst_new[x]) + 1 + len(lst[i]) <= max_size:
                lst_new[x] += ' ' + lst[i]
            else:
                lst_new.append(lst[i])
                x += 1
        s = '\n'.join(lst_new)
        print(s)
        try:
            self.ui.label.setText(s)
        except:
            return -1
        else:
            return 0
