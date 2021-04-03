#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: ImageManagement.py       ║
#╠═══ Description: ImageManagement Class   ║
#╚═════════════════════════════════════════╝

from PIL import Image, ImageDraw
from copy import deepcopy
from ImageGenerator import ImageGenerator
from exception_management import InvalidFileException, SmallerSlaveException, OutputNotSetException, MasterNotSetException, NoKeyException, KeyBadFormatException

class ImageManagement:
    def __init__(self):
        self.__image = None
        self.__map = None

    def open(self, name=""):
        try:
            self.__image = Image.open(name)
            self.__get_map()
            return (self.__map)
        except Exception as e:
            raise InvalidFileException(e)

    def __get_map(self):
        self.__map = self.__image.load()

    def __get_pixels(self):
        self.__pixels = list(self.__image.getdata())

    def create(self, mode="RGB", size=[1, 1], supplement="#FFFFFF"):
        try:
            self.__image = Image.new(mode, size)
            self.__get_map()
        except Exception as e:
            raise InvalidFileException(e)

    def set_name(self, name):
        self.__name = name

    def get_size(self):
        return (self.__image.size)

    def get_image(self):
        return (self.__image)

    def get_mode(self):
        return (self.__image.mode)

    def get_load(self):
        return(self.__image.load())

    def get_pixels(self):
        self.__get_pixels()
        return (self.__pixels)

    def change_size(self, original_size):
        self.__image = self.__image.crop((0, 0, original_size[0], original_size[1]))

    def set_image(self, _map):
        self.__image = _map
        self.__get_map()

    def show(self):
        self.__image.show()

    def set_map(self, _map):
        self.__map = _map

    def get_map(self):
        return (self.__map)

    def set_pixels(self, pixels):
        self.__image.putdata(pixels)

    def save(self):
        if (self.__name != None):
            self.__image.save(self.__name)
        else:
            raise OutputNotSetException

    def generate_image(self, master):
        gen = ImageGenerator(master, self.__image)
        self.__image = Image.fromarray(gen.generate())
        self.__image.show()
        self.__get_map()