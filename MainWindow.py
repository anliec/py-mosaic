#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, QTimer
from ui_MainWindow import Ui_MainWindow
from core import MosaicGenerator
from ExplorationWidget import ExplorationWidget
from DialogPhotos import DialogPhotos
from dialogGraphicView import *
from PreviewGraphicView import *


class MainWindow(QMainWindow):
    # target_path = None
    # generator = None
    # scene = None
    pixmap_items = dict()
    # size of pictures is x=3*preview_factor and y=2*preview_factor
    # preview_factor = 50

    preview_widget = None
    exploration_window = None
    timer = None
    photo_selection_dialog = None

    def __init__(self):
        super(MainWindow, self).__init__()
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.preview_widget = PreviewGraphicView()
        self.centralWidget().layout().addWidget(self.preview_widget)
        # set scene
        # self.scene = QGraphicsScene()
        # background_brush = QBrush(QColor(100, 100, 100))
        # self.scene.setBackgroundBrush(background_brush)
        # self.ui.graphicsView.setScene(self.scene)
        # set status bar
        self.ui.statusbar.showMessage("Ready")

        #connection
        self.ui.pb_open.clicked.connect(self.open_button_clicked)
        self.ui.pb_compute.clicked.connect(self.compute_button_clicked)
        self.ui.actionExplore_new_path.triggered.connect(self.explore_new_path)
    #
    # def set_generator(self, generator):
    #     self.generator = generator
    #     self.pixmap_items = dict()
    #     self.scene.clear()
    #
    # def update_all_scene(self):
    #     self.scene.clear()
    #     if self.generator is None:
    #         return
    #     self.scene.setSceneRect(0, 0,
    #                             self.generator.number_of_image[0] * 3 * self.preview_factor,
    #                             self.generator.number_of_image[1] * 2 * self.preview_factor)
    #     image_dict = self.generator.best_images_selected
    #     for value in image_dict.items():
    #         image_path = value[1][1]
    #         pixmap = QPixmap(image_path)
    #         pixmap = pixmap.scaled(3*self.preview_factor,
    #                                2*self.preview_factor)
    #         if value[0] is self.pixmap_items:
    #             pixmap_item = self.pixmap_items[value[0]]
    #             pixmap_item.setPixmap(pixmap)
    #         else:
    #             pixmap_item = QGraphicsPixmapItem(pixmap)
    #             pixmap_item.setOffset(value[0][0] * 3 * self.preview_factor,
    #                                   value[0][1] * 2 * self.preview_factor)
    #             self.scene.addItem(pixmap_item)
    #             self.pixmap_items[value[0]] = pixmap_item
    #     # fit the new scene into the view
    #     self.fit_scene_in_view()
    #
    # def fit_scene_in_view(self):
    #     self.ui.graphicsView.fitInView(0, 0,
    #                                    self.generator.number_of_image[0] * 3 * self.preview_factor,
    #                                    self.generator.number_of_image[1] * 2 * self.preview_factor)

    def open_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setVisible(True)
        file_dialog.fileSelected[str].connect(self.file_chosen)

    def file_chosen(self, file_path):
        self.preview_widget.target_path = file_path
        self.preview_widget.set_generator(None)
        self.ui.label.setEnabled(True)
        self.ui.label_2.setEnabled(True)
        self.ui.sb_im_h.setEnabled(True)
        self.ui.sb_im_v.setEnabled(True)
        self.ui.pb_compute.setEnabled(True)

    def compute_button_clicked(self):
        self.preview_widget.set_generator(MosaicGenerator.MosaicGenerator(self.preview_widget.target_path,
                          (self.ui.sb_im_h.value(),
                           self.ui.sb_im_v.value())))
        self.preview_widget.generator.finished.connect(self.compute_finished)
        # self.preview_widget.generator.selected_images_changed[int, int].connect(self.new_image_selected)
        self.preview_widget.generator.run_target = "found_best_images"
        self.ui.statusbar.showMessage("Computing")
        self.preview_widget.generator.start()

    def compute_finished(self):
        self.preview_widget.update_all_scene()
        self.ui.statusbar.showMessage("Ready")
        self.preview_widget.generator.finished.disconnect(self.compute_finished)
        image_dict = self.preview_widget.generator.best_images_found
        self.photo_selection_dialog = DialogGraphicView(image_dict[(0, 0)])
        self.photo_selection_dialog.show()

    # def new_image_selected(self, x, y):
    #     image_path = self.preview_widget.generator.best_images_selected[(x, y)][1]
    #     pixmap = QPixmap(image_path)
    #     pixmap = pixmap.scaled(3 * self.preview_factor,
    #                            2 * self.preview_factor)
    #     if (x, y) is self.pixmap_items:
    #         pixmap_item = self.pixmap_items[value[0]]
    #         pixmap_item.setPixmap(pixmap)
    #     else:
    #         pixmap_item = QGraphicsPixmapItem(pixmap)
    #         pixmap_item.setOffset(x * 3 * self.preview_factor,
    #                               y * 2 * self.preview_factor)
    #         self.scene.addItem(pixmap_item)
    #         self.pixmap_items[(x, y)] = pixmap_item

    def explore_new_path(self):
        self.setEnabled(False)
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setVisible(True)
        file_dialog.fileSelected[str].connect(self.set_exploration_window)

    def set_exploration_window(self, path):
        print(path)
        self.timer = QTimer()
        self.exploration_window = ExplorationWidget(path)
        self.exploration_window.show()
        self.timer.timeout.connect(self.open_exploration_window)
        self.timer.setSingleShot(True)
        self.timer.start(100)

    def open_exploration_window(self):
        print("open !")
        self.timer = None
        self.exploration_window.explore()
        self.setEnabled(True)
        self.exploration_window = None
