from PIL import Image
import glob

x_size = 64
y_size = 48
img = Image.new('RGB', (x_size * 256, y_size * 256))

for x in range(0, x_size + 1):
    for y in range(0, y_size + 1):
        tile = Image.open('./tile/%d_%d.jpg' % (x, y))
        img.paste(im=tile, box=(x * 256, y * 256))

img.save('./output.jpg')
