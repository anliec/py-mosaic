#!/bin/usr/python3.6

from core.databaseFiller import *
from GUI.ui_ExplorationWindow import *
import os
from PyQt5.QtCore import pyqtSignal, QThread
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
        self.path_to_explore = path_to_explore
        self.ui.lb_filePath.setText("...")

    def explore(self):
        self.explorer = DatabaseFiller(self.path_to_explore)
        self.explorer.start()
        self.explorer.current_path_updated.connect(self.update_current_path)
        self.explorer.finished.connect(self.on_exploration_finished)

    def update_current_path(self):
        self.ui.lb_filePath.setText(self.explorer.current_path)

    def on_exploration_finished(self):
        self.exploration_finished.emit()
        self.accept()

    # def explore(self, path_to_explore=None):
    #     if path_to_explore is None and self.path_to_explore is None:
    #         return
    #     elif path_to_explore is not None:
    #         self.path_to_explore = path_to_explore
    #         self.ui.lb_filePath.setText(self.path_to_explore)
    #     if not self.isVisible():
    #         self.show()
    #     # open DB
    #     db = DataBase()
    #     # explore file three starting at the given point
    #     for filesTuple in os.walk(self.path_to_explore):
    #         # select only pictures extension
    #         for fileName in filesTuple[2]:
    #             extension = os.path.splitext(fileName)[1]
    #             extension = extension.lower()
    #             if extension in [".png", ".jpg"]:
    #                 full_path = os.path.abspath(filesTuple[0] + "/" + fileName)
    #                 # add the picture to DB (size check is done in db class)
    #                 db.add_photo(full_path)
    #                 self.ui.lb_filePath.setText(full_path)
    #     db.close()
    #     self.exploration_finished.emit()
    #     self.close()


