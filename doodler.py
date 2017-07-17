#!/usr/bin/python

import sys
import random
from PIL import Image
from PIL import ImageOps

# get_alpha returns alpha layer of image or None if there is no alpha layer
def get_alpha(image):
    try:
        return image.split()[image.getbands().index('A')]
    except ValueError:
        return None

# doodle doodles given images on canvas of given size
# and returns PIL.Image object
def doodle(size, images, background_color="white"):
    X_OVERLAP=0.2
    Y_OVERLAP=0.35
    if type(size) is not tuple or size <= (0, 0):
        raise ValueError('size must be type like this: (width, height)')
    if len(images) == 0:
        raise ValueError('images list is empty')
    d = Image.new('RGBA', size)
    d.paste(background_color)

    off_x, off_y = 0, 0
    while True:
        img = random.choice(images)
        n_w = int(img.width*(1-X_OVERLAP))
        n_x = off_x + n_w
        n_y = int(off_y + img.height*(1-Y_OVERLAP))
        if d.height < n_y:
            break
        if d.width < n_x:
            off_x = 0
            off_y = n_y
        if random.choice([True, False]):
            img = ImageOps.mirror(img)
        mask = get_alpha(img)
        d.paste(img, (off_x, off_y), mask)
        off_x += n_w
    return d

def open_images(names):
    imgs = []
    for n in names:
        imgs.append(Image.open(n))
    return imgs


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        imgs = open_images(args[2:])
        d = doodle((int(args[0]), int(args[1])), imgs)
        d.save('doodle.png')
    except:
        print("Usage: doodler.py <width> <height> <image1>[,<image2>[,<image3>,...]]")
        print("Resulting image will be saved as 'doodle.png'")


