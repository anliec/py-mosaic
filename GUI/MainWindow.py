#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.ui_MainWindow import Ui_MainWindow
from core import MosaicGenerator
from GUI.ExplorationWidget import ExplorationWidget
from GUI.SelectionGraphicView import *
from GUI.PreviewGraphicView import *
from core.database import *
from GUI.NewMosaic import *
from core.OptimisatorLink import *


class MainWindow(QMainWindow):
    pixmap_items = dict()
    # size of pictures is x=3*preview_factor and y=2*preview_factor
    preview_factor = 150

    preview_widget = None
    exploration_window = None
    timer = None
    photo_selection_dialog = None
    new_mosaic_dialog = None

    def __init__(self, parent=None):
        super().__init__()
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # add preview widget
        self.preview_widget = PreviewGraphicView()
        self.centralWidget().layout().addWidget(self.preview_widget)
        # set photo selection dialogue
        self.photo_selection_dialog = SelectionGraphicView(list(), self.preview_widget.path_to_pixmap)
        # set preview factor for te two previous widget
        self.set_preview_factor(self.preview_factor)
        # set new mosaic dialog
        self.new_mosaic_dialog = NewMosaicDialog()
        # add the photo selection dialogue into a dock widget
        dock_widget = QDockWidget(self.tr("Picture selection"), self)
        dock_widget.setWidget(self.photo_selection_dialog)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        # setup status bar
        self.ui.statusbar.showMessage(self.tr("Ready"))
        # set window title
        self.setWindowTitle(self.tr("Mosaic Creator"))
        # setup menu
        self.ui.actionExport.setEnabled(False)
        self.ui.actionMin_same_picture_usage.setEnabled(False)
        # connection
        self.ui.actionExport.triggered.connect(self.export_button_clicked)
        self.ui.actionExplore_new_path_2.triggered.connect(self.explore_new_path)
        self.ui.actionQuit.triggered.connect(self.close)
        self.preview_widget.selection_updated.connect(self.new_image_selected)
        self.photo_selection_dialog.selection_updated.connect(self.change_image_from_selection_widget)
        self.ui.actionNew_mosaic.triggered.connect(self.new_mosaic_dialog.show)
        self.new_mosaic_dialog.finished.connect(self.on_new_mosaic_menu_finished)
        self.preview_widget.scene_update_finished.connect(self.on_scene_updated)
        self.preview_widget.scene_update_started.connect(self.on_scene_update_started)
        self.preview_widget.generator_changed.connect(self.on_preview_generator_changed)
        self.ui.actionMin_same_picture_usage.triggered.connect(self.on_optimisation_minimise_picture_double)
        # checkout DB state
        database = DataBase()
        if database.get_number_of_photo() == 0:
            self.warning_message_empty_db()

    def set_preview_factor(self, new_preview_factor):
        self.preview_factor = new_preview_factor
        self.preview_widget.preview_factor = self.preview_factor
        self.photo_selection_dialog.size_factor = self.preview_factor

    def setup_new_preview_widget(self):
        # disable old connections
        self.preview_widget.selection_updated.disconnect(self.new_image_selected)
        self.preview_widget.scene_update_finished.disconnect(self.on_scene_updated)
        self.preview_widget.scene_update_started.disconnect(self.on_scene_update_started)
        self.preview_widget.generator_changed.disconnect(self.on_preview_generator_changed)
        # replace widget in view
        old_preview_widget = self.preview_widget
        self.preview_widget = PreviewGraphicView()
        self.centralWidget().layout().replaceWidget(old_preview_widget, self.preview_widget)
        self.set_preview_factor(self.preview_factor)
        # update connections
        self.preview_widget.selection_updated.connect(self.new_image_selected)
        self.preview_widget.scene_update_finished.connect(self.on_scene_updated)
        self.preview_widget.scene_update_started.connect(self.on_scene_update_started)
        self.preview_widget.generator_changed.connect(self.on_preview_generator_changed)

    def on_new_mosaic_menu_finished(self):
        target_path = self.new_mosaic_dialog.ui.le_im_path.text()
        number_of_image_h = self.new_mosaic_dialog.ui.sb_im_h.value()
        number_of_image_v = self.new_mosaic_dialog.ui.sb_im_v.value()
        preview_factor = self.new_mosaic_dialog.ui.sb_tile_width.value() / 3
        self.new_mosaic_dialog.close()
        self.setup_new_preview_widget()
        self.set_preview_factor(preview_factor)
        self.preview_widget.set_generator(MosaicGenerator.MosaicGenerator(target_path,
                                                                          (number_of_image_h,
                                                                           number_of_image_v)))
        if self.new_mosaic_dialog.ui.cb_grayscale.isChecked():
            self.preview_widget.generator.generator_config.color_type = "BW"
        else:
            self.preview_widget.generator.generator_config.color_type = "color"
        self.preview_widget.generator.finished.connect(self.compute_finished)
        # self.preview_widget.generator.selected_images_changed[int, int].connect(self.new_image_selected)
        self.preview_widget.generator.run_target = "found_best_images"
        self.ui.statusbar.showMessage(self.tr("Computing"))
        self.preview_widget.generator.start()
        self.ui.actionExport.setEnabled(False)
        self.ui.actionMin_same_picture_usage.setEnabled(False)
        self.preview_widget.clear_scene()
        self.photo_selection_dialog.clear_scene()

    def compute_finished(self):
        self.preview_widget.update_all_scene()
        # self.ui.statusbar.showMessage(self.tr("Updating preview"))
        self.preview_widget.generator.finished.disconnect(self.compute_finished)
        self.ui.actionExport.setEnabled(True)
        self.ui.actionMin_same_picture_usage.setEnabled(True)

    def on_scene_updated(self):
        self.ui.statusbar.showMessage(self.tr("Ready"))

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
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setModal(True)
        file_dialog.show()
        file_dialog.fileSelected[str].connect(self.set_exploration_window)

    def set_exploration_window(self, path):
        self.exploration_window = ExplorationWidget(path)
        self.exploration_window.show()
        self.exploration_window.explore()
        self.exploration_window.finished.connect(self.on_exploration_window_closed)

    def on_exploration_window_closed(self):
        self.exploration_window = None

    def new_image_selected(self):
        selected_image = self.preview_widget.selected_image
        images = self.preview_widget.generator.best_images_found[selected_image]
        self.photo_selection_dialog.set_images(images)

    def change_image_from_selection_widget(self):
        selected_image = self.preview_widget.selected_image
        pixmap_item = self.preview_widget.pixmap_items[selected_image]
        new_pixmap = self.photo_selection_dialog.pixmap_dict[self.photo_selection_dialog.selected_image_index].pixmap()
        pixmap_item.setPixmap(new_pixmap)

    def export_button_clicked(self):
        file_dialog = QFileDialog(self, self.tr("Export current Mosaic as"))
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("png")
        file_dialog.setVisible(True)
        file_dialog.fileSelected[str].connect(self.preview_widget.export_to_file)

    def warning_message_empty_db(self):
        message_box = QMessageBox(QMessageBox.Warning,
                                  self.tr("Empty DataBase"),
                                  self.tr("Your photo database is currently empty.\nPlease go to \"DataBase\"/\"explore new path...\" to add files in it."),
                                  QMessageBox.Ok,
                                  self)
        message_box.show()
        return

    def on_preview_generator_changed(self):
        self.photo_selection_dialog.generator_config = self.preview_widget.generator.generator_config

    def on_optimisation_minimise_picture_double(self):
        self.ui.statusbar.showMessage(self.tr("Computing optimisation"))
        # setup optimisator
        optimisator_link = Optimiser()
        # run optimisator
        optimisator_link.set_dict(self.preview_widget.generator.best_images_found,
                                       self.preview_widget.generator.number_of_image)
        optimisator_link.call_cpp()
        self.preview_widget.generator.best_images_selected = optimisator_link.tile_dict_ret
        self.preview_widget.update_all_scene()

    def on_scene_update_started(self):
        self.ui.statusbar.showMessage(self.tr("Updating preview"))
