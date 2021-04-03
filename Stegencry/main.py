#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: main.py                  ║
#╠═══ Description: Stegencry Class         ║
#╚═════════════════════════════════════════╝

from exception_management import InvalidFileException, SmallerSlaveException, OutputNotSetException, MasterNotSetException, NoKeyException, KeyBadFormatException
from random import randint
from SetupKey import SetupKey
from ImageManagement import ImageManagement

class Stegencry(SetupKey):
    def __init__(self, master=None, output=None, key=None, slave=None):
        super(Stegencry, self).__init__()
        self.__init_master(master)
        self.__init_slave(slave)
        self.__init_output(output)
        self.__init_key(key)

    def __init_master(self, master):
        self._master = ImageManagement()
        if (master != None):
            self._map_master = self._master.open(master)
            self._pixels = self._master.get_pixels()
        else:
            self._map_master = None
            self._pixels = None

    def __init_key(self, key):
        self._key, self._rgb_seed, self._iter_mult, self._pixels_seed = self._set_key(key)

    def __init_slave(self, slave):
        self._slave = ImageManagement()
        if (slave != None):
            self._map_slave = self._master.open(slave)
        else:
            self._map_slave = None

    def __init_output(self, output):
        self._output = ImageManagement()
        if (output != None and self._map_master != None):
            size = self._master.get_size()
            self._output.create(self._master.get_mode(), size[0], size[1])

    def set_master(self, master):
        self._map_master = self._master.open(master)
        self._pixels = self._master.get_pixels()

    def set_slave(self, slave):
        self._map_slave = self._slave.open(slave)

    def set_output(self, output):
        self._output.set_name(output)

    def set_key(self, key):
        self.__init_key(key)

    def save_image(self):
        self._output.create(self._master.get_mode(), self._master.get_size())
        self._output.set_pixels(self._pixels)
        self._output.save()

    def generate_key(self):
        self._key, self._rgb_seed, self._iter_mult, self._pixels_seed = self._generate_key()

    def print_key(self):
        try:
            print(self._key)
        except:
            raise NoKeyException("print_key")

    def _bin_to_int(self, rgb):
        if (len(rgb) == 3):
            r, g, b = rgb
        elif (len(rgb) == 4):
            r, g, b, a = rgb
        return (int(r, 2), int(g, 2), int(b, 2))

    def _int_to_bin(self, rgb):
        if (len(rgb) == 3):
            r, g, b = rgb
        elif (len(rgb) == 4):
            r, g, b, a = rgb
        return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))

    def _merge_rgb(self, rgb1, rgb2):
        if (len(rgb1) == 3):
            r1, g1, b1 = rgb1
        elif (len(rgb1) == 4):
            r1, g1, b1, a = rgb1
        if (len(rgb2) == 3):
            r2, g2, b2 = rgb2
        elif (len(rgb2) == 4):
            r2, g2, b2, a = rgb2
        rgb = (r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4])
        return rgb