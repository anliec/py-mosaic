#!/usr/bin/python3.6
import os


def FindPhotos(search_path):
    '''Get pictures files in the given folder

    :return a list of tuple: directory, list of picture file in this directory'''
    file_found = []

    for filesTuple in os.walk(search_path):
        files_names = []
        for fileName in filesTuple[2]:
            extension = os.path.splitext(fileName)[1]
            extension = extension.lower()
            if extension in [".png", ".jpg"]:
                files_names.append(fileName)
        if len(files_names) != 0:
            file_found.append([filesTuple[0], files_names])

    return file_found

