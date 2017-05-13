#!/usr/bin/python3.6

import sys
from PyQt5.QtWidgets import QApplication, QDialog
from GUI.MainWindow import MainWindow
from PyQt5 import QtCore

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Translation setting
    language = QtCore.QLocale.system().name()
    loc = language.split('_')[0]

    translator = QtCore.QTranslator()
    translator.load("mosaic_" + loc)
    app.installTranslator(translator)

    w = MainWindow(app)
    w.show()

    sys.exit(app.exec_())
