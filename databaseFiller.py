#!/usr/bin/python3.6
import os
import database
import FindPhotos


def explore_path(path_to_explore):
    # open DB
    db = database.DataBase()
    file_found = []
    # explore file three starting at the given point
    for filesTuple in os.walk(path_to_explore):
        files_names = []
        # select only pictures extension
        for fileName in filesTuple[2]:
            extension = os.path.splitext(fileName)[1]
            extension = extension.lower()
            if extension in [".png", ".jpg"]:
                files_names.append(fileName)
        if len(files_names) != 0:
            file_found.append([filesTuple[0], files_names])
    files_found = FindPhotos.FindPhotos(path_to_explore)
    # add each file to the database
    for directory in files_found:
        for file in directory[1]:
            full_path = os.path.abspath(directory[0] + "/" + file)
            db.add_photo(full_path)
    db.close()
