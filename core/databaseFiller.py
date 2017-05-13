#!/usr/bin/python3.6
import os
from core import database
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DatabaseFiller(QThread):
    path_to_explore = None

    current_path = ""

    # signal
    current_path_updated = pyqtSignal()

    def __init__(self, path_to_explore):
        super().__init__()
        self.path_to_explore = path_to_explore

    def run(self):
        # open DB
        db = database.DataBase()
        # explore file three starting at the given point
        for filesTuple in os.walk(self.path_to_explore):
            # select only pictures extension
            for fileName in filesTuple[2]:
                self.current_path = filesTuple[0] + "/" + fileName
                self.current_path_updated.emit()
                extension = os.path.splitext(fileName)[1]
                extension = extension.lower()
                if extension in [".png", ".jpg"]:
                    full_path = os.path.abspath(self.current_path)
                    # add the picture to DB (size check is done in db class)
                    db.add_photo(full_path)
        db.close()
