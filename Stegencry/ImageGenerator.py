#╔════════╦═══════════════════════╦════════╗
#║        ║       Stegencry       ║        ║
#║   ___  ╚═══════════════════════╝  ___   ║
#║  (o o)                           (o o)  ║
#║ (  V  )  Julien Calenge © 2021  (  V  ) ║
#╠═══m═m═════════════════════════════m═m═══╣
#╠════ File name: ImageGenerator.py        ║
#╠═══ Description: ImageGenerator Class    ║
#╚═════════════════════════════════════════╝

import numpy as np, random
from random import randint

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