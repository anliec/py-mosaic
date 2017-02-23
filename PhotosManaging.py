#!/usr/bin/python3.6
from PIL import Image


def image_from_path(image_path):
    return Image.open(image_path)


def miniaturize(image):
    return image.resize((3, 2))


def miniature_image_pixels(image_path):
    image = image_from_path(image_path)
    image = miniaturize(image)
    return pixelize(image)


def pixelize(image):
    return list(image.getdata())


