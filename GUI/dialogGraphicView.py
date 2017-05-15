#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DialogGraphicView(QGraphicsView):
    images = None
    selected_image_index = 0

    size_factor = None # set in MainWindow
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
        self.scene.addText(self.tr("Select a picture in the\nmain view to show\nhere the others\npossibility for\nthis position"))

    def update_scene(self):
        self.scene.clear()
        if self.images is None or len(self.images) == 0:
            return
        print("updating scene")
        n = 0
        thread_array = []
        for image in self.images:
            image_path = image[1] # 1 to get the path (0 is the score)
            image_loader = ThreadedImageSelectionLoader(image_path, self.size_factor, self.scene, self.pixmap_dict, n,
                                                        self.image_by_line)
            image_loader.start()
            thread_array.append(image_loader)
            n += 1
        self.selection_rect = self.scene.addRect(
                                    self.selected_image_index % self.image_by_line * (self.size_factor * 3 + 10),
                                    self.selected_image_index // self.image_by_line * (self.size_factor * 2 + 10),
                                    self.size_factor * 3,
                                    self.size_factor * 2)
        for thread in thread_array:
            thread.wait()
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

    def clear_scene(self):
        self.images = None
        self.scene.clear()
        self.pixmap_dict = dict()
        self.selected_image_index = 0
        self.update_scene()


class ThreadedImageSelectionLoader(QThread):
    image_path = None
    size_factor = None
    new_scene = None
    pixmap_dict = None
    n = 0
    image_by_line = 0

    def __init__(self, image_path, size_factor, new_scene, pixmap_dict, n, image_by_line):
        super(ThreadedImageSelectionLoader, self).__init__()
        self.image_path = image_path
        self.size_factor = size_factor
        self.new_scene = new_scene
        self.pixmap_dict = pixmap_dict
        self.n = n
        self.image_by_line = image_by_line

    def run(self):
        pixmap = QPixmap(self.image_path)
        pixmap = pixmap.scaled(3 * self.size_factor,
                               2 * self.size_factor)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        x = self.n % self.image_by_line
        y = self.n // self.image_by_line
        pixmap_item.setOffset(x * (self.size_factor * 3 + 10),
                              y * (self.size_factor * 2 + 10))
        self.pixmap_dict[self.n] = pixmap_item
        self.new_scene.addItem(pixmap_item)
