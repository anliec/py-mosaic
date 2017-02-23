#!/usr/bin/python3.6
import os
import database
import FindPhotos
import PhotosManaging
import databaseFiller
import MosaicGenerator

mosaic = MosaicGenerator.MosaicGenerator("photosForTests/_DSC0008.JPG", (15, 10))
print("mosaic set")
mosaic.found_best_images()
print("images found")
image = mosaic.montage((60, 40))

image.show()

# databaseFiller.explore_path('/home/nicolas/Images/2015')
#
# print("done")

