from PIL import Image
from copy import deepcopy
import base64
from sys import stderr
import Crypto.Util.number
import numpy as np, random
from random import randint, shuffle, seed

class _stegencry:
    def __init__(self):
        self._letters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
        self._master = None
        self._map_master = None
        self._slave = None
        self._map_slave = None
        self._rgb_seed = None
        self._output = None
        self._iter_mult = None
        self._pixels_seed = None
        self._pixels = None
        self._key = None

    def set_master(self, master):
        self._master = Image.open(master)
        self._map_master = self._master.load()
        self._pixels = list(self._master.getdata())

    def set_slave(self, slave):
        self._slave = Image.open(slave)
        self._map_slave = self._slave.load()

    def set_output(self, output):
        self._output = output

    def __get_key_elements(self):
        res = []
        tmp = []
        for i in range(len(self._key)):
            if self._key[i] in self._letters or self._key[i] == '=':
                tmp = ''.join(tmp)
                if res == []:
                    res.append(tmp)
                else:
                    res.append(tmp[1:])
                tmp = []
                pass
            tmp.append(self._key[i])
        self._rgb_seed = int(res[0], 16)
        self._iter_mult = int(res[1])
        self._pixels_seed = int(res[2], 16)

    def set_key(self, key):
        self._key = key
        self.__get_key_elements()

    def print_key(self):
        print(self._key)

    def __generate_prime_key(self, bits):
        p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        q = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        return(p*q)

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

    def _bin_to_int(self, rgb):
        if (len(rgb) == 3):
            r, g, b = rgb
        elif (len(rgb) == 4):
            r, g, b, a = rgb
        return (int(r, 2), int(g, 2), int(b, 2))

    def generate_key(self):
        self._rgb_seed = self.__generate_prime_key(1024)
        self._iter_mult = int(randint(5, 10))
        self._pixels_seed = self.__generate_prime_key(2048)
        self._key = str(hex(self._rgb_seed))[2:] + self._letters[randint(0, 18)] + str(self._iter_mult) + self._letters[randint(0, 18)] + str(hex(self._pixels_seed))[2:] + '='

class encrypt(_stegencry):
    def __generate_image(self):
        ### Code/algorithm of this function taken from Nathan Reed on his website reedbeta.com and modified to fit the project
        dX, dY = max(self._master.size[0], self._master.size[1]), max(self._master.size[0], self._master.size[1])
        print(dX, dY)
        xArray = np.linspace(0.0, 1.0, dX).reshape((1, dX, 1))
        yArray = np.linspace(0.0, 1.0, dY).reshape((dY, 1, 1))
        def randColor():
            return np.array([random.random(), random.random(), random.random()]).reshape((1, 1, 3))
        def getX():
            return xArray
        def getY():
            return yArray
        def safeDivide(a, b):
            return np.divide(a, np.maximum(b, 0.001))
        functions = [(0, randColor),
             (0, getX),
             (0, getY),
             (1, np.sin),
             (1, np.cos),
             (2, np.add),
             (2, np.subtract),
             (2, np.multiply),
             (2, safeDivide)]
        depthMin = 2
        depthMax = 10
        def buildImg(depth = 0):
            funcs = [f for f in functions if
                        (f[0] > 0 and depth < depthMax) or
                        (f[0] == 0 and depth >= depthMin)]
            nArgs, func = random.choice(funcs)
            args = [buildImg(depth + 1) for n in range(nArgs)]
            return func(*args)
        img = buildImg()
        img = np.tile(img, (dX / img.shape[0], dY / img.shape[1], 3 / img.shape[2]))
        img8Bit = np.uint8(np.rint(img.clip(0.0, 1.0) * 255.0))
        self._slave = Image.fromarray(img8Bit)
        self._map_slave = self._slave.load()

    def steganography(self):
        if (self._slave == None):
            self.__generate_image()
        res = Image.new(self._slave.mode, self._slave.size)
        new_image = res.load()
        for x in range(self._slave.size[0]):
            for y in range(self._slave.size[1]):
                rgb1 = self._int_to_bin(self._map_slave[x, y])
                rgb2 = (0, 0, 0)
                if (x < self._master.size[0] and y < self._master.size[1]):
                    rgb2 = self._int_to_bin(self._map_master[x, y])
                rgb = self._merge_rgb(rgb1, rgb2)
                new_image[x, y] = self._bin_to_int(rgb)
        res.save(self._output)

    def __get_gradient_2d(self, start, stop, width, height, is_horizontal):
        if is_horizontal:
            return np.tile(np.linspace(start, stop, width), (height, 1))
        else:
            return np.tile(np.linspace(start, stop, height), (width, 1)).T

    def __get_gradient_3d(self, width, height, start_list, stop_list, is_horizontal_list):
        result = np.zeros((height, width, len(start_list)), dtype=np.float)

        for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
            result[:, :, i] = self.__get_gradient_2d(start, stop, width, height, is_horizontal)

        return result

    def __w_seed_rgb(self, rgb, rgb_enc):
        if (len(rgb) == 3):
            r, g, b = rgb
        else:
            r, g, b, a = rgb
        r = deepcopy(rgb_enc[r])
        g = deepcopy(rgb_enc[g])
        b = deepcopy(rgb_enc[b])
        return (r, g, b)

    def shuffle_pixels(self):
        for _ in range(self._iter_mult):
            seed(self._pixels_seed)
            shuffle(self._pixels)

    def encrypt_rgb(self):
        rgb_encryption = list(range(0, 256))
        seed(self._rgb_seed)
        shuffle(rgb_encryption)
        i = 0
        while (i != len(self._pixels)):
            self._pixels[i] = deepcopy(self.__w_seed_rgb(self._pixels[i], rgb_encryption))
            i += 1

    def save_image(self):
        res = Image.new(self._master.mode, self._master.size)
        res.putdata(self._pixels)
        res.save(self._output)

    def __print_key(self):
        print(self._key)

class decrypt(_stegencry):
    def save_image(self):
        res = Image.new(self._master.mode, self._master.size)
        res.putdata(self._pixels)
        res.save(self._output)

    def unshuffle_pixels(self):
        Order = list(range(len(self._pixels)))
        seed(self._pixels_seed)
        shuffle(Order)
        res = []
        for element in self._pixels:
            res.append(0)
        i = 0
        for y in range(self._iter_mult):
            for element in self._pixels:
                res[Order[i]] = deepcopy(element)
                i += 1
            self._pixels = deepcopy(res)
            i = 0

    def __decrypt_rgb(self, pixel, rgb_enc):
        if len(pixel) == 3:
            r, g, b = pixel
        elif len(pixel) == 4:
            r, g, b, a = pixel
        r = deepcopy(rgb_enc.index(r))
        g = deepcopy(rgb_enc.index(g))
        b = deepcopy(rgb_enc.index(b))
        return (r, g, b)

    def steganography(self):
        new_image = Image.new(self._master.mode, self._master.size)
        pixels_new = new_image.load()
        original_size = self._master.size
        for i in range(self._master.size[0]):
            for j in range(self._master.size[1]):
                r, g, b = self._int_to_bin(self._map_master[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')
                pixels_new[i, j] = self._bin_to_int(rgb)
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
        new_image.save(self._output)

    def decrypt_rgb(self):
        rgb_encryption = list(range(0, 256))
        seed(self._rgb_seed)
        shuffle(rgb_encryption)
        for i in range(len(self._pixels)):
            self._pixels[i] = deepcopy(self.__decrypt_rgb(self._pixels[i], rgb_encryption))