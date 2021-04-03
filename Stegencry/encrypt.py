#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: encrypt.py               ║
#╠═══ Description: encrypt Class           ║
#╚═════════════════════════════════════════╝

from main import Stegencry
from exception_management import InvalidFileException, SmallerSlaveException, OutputNotSetException, MasterNotSetException, NoKeyException, KeyBadFormatException
from random import randint, shuffle, seed
from ImageManagement import ImageManagement
from copy import deepcopy

class encrypt(Stegencry):
    def steganography(self):
        self.__stegano_error_management()
        size_s, size_m = self.__get_sizes()
        res = self.__process_hidden_process(size_s, size_m)
        self._master.set_image(res.get_image())
        self._pixels = self._master.get_pixels()
        del res

    def __get_sizes(self):
        return (self._slave.get_size(), self._master.get_size())

    def __shuffle_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException
        if (self._key == None):
            raise NoKeyException("shuffle_pixels")

    def __shuffle(self):
        for _ in range(self._iter_mult):
            seed(self._pixels_seed)
            shuffle(self._pixels)

    def shuffle_pixels(self):
        self.__shuffle_error_management()
        self.__shuffle()
        self._master.set_pixels(self._pixels)
        self._map_master = self._master.get_map()

    def __encrypt_rgb_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException
        if (self._key == None):
            raise NoKeyException("encrypt_rgb")

    def __w_seed_rgb(self, rgb, rgb_enc):
        if (len(rgb) == 3):
            r, g, b = rgb
        else:
            r, g, b, a = rgb
        r = deepcopy(rgb_enc[r])
        g = deepcopy(rgb_enc[g])
        b = deepcopy(rgb_enc[b])
        return (r, g, b)

    def __shuffle_rgb(self):
        rgb_encryption = list(range(0, 256))
        seed(self._rgb_seed)
        shuffle(rgb_encryption)
        return (rgb_encryption)

    def __process_rgb_encryption(self, rgb_encryption):
        for i in range(len(self._pixels)):
            self._pixels[i] = deepcopy(self.__w_seed_rgb(self._pixels[i], rgb_encryption))

    def encrypt_rgb(self):
        self.__encrypt_rgb_error_management()
        rgb_encryption = self.__shuffle_rgb()
        self.__process_rgb_encryption(rgb_encryption)

    def __process_hidden_process(self, size_s, size_m):
        res = ImageManagement()
        res.create(self._master.get_mode(), self._slave.get_size())
        loaded_s = res.get_load()
        for x in range(size_s[0]):
            for y in range(size_s[1]):
                rgb1 = self._int_to_bin(self._map_slave[x, y])
                rgb2 = self._int_to_bin([0, 0, 0])
                if (x < size_m[0] and y < size_m[1]):
                    rgb2 = self._int_to_bin(self._map_master[x, y])
                rgb = self._merge_rgb(rgb1, rgb2)
                loaded_s[x, y] = self._bin_to_int(rgb)
        return (res)

    def __stegano_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException
        if (self._map_slave == None):
            self._slave.generate_image(self._master)
            self._map_slave = self._slave.get_map()
        elif (self._slave.get_size()[0] < self._master.get_size()[0] or
            self._slave.get_size()[1] < self._master.get_size()[1]):
            raise SmallerSlaveException