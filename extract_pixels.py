from PIL import Image
from random import randint, seed, shuffle
from copy import deepcopy

im = Image.open('image1.png', 'r')
res = Image.new(im.mode, im.size)
pixels = list(im.getdata())
SEED = 1234542
seed(SEED)
shuffle(pixels)
i = 0

res.putdata(pixels)
res.save("tmp.png")

im = Image.open("tmp.png", 'r')
res = Image.new(im.mode, im.size)
tmp = list(im.getdata())
seed(SEED)
Order = list(range(len(tmp)))
shuffle(Order)
to_save = []
for element in tmp:
    to_save.append(deepcopy(0))
for element in tmp:
    to_save[Order[i]] = element
    i+=1
res.putdata(to_save)
res.save("res.png")