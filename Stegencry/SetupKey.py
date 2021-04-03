#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: SetupKey.py              ║
#╠═══ Description: SetupKey Class          ║
#╚═════════════════════════════════════════╝

from exception_management import InvalidFileException, SmallerSlaveException, OutputNotSetException, MasterNotSetException, NoKeyException, KeyBadFormatException
from random import randint
import Crypto.Util.number

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