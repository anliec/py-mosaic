#!/usr/bin/python3.6
from ctypes import *
import platform


class Tile(Structure):
    _fields_ = [('name', c_char_p),
                ('score', c_int)]


class Optimiser:

    tile_list = []
    tile_array = None
    tile_dict_ret = dict()
    size_x = None
    size_y = None
    size_n = None

    def __init__(self):
        self.tile_array = None

    def set_dict(self, best_images_list_by_pos, number_of_image_xy):
        self.size_y = number_of_image_xy[1]
        self.size_x = number_of_image_xy[0]
        # n is constant : the only case were it can not have the wanted value, 21 for example,
        # is when the data base do not have that musch picture, let say 15, in that case every
        # n will be 15.
        self.size_n = len(best_images_list_by_pos[(0, 0)])
        array_size = self.size_y * self.size_x * self.size_n
        self.tile_array = (Tile * array_size)()
        i = 0
        for x in range(0, number_of_image_xy[0]):
            for y in range(0, number_of_image_xy[1]):
                tuple_list = best_images_list_by_pos[(x, y)]
                # n = 0
                for tuple_tile in tuple_list:
                    tile = Tile()
                    tile.score = tuple_tile[0]
                    tile.name = tuple_tile[1].encode('utf8')
                    self.tile_array[i] = tile
                    i += 1
                    # print("tile(" + str(x) + "," + str(y) + "," + str(n) + ") : " + tuple_tile[1])
                    # n += 1

    def call_cpp(self):
        lib = self.load_library()
        lib.python_main.argtypes = POINTER(Tile), c_int, c_int, c_int
        # lib.python_main.restype = POINTER(Tile)
        # execute cpp code (optimiser)
        lib.python_main(self.tile_array, self.size_x, self.size_y, self.size_n)
        # get result into python dict
        self.tile_dict_ret = dict()
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                tile = self.tile_array[(x*self.size_y + y)]
                self.tile_dict_ret[(x, y)] = (tile.score, tile.name.decode("utf-8"))
                print("tile("+str(x)+","+str(y)+") : "+tile.name.decode("utf-8"))
        print("compute finished !")

    def load_library(self):
        lib = None
        if platform.system() == "Linux":
            print("We are on Linux")
            lib = CDLL('cpp/TilesOptimisatorlib.so')
        elif platform.system() == "Windows":
            print("We are on Windows :(")
            lib = CDLL('cpp/TilesOptimisatorlib.dll')
        else:
            print("I'm not ready for this platform : " + platform.system())
        return lib
