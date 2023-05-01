from PIL import Image
import glob

x_size = 65
y_size = 49
img = Image.new('RGB', (x_size * 256, y_size * 256))

for x in range(0, x_size):
    for y in range(0, y_size):
        tile = Image.open('./tile/%d_%d.jpg' % (x, y))
        img.paste(im=tile, box=((x * 256) or 1, (y * 256) or 1 ))

img.save('./output.jpg')
