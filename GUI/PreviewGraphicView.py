#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class PreviewGraphicView(QGraphicsView):
    images = None
    selected_image = (0, 0)

    generator = None
    target_path = None
    pixmap_items = dict()

    path_to_pixmap = dict()

    preview_factor = None  # set in MainWindow
    image_by_line = 3

    scene = None
    selection_rect = None
    scene_updater_thread = None
    background_brush = QBrush(QColor(100, 100, 100))

    # signals
    compute_started = pyqtSignal()
    compute_finished = pyqtSignal()
    selection_updated = pyqtSignal()

    def __init__(self):
        super(PreviewGraphicView, self).__init__()
        # set scene
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(self.background_brush)
        self.setScene(self.scene)
        # set help text
        self.scene.addText(self.tr("Click on \"Open\" to chose a\npicture to transform in a mosaic.\nOr go to \"File\"/\"Explore new path...\"\nto add file into de database."))
        # enable map style navigation
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def set_generator(self, generator):
        self.generator = generator
        self.pixmap_items = dict()
        self.path_to_pixmap = dict()
        self.scene.clear()

    def update_all_scene(self):
        # self.scene.clear()
        if self.generator is None:
            return
        print("updating preview")
        image_dict = self.generator.best_images_selected
        self.scene_updater_thread = ThreadedSceneUpdater(image_dict, self.preview_factor, self.path_to_pixmap)
        self.scene_updater_thread.start()
        self.scene_updater_thread.finished.connect(self.scene_updated)

    def scene_updated(self):
        # get the new scene and pixmap dict from the thread
        self.pixmap_items = self.scene_updater_thread.pixmap_items
        self.scene = self.scene_updater_thread.new_scene

        self.scene.setSceneRect(0, 0,
                                self.generator.number_of_image[0] * 3 * self.preview_factor,
                                self.generator.number_of_image[1] * 2 * self.preview_factor)
        self.selection_rect = self.scene.addRect(self.selected_image[0] * 3 * self.preview_factor,
                                                 self.selected_image[1] * 2 * self.preview_factor,
                                                 3 * self.preview_factor,
                                                 2 * self.preview_factor)
        # fit the new scene into the view
        self.scene.setBackgroundBrush(self.background_brush)
        self.setScene(self.scene)
        self.fit_scene_in_view()
        print("preview updated")

    def fit_scene_in_view(self):
        if self.generator is not None:
            self.fitInView(0, 0,
                           self.generator.number_of_image[0] * 3 * self.preview_factor,
                           self.generator.number_of_image[1] * 2 * self.preview_factor,
                           Qt.KeepAspectRatio)

    def update_scene_selection(self):
        x = self.selected_image[0] * self.preview_factor * 3
        y = self.selected_image[1] * self.preview_factor * 2
        self.selection_rect.setPos(x, y)

    def mouseDoubleClickEvent(self, event):
        position = event.pos()
        scene_pos = self.mapToScene(position)
        x = int(scene_pos.x()) // (self.preview_factor * 3)
        y = int(scene_pos.y()) // (self.preview_factor * 2)
        if x >= 0 and y >= 0 and x < self.generator.number_of_image[0] and y < self.generator.number_of_image[1]:
            if self.selected_image is not (x, y):
                self.selected_image = (x, y)
                self.update_scene_selection()
                self.selection_updated.emit()

    def resizeEvent(self, event):
        self.fit_scene_in_view()

    def wheelEvent(self, event):
        num_degree = event.angleDelta() / 8
        factor = 1.01**num_degree.y()
        self.scale(factor, factor)

    def compute(self):
        self.generator.finished.connect(self.computation_end)
        self.generator.selected_images_changed[int, int].connect(self.new_image_selected)
        self.generator.run_target = "found_best_images"
        self.generator.start()

    def computation_end(self):
        self.update_all_scene()
        self.generator.finished.disconnect(self.compute_finished)
        # image_dict = self.generator.best_images_found
        self.compute_finished.emit()

    def export_to_file(self, file_path):
        self.selection_rect.setVisible(False)
        image = QImage(self.generator.number_of_image[0] * 3 * self.preview_factor,
                       self.generator.number_of_image[1] * 2 * self.preview_factor,
                       QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(file_path)
        self.selection_rect.setVisible(True)


class ThreadedSceneUpdater(QThread):
    image_dict = None
    preview_factor = None
    new_scene = None
    pixmap_items = dict()
    number_of_child_thread = 0
    path_to_pixmap = dict()

    def __init__(self, image_dict, preview_factor, path_to_pixmap):
        super(ThreadedSceneUpdater, self).__init__()
        self.image_dict = image_dict
        self.preview_factor = preview_factor
        self.new_scene = QGraphicsScene()
        self.path_to_pixmap = path_to_pixmap

    def run(self):
        # load every image in it own thread, launch all the thread at the same time
        thread_list = []
        for value in self.image_dict.items():
            image_path = value[1][1]
            image_loader = ThreadedImageLoader(image_path, self.preview_factor, self.new_scene, self.pixmap_items, value[0], self.path_to_pixmap)
            image_loader.start()
            thread_list.append(image_loader)
        for thread in thread_list:
            thread.wait()


class ThreadedImageLoader(QThread):
    image_path = None
    preview_factor = None
    new_scene = None
    pixmap_items = None
    pos = (0, 0)
    path_to_pixmap = dict()

    def __init__(self, image_path, preview_factor, new_scene, pixmap_items, pos, path_to_pixmap):
        super(ThreadedImageLoader, self).__init__()
        self.image_path = image_path
        self.preview_factor = preview_factor
        self.new_scene = new_scene
        self.pixmap_items = pixmap_items
        self.pos = pos
        self.path_to_pixmap = path_to_pixmap

    def run(self):
        if self.image_path in self.path_to_pixmap:
            pixmap = self.path_to_pixmap[self.image_path]
        else:
            pixmap = QPixmap(self.image_path)
            pixmap = pixmap.scaled(3 * self.preview_factor,
                                       2 * self.preview_factor)
            self.path_to_pixmap[self.image_path] = pixmap
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setOffset(self.pos[0] * 3 * self.preview_factor,
                              self.pos[1] * 2 * self.preview_factor)
        self.new_scene.addItem(pixmap_item)
        self.pixmap_items[self.pos] = pixmap_item
