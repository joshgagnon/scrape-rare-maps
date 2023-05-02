from PIL import Image, ImageChops
import sys
Image.MAX_IMAGE_PIXELS = 933120000
im = Image.open(sys.argv[1])

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((im.size[0]-1,im.size[1]-1)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

if __name__ == '__main__':
    trim(im).save('trimmed.jpg')