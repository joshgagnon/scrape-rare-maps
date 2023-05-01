from PIL import Image
import glob

x_size = 18 #64
y_size = 48
img = Image.new('RGB', (x_size * 256, y_size * 256))

for x in range(1, x_size):
    for y in range(1, y_size):
        tile = Image.open('./tile/%d_%d.jpg' % (x, y))
        img.paste(im=tile, box=((x-1) * 256, (y-1) * 256))

img.save('./output.jpg')
