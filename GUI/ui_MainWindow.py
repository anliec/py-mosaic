# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 559, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDataBase = QtWidgets.QMenu(self.menubar)
        self.menuDataBase.setObjectName("menuDataBase")
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
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew_mosaic)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuDataBase.addAction(self.actionExplore_new_path_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDataBase.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDataBase.setTitle(_translate("MainWindow", "DataBase"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionExplore_new_path.setText(_translate("MainWindow", "Explore new path..."))
        self.actionNew_mosaic.setText(_translate("MainWindow", "New mosaic"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExplore_new_path_2.setText(_translate("MainWindow", "Explore new path..."))

