#!/usr/bin/python3.6
import os
import database
import FindPhotos
import PhotosManaging
import databaseFiller

databaseFiller.explore_path('/home/nicolas/Images/2015')

print("done")
#
# pathToExplore = 'photosForTests'
# fileFound = []
#
# for filesTuple in os.walk(pathToExplore):
#     filesNames = []
#     for fileName in filesTuple[2]:
#         extension = os.path.splitext(fileName)[1]
#         extension = extension.lower()
#         if extension in [".png", ".jpg"]:
#             filesNames.append(fileName)
#     if len(filesNames) != 0:
#         fileFound.append([filesTuple[0], filesNames])
# filesFound = FindPhotos.FindPhotos(pathToExplore)
#
# for directory in filesFound:
#     for file in directory[1]:
#         fullpath = os.path.abspath(directory[0] + "/" + file)
#         db.add_photo(fullpath)
#
# print(filesFound)
# db.close()
