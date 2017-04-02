#!/usr/bin/python3.6

import sys
from PyQt5.QtWidgets import QApplication, QDialog
from GUI.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
