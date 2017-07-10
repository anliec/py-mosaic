# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(559, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 559, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDataBase = QtWidgets.QMenu(self.menubar)
        self.menuDataBase.setObjectName("menuDataBase")
        self.menuOptimisation = QtWidgets.QMenu(self.menubar)
        self.menuOptimisation.setObjectName("menuOptimisation")
        self.menuWindows = QtWidgets.QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionExplore_new_path = QtWidgets.QAction(MainWindow)
        self.actionExplore_new_path.setObjectName("actionExplore_new_path")
        self.actionNew_mosaic = QtWidgets.QAction(MainWindow)
        self.actionNew_mosaic.setObjectName("actionNew_mosaic")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionExplore_new_path_2 = QtWidgets.QAction(MainWindow)
        self.actionExplore_new_path_2.setObjectName("actionExplore_new_path_2")
        self.actionMin_same_picture_usage = QtWidgets.QAction(MainWindow)
        self.actionMin_same_picture_usage.setEnabled(False)
        self.actionMin_same_picture_usage.setObjectName("actionMin_same_picture_usage")
        self.actionPicture_Selection = QtWidgets.QAction(MainWindow)
        self.actionPicture_Selection.setCheckable(True)
        self.actionPicture_Selection.setObjectName("actionPicture_Selection")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew_mosaic)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuDataBase.addAction(self.actionExplore_new_path_2)
        self.menuOptimisation.addAction(self.actionMin_same_picture_usage)
        self.menuWindows.addAction(self.actionPicture_Selection)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDataBase.menuAction())
        self.menubar.addAction(self.menuOptimisation.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDataBase.setTitle(_translate("MainWindow", "DataBase"))
        self.menuOptimisation.setTitle(_translate("MainWindow", "Optimisation"))
        self.menuWindows.setTitle(_translate("MainWindow", "Windows"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionExplore_new_path.setText(_translate("MainWindow", "Explore new path..."))
        self.actionNew_mosaic.setText(_translate("MainWindow", "New mosaic"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExplore_new_path_2.setText(_translate("MainWindow", "Explore new path..."))
        self.actionMin_same_picture_usage.setText(_translate("MainWindow", "Min. same picture usage"))
        self.actionPicture_Selection.setText(_translate("MainWindow", "Picture Selection"))

