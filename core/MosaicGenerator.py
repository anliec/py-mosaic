#!/usr/bin/python3.6
from PIL import Image
from core import database
from core import PhotosManaging
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class MosaicGenerator(QThread):
    # list of best possibility per zone
    best_images_found = dict()
    # best image per zone
    best_images_selected = dict()

    number_of_image = (0, 0)
    # model data
    model_path = ""
    model_im = None
    target_im = None

    # signals
    # selected_images_changed = pyqtSignal(int, int)
    # finished = pyqtSignal()

    # threading
    run_target = None

    def __init__(self, path_to_model, number_of_images):
        super(MosaicGenerator, self).__init__()
        self.number_of_image = number_of_images
        self.model_path = path_to_model
        self.model_im = Image.open(self.model_path)
        self.target_im = self.model_im.resize((6*self.number_of_image[0], 4*self.number_of_image[1]))

    def found_best_images(self):
        """set best_images_found with the best possible result from DB
        set the best_image_selected using the highest score"""
        self.best_images_found = dict()
        self.best_images_selected = dict()
        db = database.DataBase()
        for x in range(0, self.number_of_image[0]):
            for y in range(0, self.number_of_image[1]):
                target_pixels = self.pixels_from_model_part(x, y)
                best_list = db.get_bests_candidates(target_pixels)
                self.best_images_found[(x, y)] = best_list
                self.best_images_selected[(x, y)] = best_list[0]
                # self.selected_images_changed.emit(x, y)
        db.close()
        # self.finished.emit()

    def pixels_from_model_part(self, x, y):
        box = (x*6, y*4, x*6+6, y*4+4)
        region = self.target_im.crop(box)
        return PhotosManaging.pixelize(region)

    def montage(self, size_images):
        background_size = (self.number_of_image[0]*size_images[0], self.number_of_image[1]*size_images[1])
        background = Image.new('RGB', background_size, (255, 255, 255))
        for key, value in self.best_images_selected.items():
            x, y = key
            image_path = value[1]
            image = Image.open(image_path)
            image = image.resize(size_images)
            offset = (x*size_images[0], y*size_images[1])
            background.paste(image, offset)
        return background

    def run(self):
        if self.run_target is None:
            return
        elif self.run_target == "found_best_images":
            self.found_best_images()
        self.run_target = None

