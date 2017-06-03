#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from GUI.ui_dialogphotos import *
from GUI.SelectionGraphicView import *


class DialogPhotos(QDialog):

    def __init__(self, list_of_images):
        super(DialogPhotos, self).__init__()
        # setup ui
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.graphicsView = SelectionGraphicView(list_of_images)



