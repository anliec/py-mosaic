#!/bin/usr/python3.6

from core.databaseFiller import *
from GUI.ui_ExplorationWindow import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *


class ExplorationWidget(QDialog):
    path_to_explore = None
    explorer = None
    # signals
    exploration_finished = pyqtSignal()

    def __init__(self, path_to_explore):
        super(ExplorationWidget, self).__init__()
        # setup ui
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.path_to_explore = path_to_explore
        self.ui.lb_filePath.setText(path_to_explore)

    def explore(self):
        self.explorer = DatabaseFiller(self.path_to_explore)
        self.explorer.current_path_updated.connect(self.update_current_path)
        self.explorer.finished.connect(self.on_exploration_finished)
        self.explorer.start()

    def update_current_path(self):
        self.ui.lb_filePath.setText(self.explorer.current_path)

    def on_exploration_finished(self):
        self.exploration_finished.emit()
        self.accept()


