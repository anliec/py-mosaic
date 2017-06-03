#!/usr/bin/python3.6
from PIL import Image


def image_from_path(image_path):
    im = Image.open(image_path)
    im = im.convert("YCbCr")
    return im


def convert_to_YCbCr(image):
    return image.convert("YCbCr")


def miniaturize(image):
    return image.resize((6, 4))


def miniature_image_pixels(image_path):
    image = image_from_path(image_path)
    image = miniaturize(image)
    return pixelize(image)


def pixelize(image):
    return list(image.getdata())


