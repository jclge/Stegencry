from PIL import Image
from copy import deepcopy
from sys import argv, stderr
import Crypto.Util.number
from random import randint, shuffle, seed

def __int_to_bin(rgb):
    if (len(rgb) == 3):
        r, g, b = rgb
    elif (len(rgb) == 4):
        r, g, b, a = rgb
    return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))

def __merge_rgb(rgb1, rgb2):
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

def __bin_to_int(rgb):
    if (len(rgb) == 3):
        r, g, b = rgb
    elif (len(rgb) == 4):
        r, g, b, a = rgb
    return (int(r, 2), int(g, 2), int(b, 2))


def unmerge(img, output, key):
        img = Image.open(img)
        pixel_map = img.load()
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()
        original_size = img.size
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = __int_to_bin(pixel_map[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')
                pixels_new[i, j] = __bin_to_int(rgb)
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
        new_image.save(output)
        map_new = new_image.load()
        _decrypt(output, key)

def encrypt_rgb(rgb, rgb_enc):
    if (len(rgb) == 3):
        r, g, b = rgb
    else:
        r, g, b, a = rgb
    r = deepcopy(rgb_enc[r])
    g = deepcopy(rgb_enc[g])
    b = deepcopy(rgb_enc[b])
    return (r, g, b)


def generate_key(bits):
    p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
    q = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
    N=p*q
    return(N)

def _encrypt(img, map_img, output):
    letters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    rgb_encryption = []
    rgb_seed_ = generate_key(1024)
    rgb_seed = deepcopy(rgb_seed_)
    rgb_encryption = list(range(0, 256))
    seed(rgb_seed)
    shuffle(rgb_encryption)
    # print(rgb_encryption)
    # shuffle_list_seed = generate_key(1024)
    # rgb_encrypt = deepcopy(rgb_encryption)
    # seed(shuffle_list_seed)
    # shuffle(rgb_encrypt)

    e = int(randint(5, 10))
    f = generate_key(2048)
    key = str(hex(rgb_seed_))[2:] + letters[randint(0, 18)] + str(e) + letters[randint(0, 18)] + str(hex(f))[2:] + '='
    print(key)
    res = Image.new(img.mode, img.size)
    pixels = list(img.getdata())
    i = 0
    while (i != len(pixels)):
        pixels[i] = deepcopy(encrypt_rgb(pixels[i], rgb_encryption))
        i += 1
    seed(f)
    for x in range(e):
        shuffle(pixels)
        seed(f)
    res.putdata(pixels)
    res.save(output)

def decrypt_rgb(rgb, rgb_enc):
    if (len(rgb) == 3):
        r, g, b = rgb
    elif (len(rgb) == 4):
        r, g, b, a = rgb
    r = deepcopy(rgb_enc.index(r))
    g = deepcopy(rgb_enc.index(g))
    b = deepcopy(rgb_enc.index(b))
    return (r, g, b)

def _decrypt(output, key):
    img = Image.open(output)
    letters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    tmp = ""
    keys = []
    for letter in key:
        if (letter in letters):
            if (len(keys) == 1):
                keys.append(int(tmp))
            else:
                keys.append(int(tmp, 16))
            tmp = ""
        else:
            tmp += letter
    keys.append(tmp)
    rgb_encryption = []
    rgb_seed = keys[0]
    rgb_encryption = list(range(0, 256))
    seed(rgb_seed)
    shuffle(rgb_encryption)
    tmp = deepcopy(list(img.getdata()))
    keys[2] = keys[2].replace('=', '')
    res = Image.new(img.mode, img.size)
    i = 0
    Order = list(range(len(tmp)))
    seed(int(keys[2], 16))
    shuffle(Order)
    to_save = []
    for element in tmp:
        to_save.append(0)
    for y in range(int(keys[1])):
        for element in tmp:
            to_save[Order[i]] = deepcopy(element)
            i+=1
        tmp = deepcopy(to_save)
        i = 0
    i = 0
    while (i != len(to_save)):
        to_save[i] = deepcopy(decrypt_rgb(to_save[i], rgb_encryption))
        i+=1
    res.putdata(to_save)
    res.save(output)

def merge(input_to_hide, input_dest_, output):
    input_to_hide = Image.open(input_to_hide)
    input_dest = Image.open(input_dest_)
    map_input_hide = input_to_hide.load()
    map_input_dest = input_dest.load()
    _encrypt(input_dest, map_input_dest, "tmp.png")
    input_dest = Image.open("tmp.png")
    map_input_dest = input_dest.load()
    res = Image.new(input_to_hide.mode, input_to_hide.size)
    new_image = res.load()

    for x in range(input_to_hide.size[0]):
        for y in range(input_to_hide.size[1]):
            rgb1 = __int_to_bin(map_input_hide[x, y])
            rgb2 = (0, 0, 0)
            if (x < input_dest.size[0] and y < input_dest.size[1]):
                rgb2 = __int_to_bin(map_input_dest[x, y])
            rgb = __merge_rgb(rgb1, rgb2)
            new_image[x, y] = __bin_to_int(rgb)
            #print(new_image[x, y])

    res.save(output)

def main(av):
    if (av[1] == 'merge'):
        merge(av[2], av[3], av[4])
    elif (av[1] == 'unmerge'):
        unmerge(av[2], av[3], av[4])

if __name__ == '__main__':
    main(argv)