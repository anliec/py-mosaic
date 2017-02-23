#!/usr/bin/python3.6
import os
import database
import FindPhotos
import PhotosManaging
import databaseFiller
import MosaicGenerator


bestpictures = MosaicGenerator.mosaic_generator("photosForTests/_DSC0008.JPG", 15, 10)

result_im = MosaicGenerator.montage(bestpictures, (15, 10), (60, 40))

result_im.show()

# databaseFiller.explore_path('/home/nicolas/Images/2015')
#
# print("done")

