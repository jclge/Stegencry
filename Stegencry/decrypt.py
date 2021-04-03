#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: decrypt.py               ║
#╠═══ Description: decrypt Class           ║
#╚═════════════════════════════════════════╝

from main import Stegencry
from exception_management import InvalidFileException, SmallerSlaveException, OutputNotSetException, MasterNotSetException, NoKeyException, KeyBadFormatException
from random import randint, shuffle, seed
from ImageManagement import ImageManagement
from copy import deepcopy

class decrypt(Stegencry):
    def steganography(self):
        self.__steganography_error_management()
        original_size, size = self.__get_sizes()
        res, original_size = self.__process_stegano(original_size, size)
        res.change_size(original_size)
        self._master.set_image(res.get_image())
        self._map_master = self._master.get_map()
        self._pixels = self._master.get_pixels()
        del res

    def __process_stegano(self, original_size, size):
        res = ImageManagement()
        res.create(self._master.get_mode(), self._master.get_size())
        pixels_new = res.get_load()
        for i in range(size[0]):
            for j in range(size[1]):
                r, g, b = self._int_to_bin(self._map_master[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')
                pixels_new[i, j] = self._bin_to_int(rgb)
                if (pixels_new[i, j] != (0, 0, 0)):
                    original_size = (i + 1, j + 1)
        return (res, original_size)

    def __get_sizes(self):
        return (self._master.get_size(), self._master.get_size())

    def __steganography_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException

    def unshuffle_pixels(self):
        self.__unshuffle_pixels_error_management()
        Order = self.__get_order()
        self.__unshuffle(Order)
        self._master.set_pixels(self._pixels)
        self._map_master = self._master.get_load()

    def __unshuffle(self, Order):
        res = [0] * len(self._pixels)
        for _ in range(self._iter_mult):
            for element, i in zip(self._pixels, range(len(self._pixels))):
                res[Order[i]] = deepcopy(element)
            self._pixels = deepcopy(res)

    def __unshuffle_pixels_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException
        if (self._key == None):
            raise NoKeyException("unshuffle_pixels")

    def __get_order(self):
        Order = list(range(len(self._pixels)))
        seed(self._pixels_seed)
        shuffle(Order)
        return (Order)

    def __decrypt_rgb_error_management(self):
        if (self._map_master == None):
            raise MasterNotSetException
        if (self._key == None):
            raise NoKeyException("decrypt_rgb")

    def __rgb_setup(self):
        rgb_encryption = list(range(0, 256))
        seed(self._rgb_seed)
        shuffle(rgb_encryption)
        return (rgb_encryption)

    def decrypt_rgb(self):
        rgb_encryption = self.__rgb_setup()
        for i in range(len(self._pixels)):
            self._pixels[i] = deepcopy(self.__decrypt_rgb(self._pixels[i], rgb_encryption))

    def __decrypt_rgb(self, pixel, rgb_enc):
        if len(pixel) == 3:
            r, g, b = pixel
        elif len(pixel) == 4:
            r, g, b, a = pixel
        r = deepcopy(rgb_enc.index(r))
        g = deepcopy(rgb_enc.index(g))
        b = deepcopy(rgb_enc.index(b))
        return (r, g, b)