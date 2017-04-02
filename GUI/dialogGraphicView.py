#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogGraphicView(QGraphicsView):
    images = None
    selected_image_index = 0

    size_factor = None# set in MainWindow
    image_by_line = 3

    scene = None
    selection_rect = None

    pixmap_dict = dict()

    #signals
    selection_updated = pyqtSignal()

    def __init__(self, list_of_images):
        super(DialogGraphicView, self).__init__()
        self.images = list_of_images
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.update_scene()

    def update_scene(self):
        if len(self.images) == 0:
            return
        print("updating scene")
        n = 0
        for image in self.images:
            pixmap = QPixmap(image[1]) # 1 to get the path (0 is the score)
            pixmap = pixmap.scaled(3 * self.size_factor,
                                   2 * self.size_factor)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            x = n % self.image_by_line
            y = n // self.image_by_line
            pixmap_item.setOffset(x * (self.size_factor * 3 + 10),
                                  y * (self.size_factor * 2 + 10))
            self.pixmap_dict[n] = pixmap_item
            self.scene.addItem(pixmap_item)
            n += 1
        self.selection_rect = self.scene.addRect(
                                    self.selected_image_index % self.image_by_line * (self.size_factor * 3 + 10),
                                    self.selected_image_index // self.image_by_line * (self.size_factor * 2 + 10),
                                    self.size_factor * 3,
                                    self.size_factor * 2)
        self.fit_scene_in_view()
        print("scene updated")

    def fit_scene_in_view(self):
        self.fitInView(0, 0,
                       self.image_by_line * (self.size_factor * 3 + 10) - 10,
                       (len(self.images) // self.image_by_line + 1) * (self.size_factor * 2 + 10) - 10,
                       Qt.KeepAspectRatio)

    def update_scene_selection(self):
        x = self.selected_image_index % self.image_by_line * (self.size_factor * 3 + 10)
        y = self.selected_image_index // self.image_by_line * (self.size_factor * 2 + 10)
        self.selection_rect.setPos(x, y)

    def mousePressEvent(self, event):
        position = event.pos()
        scene_pos = self.mapToScene(position)
        x = int(scene_pos.x()) // (self.size_factor * 3 + 10)
        y = int(scene_pos.y()) // (self.size_factor * 2 + 10)
        if x >= 0 and y >= 0 and x < self.image_by_line and x + y * self.image_by_line < len(self.images):
            self.selected_image_index = x + y * self.image_by_line
            print(self.selected_image_index)
            self.update_scene_selection()
            self.selection_updated.emit()

    def resizeEvent(self, QResizeEvent):
        self.fit_scene_in_view()

    def set_images(self, new_images):
        self.images = new_images
        self.scene.clear()
        self.pixmap_dict = dict()
        self.selected_image_index = 0
        self.update_scene()