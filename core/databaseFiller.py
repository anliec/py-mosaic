#!/usr/bin/python3.6
import os
from core import database


def explore_path(path_to_explore):
    # open DB
    db = database.DataBase()
    # explore file three starting at the given point
    for filesTuple in os.walk(path_to_explore):
        # select only pictures extension
        for fileName in filesTuple[2]:
            extension = os.path.splitext(fileName)[1]
            extension = extension.lower()
            if extension in [".png", ".jpg"]:
                full_path = os.path.abspath(filesTuple[0] + "/" + fileName)
                # add the picture to DB (size check is done in db class)
                db.add_photo(full_path)
    db.close()
