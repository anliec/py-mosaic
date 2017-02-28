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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_open = QtWidgets.QPushButton(self.centralwidget)
        self.pb_open.setObjectName("pb_open")
        self.horizontalLayout.addWidget(self.pb_open)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(False)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sb_im_h = QtWidgets.QSpinBox(self.centralwidget)
        self.sb_im_h.setEnabled(False)
        self.sb_im_h.setMinimum(1)
        self.sb_im_h.setObjectName("sb_im_h")
        self.horizontalLayout.addWidget(self.sb_im_h)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setEnabled(False)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.sb_im_v = QtWidgets.QSpinBox(self.centralwidget)
        self.sb_im_v.setEnabled(False)
        self.sb_im_v.setMinimum(1)
        self.sb_im_v.setObjectName("sb_im_v")
        self.horizontalLayout.addWidget(self.sb_im_v)
        self.pb_compute = QtWidgets.QPushButton(self.centralwidget)
        self.pb_compute.setEnabled(False)
        self.pb_compute.setObjectName("pb_compute")
        self.horizontalLayout.addWidget(self.pb_compute)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 559, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        self.actionExplore_new_path = QtWidgets.QAction(MainWindow)
        self.actionExplore_new_path.setObjectName("actionExplore_new_path")
        self.menuFile.addAction(self.actionExplore_new_path)
        self.menuFile.addAction(self.actionquit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb_open.setText(_translate("MainWindow", "Open"))
        self.label.setText(_translate("MainWindow", "Images h."))
        self.label_2.setText(_translate("MainWindow", "Images v."))
        self.pb_compute.setText(_translate("MainWindow", "Compute"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionquit.setText(_translate("MainWindow", "quit"))
        self.actionExplore_new_path.setText(_translate("MainWindow", "Explore new path..."))

