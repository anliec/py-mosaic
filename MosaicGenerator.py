#!/usr/bin/python3.6
from PIL import Image
import database


def mosaic_generator(path_to_model, number_of_images_x, number_of_images_y):
    model_im = Image.open(path_to_model)
    model_im = model_im.resize((3*number_of_images_x, 2*number_of_images_y))

    best_pictures = dict()
    db = database.DataBase()

    for x in range(0, number_of_images_x):
        for y in range(0, number_of_images_y):
            target_pixels = pixels_from_part(model_im, x, y)
            best_pictures[(x, y)] = db.get_bests_candidates(target_pixels)
    db.close()
    return best_pictures


def pixels_from_part(image, x, y):
    box = (x*3, y*2, x*3+3, y*2+2)
    region = image.crop(box)
    return list(region.getdata())


def montage(best_pictures, number_of_image_xy, size_images):
    background_size = (number_of_image_xy[0]*size_images[0], number_of_image_xy[1]*size_images[1])
    background = Image.new('RGB', background_size, (255, 255, 255))
    for key, value in best_pictures.items():
        x, y = key
        image_path = value[0][1]
        image = Image.open(image_path)
        image = image.resize(size_images)
        offset = (x*size_images[0], y*size_images[1])
        background.paste(image, offset)
    return background
