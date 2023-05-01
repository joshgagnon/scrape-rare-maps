from PIL import Image
import sys

im = Image.open(sys.argv[1])

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((im.size[0]-1,im.size[1]-1)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


trim(im).save('trimmed.jpg')