#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal


class PreviewGraphicView(QGraphicsView):
    images = None
    selected_image = (0, 0)

    generator = None
    target_path = None
    pixmap_items = dict()

    preview_factor = 50
    image_by_line = 3

    scene = None
    selection_rect = None

    #signals
    compute_started = pyqtSignal()
    compute_finished = pyqtSignal()

    def __init__(self):
        super(PreviewGraphicView, self).__init__()
        # set scene
        self.scene = QGraphicsScene()
        background_brush = QBrush(QColor(100, 100, 100))
        self.scene.setBackgroundBrush(background_brush)
        self.setScene(self.scene)
        self.update_all_scene()

    def set_generator(self, generator):
        self.generator = generator
        self.pixmap_items = dict()
        self.scene.clear()

    def update_all_scene(self):
        self.scene.clear()
        if self.generator is None:
            return
        self.scene.setSceneRect(0, 0,
                                self.generator.number_of_image[0] * 3 * self.preview_factor,
                                self.generator.number_of_image[1] * 2 * self.preview_factor)
        image_dict = self.generator.best_images_selected
        for value in image_dict.items():
            image_path = value[1][1]
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(3*self.preview_factor,
                                   2*self.preview_factor)
            if value[0] is self.pixmap_items:
                pixmap_item = self.pixmap_items[value[0]]
                pixmap_item.setPixmap(pixmap)
            else:
                pixmap_item = QGraphicsPixmapItem(pixmap)
                pixmap_item.setOffset(value[0][0] * 3 * self.preview_factor,
                                      value[0][1] * 2 * self.preview_factor)
                self.scene.addItem(pixmap_item)
                self.pixmap_items[value[0]] = pixmap_item
        # display selection rect
        self.selection_rect = self.scene.addRect(self.selected_image[0] * 3 * self.preview_factor,
                                                 self.selected_image[1] * 2 * self.preview_factor,
                                                 3 * self.preview_factor,
                                                 2 * self.preview_factor)
        # fit the new scene into the view
        self.fit_scene_in_view()

    def fit_scene_in_view(self):
        self.fitInView(0, 0,
                       self.generator.number_of_image[0] * 3 * self.preview_factor,
                       self.generator.number_of_image[1] * 2 * self.preview_factor)

    def update_scene_selection(self):
        x = self.selected_image_index % self.image_by_line * self.preview_factor * 3
        y = self.selected_image_index // self.image_by_line * self.preview_factor * 2
        if x >= 0 and\
                y >= 0 and\
                x < self.generator.number_of_image[0] and\
                y < self.generator.number_of_image[1]:
            self.selection_rect.setPos(self.selected_image_index % self.image_by_line * self.preview_factor * 3,
                                       self.selected_image_index // self.image_by_line * self.preview_factor * 2)

    def mousePressEvent(self, event):
        position = event.pos()
        scene_pos = self.mapToScene(position)
        self.selected_image = (int(scene_pos.x()) // (self.preview_factor * 3),
                               int(scene_pos.y()) // (self.preview_factor * 2))
        self.update_scene_selection()

    def compute(self):
        self.generator.finished.connect(self.computation_end)
        self.generator.selected_images_changed[int, int].connect(self.new_image_selected)
        self.generator.run_target = "found_best_images"
        self.generator.start()

    def computation_end(self):
        self.update_all_scene()
        self.generator.finished.disconnect(self.compute_finished)
        image_dict = self.generator.best_images_found
        self.compute_finished.emit()