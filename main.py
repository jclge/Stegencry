from PIL import Image
from copy import deepcopy
from sys import argv, stderr
import Crypto.Util.number
from random import randint, shuffle, seed

class stegencry:
    def __init__(self):
        self.letters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
        self.master = None
        self.map_master = None
        self.slave = None
        self.map_slave = None
        self.rgb_seed = None
        self.output = None
        self.iter_mult = None
        self.pixels_seed = None
        self.pixels = None
        self.key = None

    def set_master(self, master):
        self.master = Image.open(master)
        self.map_master = self.master.load()
        self.pixels = list(self.master.getdata())

    def set_slave(self, slave):
        self.slave = Image.open(slave)
        self.map_slave = self.slave.load()

    def set_output(self, output):
        self.output = output

    def __get_key_elements(self):
        res = []
        tmp = []
        for i in range(len(self.key)):
            if self.key[i] in self.letters or self.key[i] == '=':
                tmp = ''.join(tmp)
                if res == []:
                    res.append(tmp)
                else:
                    res.append(tmp[1:])
                tmp = []
                pass
            tmp.append(self.key[i])
        self.rgb_seed = int(res[0], 16)
        self.iter_mult = int(res[1])
        self.pixels_seed = int(res[2], 16)

    def set_key(self, key):
        self.key = key
        self.__get_key_elements()

    def print_key(self):
        print(self.key)

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
        self.rgb_seed = self.__generate_prime_key(1024)
        self.iter_mult = int(randint(5, 10))
        self.pixels_seed = self.__generate_prime_key(2048)
        self.key = str(hex(self.rgb_seed))[2:] + self.letters[randint(0, 18)] + str(self.iter_mult) + self.letters[randint(0, 18)] + str(hex(self.pixels_seed))[2:] + '='

class encrypt(stegencry):
    def steganography(self):
        res = Image.new(self.slave.mode, self.slave.size)
        new_image = res.load()
        for x in range(self.slave.size[0]):
            for y in range(self.slave.size[1]):
                rgb1 = self._int_to_bin(self.map_slave[x, y])
                rgb2 = (0, 0, 0)
                if (x < self.master.size[0] and y < self.master.size[1]):
                    rgb2 = self._int_to_bin(self.map_master[x, y])
                rgb = self._merge_rgb(rgb1, rgb2)
                new_image[x, y] = self._bin_to_int(rgb)
        res.save(self.output)

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
        for i in range(self.iter_mult):
            seed(self.pixels_seed)
            shuffle(self.pixels)

    def encrypt_rgb(self):
        rgb_encryption = list(range(0, 256))
        seed(self.rgb_seed)
        shuffle(rgb_encryption)
        i = 0
        while (i != len(self.pixels)):
            self.pixels[i] = deepcopy(self.__w_seed_rgb(self.pixels[i], rgb_encryption))
            i += 1

    def save_image(self):
        res = Image.new(self.master.mode, self.master.size)
        res.putdata(self.pixels)
        res.save(self.output)

    def __print_key(self):
        print(self.key)

