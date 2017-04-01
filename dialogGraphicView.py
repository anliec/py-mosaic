#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DialogGraphicView(QGraphicsView):
    images = None
    selected_image_index = 0

    size_factor = 30
    image_by_line = 3

    scene = None
    selection_rect = None

    def __init__(self, list_of_images):
        super(DialogGraphicView, self).__init__()
        self.images = list_of_images
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.update_scene()

    def update_scene(self):
        print("scene updated")
        n = 0
        for image in self.images:
            pixmap = QPixmap(image[1]) # 1 to get the path (0 is the score)
            pixmap = pixmap.scaled(3 * self.size_factor,
                                   2 * self.size_factor)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setOffset(n % self.image_by_line * (self.size_factor * 3 + 10),
                                  n // self.image_by_line * (self.size_factor * 2 + 10))
            self.scene.addItem(pixmap_item)
            n += 1
        self.selection_rect = self.scene.addRect(
                                    self.selected_image_index % self.image_by_line * (self.size_factor * 3 + 10),
                                    self.selected_image_index // self.image_by_line * (self.size_factor * 2 + 10),
                                    self.size_factor * 3,
                                    self.size_factor * 2)

    def update_scene_selection(self):
        x = self.selected_image_index % self.image_by_line * (self.size_factor * 3 + 10)
        y = self.selected_image_index // self.image_by_line * (self.size_factor * 2 + 10)
        self.selection_rect.setPos(x, y)

    def mousePressEvent(self, event):
        position = event.pos()
        scene_pos = self.mapToScene(position)
        x = int(scene_pos.x()) // (self.size_factor * 3 + 10)
        y = int(scene_pos.y()) // (self.size_factor * 2 + 10) * self.image_by_line
        if x >= 0 and \
                        y >= 0 and \
                        x < self.image_by_line and \
                        y < len(self.images) / 3:
            self.selected_image_index = x + y
            print(self.selected_image_index)
            self.update_scene_selection()