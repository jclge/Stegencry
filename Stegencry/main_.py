#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m════════════════════════════m═m════╣
#╠════ File name: main.py                  ║
#╠═══ Description: Everything              ║
#╚═════════════════════════════════════════╝

from PIL import Image, ImageDraw
from copy import deepcopy
from sys import stderr, argv
import Crypto.Util.number
import numpy as np, random
from random import randint, shuffle, seed

class NoFileException(Exception):
    pass

class InvalidFileException(Exception):
    def __init__(self, error="unkown", message="Error [10]: File may not be an image, does not exist, is corrupted or has an unsupported format. Pillow exception :"):
        message = ' '.join([message, str(error)])
        super().__init__(message)

class SmallerSlaveException(Exception):
    def __init__(self, message="Error [24]: The slave image is smaller than the master."):
        super().__init__(message)

class OutputNotSetException(Exception):
    def __init__(self, message="Error [31]: output name has not been set."):
        super().__init__(message)

class MasterNotSetException(Exception):
    def __init__(self, message="Error [32]: no Image has been set as master."):
        super().__init__(message)

class NoKeyException(Exception):
    def __init__(self, function="unknown", message="Error [33]: No key has been given to Stegencry before"):
        self.message = ' '.join([message, function, "call."])
        super().__init__(self.message)

class KeyBadFormatException(Exception):
    def __init__(self, message="Error [23]: Key badly formated. A key has to be a string and generated by Stegencry."):
        super().__init__(message)

class ImageGenerator:
    ### Algorithm of this function taken from Nathan Reed on his website reedbeta.com and modified to fit the project
    def __init__(self, master, slave):
        self.__get_vectors_dirs(master)
        self.__set_array_vectors()
        self.__set_depth()
        self.__functions = [(0, self.__randColor),
            (0, self.__getX),
            (0, self.__getY),
            (1, np.sin),
            (1, np.cos),
            (2, np.add),
            (2, np.subtract),
            (2, np.multiply),
            (2, self.__safeDivide)]

    def __get_vectors_dirs(self, master):
        size = max(master.get_size())
        self.__dX, self.__dY = size, size

    def __set_array_vectors(self):
        self.__xArray = np.linspace(0.0, 1.0, self.__dX).reshape((1, self.__dX, 1))
        self.__yArray = np.linspace(0.0, 1.0, self.__dY).reshape((self.__dY, 1, 1))

    def __set_depth(self):
        self.__depthMin = randint(5,7)
        self.__depthMax = randint(9,12)

    def __randColor(self):
        return np.array([random.random(), random.random(), random.random()]).reshape((1, 1, 3))

    def __getX(self):
        return self.__xArray

    def __getY(self):
        return self.__yArray

    def __safeDivide(self, a, b):
        return np.divide(a, np.maximum(b, 0.001))

    def __buildImg(self, depth = 0):
        funcs = [f for f in self.__functions if
                    (f[0] > 0 and depth < self.__depthMax) or
                    (f[0] == 0 and depth >= self.__depthMin)]
        nArgs, func = random.choice(funcs)
        args = [self.__buildImg(depth + 1) for n in range(nArgs)]
        return func(*args)

    def generate(self):
        img = self.__buildImg()
        img = np.tile(img, (int(self.__dX / img.shape[0]), int(self.__dY / img.shape[1]), int(3 / img.shape[2])))
        return (np.uint8(np.rint(img.clip(0.0, 1.0) * 255.0)))

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
        self.__get_map()


class SetupKey:
    def __init__(self):
        self.__key = None
        self.__alphabet = list(map(chr, range(103, 123)))

    def _set_key(self, key):
        self.__key = key
        if (self.__key == None):
            return (None, None, None, None)
        else:
            self.__check_key_integrity()
            return (self.__get_key_elements())

    def __split_key_elements(self):
        res = []
        tmp = []
        for i in range(len(self.__key)):
                if self.__key[i] in self.__alphabet or self.__key[i] == '=':
                    tmp = ''.join(tmp)
                    if res == []:
                        res.append(tmp)
                    else:
                        res.append(tmp[1:])
                    tmp = []
                    pass
                tmp.append(self.__key[i])
        return (res)

    def __get_key_elements(self):
        res = self.__split_key_elements()
        try:
            rgb_seed = int(res[0], 16)
            iter_mult = int(res[1])
            pixels_seed = int(res[2], 16)
            return (self.__key, rgb_seed, iter_mult, pixels_seed)
        except:
            raise KeyBadFormatException

    def __check_key_integrity(self):
        if (type(self.__key) != str):
            raise KeyBadFormatException
        if (len(self.__key) != 1540 or
        self.__key[len(self.__key) - 1] != '=' or
        self.__key[514] not in self.__alphabet):
            raise KeyBadFormatException

    def __generate_prime_key(self, bits):
        p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        q = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        return(p*q)

    def _generate_key(self):
        rgb_seed = self.__generate_prime_key(1024)
        iter_mult = int(randint(5, 10))
        pixels_seed = self.__generate_prime_key(2048)
        key = str(hex(rgb_seed))[2:] + self.__alphabet[randint(0, 18)] + str(iter_mult) + self.__alphabet[randint(0, 18)] + str(hex(pixels_seed))[2:] + '='
        return (key, rgb_seed, iter_mult, pixels_seed)


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
        self._map_slave = self._master.open(slave)

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