class uncrypt(stegencry):
    def save_image(self):
        res = Image.new(self.master.mode, self.master.size)
        res.putdata(self.pixels)
        res.save(self.output)

    def unshuffle_pixels(self):
        Order = list(range(len(self.pixels)))
        seed(self.pixels_seed)
        shuffle(Order)
        res = []
        for element in self.pixels:
            res.append(0)
        i = 0
        for y in range(self.iter_mult):
            for element in self.pixels:
                res[Order[i]] = deepcopy(element)
                i += 1
            self.pixels = deepcopy(res)
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
        new_image = Image.new(self.master.mode, self.master.size)
        pixels_new = new_image.load()
        original_size = self.master.size
        for i in range(self.master.size[0]):
            for j in range(self.master.size[1]):
                r, g, b = self._int_to_bin(self.map_master[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')
                pixels_new[i, j] = self._bin_to_int(rgb)
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
        new_image.save(self.output)

    def uncrypt_rgb(self):
        rgb_encryption = list(range(0, 256))
        seed(self.rgb_seed)
        shuffle(rgb_encryption)
        for i in range(len(self.pixels)):
            self.pixels[i] = deepcopy(self.__decrypt_rgb(self.pixels[i], rgb_encryption))

def main(av):
    if (av[1] == 'merge'):
        res = encrypt()
        res.set_key("c5e75c138a6fca40efc25eeb1a8a3512b228c4dab7250abd0da8dd889a0014be0b6e4c84d50216aff266622234a758e855370f8ccd7d06c9c39139274ad8b377fb5f410fc8a445398a597a9687332a94fd7d1f1ed22022b32600b527f278c628cdf043a739b95c1446077f636ada506f28dc2bb53b04f2830e0879fbf4f1b8935088e216cadf48b3046939cff95f780eaf7154788f4095ae75c193dc26af27c2930a0a1372500c70f86a248c6e26d9e801e439fb77a69b3b20fe383d4339d3d13feebc4dee7e1d945271b57b772ad1a9fdccaa51db6842e8d2587495a93a2c039ef2b50286ce81046a058276a5411219e4db924187287174e16d4d447f95c685v5g708a17487324600401b61a27c669743c448e649f680182d1e8d09d558bd7c32c62ff7e0591d492027cde842268a4b9d66b68887ed759dbe2f2383631f4bfc8c85d3a7ff9b9c23a7f114b73baec7df3058404ae11c0787eff1b3ded45f58642e02edea69443066c6393640a6ea03984b3fbdc38eb0cd92eb4eca704491195921deeaac227d7f5df81e2dd5170ea1223943d0187d44d3d2c8d77322b0d2b4ab4e1e817775159d2810d61332216521eb43ec6153fa21c3217795de2ebd8b410e9b8588e416d3c03c4ceb153df04d8f03aad70948ee4c30cc68a647927030e3de7c9ea635faf5fa17c92d10be007b332d535bccf4cf8a3f2a8817b0112d90a5e2f028434afc0774ebd3c1e4f1885f4b241f20bfa3a711b999a340fc3f54ddeb956f5238011a0d85876d91f1534754a3fcf754d1e20ba74a4d79c2539933b80bca92fef681c0139aca142114fc5eedb8ecd15a5efde9f02c316818ad4e0b97905d517142ab6bc9e1555b5f823111921c03750fb2146430b398020fad5c5a1936636dbc344a0ad4cdae45cadcc627d7acd8b028441d3e9fe84b1f621139f667a5ae80c7f266ff068caf578eee777dce3e647193cabcecdc7b404ac5d3987f5242a6a57dd4c58fc48dfa0d2addd1c160986661fc17b75e2820b47e07b9fdedf7b53690fbfd41ce8699895e5f037cd781aa3f32e9d95b065865a12619881e900f31ced31=")
        # res.generate_key()
        # res.print_key()
        res.set_master("image1.png")
        res.set_slave("image2.png")
        res.set_output("res.png")
        res.shuffle_pixels()
        res.save_image()
        res.set_master("res.png")
        res.steganography()
        #res.save_image()
    elif (av[1] == 'unmerge'):
        res = uncrypt()
        res.set_key("c5e75c138a6fca40efc25eeb1a8a3512b228c4dab7250abd0da8dd889a0014be0b6e4c84d50216aff266622234a758e855370f8ccd7d06c9c39139274ad8b377fb5f410fc8a445398a597a9687332a94fd7d1f1ed22022b32600b527f278c628cdf043a739b95c1446077f636ada506f28dc2bb53b04f2830e0879fbf4f1b8935088e216cadf48b3046939cff95f780eaf7154788f4095ae75c193dc26af27c2930a0a1372500c70f86a248c6e26d9e801e439fb77a69b3b20fe383d4339d3d13feebc4dee7e1d945271b57b772ad1a9fdccaa51db6842e8d2587495a93a2c039ef2b50286ce81046a058276a5411219e4db924187287174e16d4d447f95c685v5g708a17487324600401b61a27c669743c448e649f680182d1e8d09d558bd7c32c62ff7e0591d492027cde842268a4b9d66b68887ed759dbe2f2383631f4bfc8c85d3a7ff9b9c23a7f114b73baec7df3058404ae11c0787eff1b3ded45f58642e02edea69443066c6393640a6ea03984b3fbdc38eb0cd92eb4eca704491195921deeaac227d7f5df81e2dd5170ea1223943d0187d44d3d2c8d77322b0d2b4ab4e1e817775159d2810d61332216521eb43ec6153fa21c3217795de2ebd8b410e9b8588e416d3c03c4ceb153df04d8f03aad70948ee4c30cc68a647927030e3de7c9ea635faf5fa17c92d10be007b332d535bccf4cf8a3f2a8817b0112d90a5e2f028434afc0774ebd3c1e4f1885f4b241f20bfa3a711b999a340fc3f54ddeb956f5238011a0d85876d91f1534754a3fcf754d1e20ba74a4d79c2539933b80bca92fef681c0139aca142114fc5eedb8ecd15a5efde9f02c316818ad4e0b97905d517142ab6bc9e1555b5f823111921c03750fb2146430b398020fad5c5a1936636dbc344a0ad4cdae45cadcc627d7acd8b028441d3e9fe84b1f621139f667a5ae80c7f266ff068caf578eee777dce3e647193cabcecdc7b404ac5d3987f5242a6a57dd4c58fc48dfa0d2addd1c160986661fc17b75e2820b47e07b9fdedf7b53690fbfd41ce8699895e5f037cd781aa3f32e9d95b065865a12619881e900f31ced31=")
        res.set_master("res.png")
        res.set_output("unres.png")
        res.steganography()
        res.set_master("unres.png")
        res.unshuffle_pixels()
        res.save_image()

if __name__ == '__main__':
    main(argv)