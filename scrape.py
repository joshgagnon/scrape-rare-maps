import requests
import json
import re


x_size = 64
y_size = 48
url = "https://storage.googleapis.com/raremaps/img/dzi/img_72022_files/15/%d_%d.jpg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
for x in range(1, x_size):
    for y in range(1, y_size):
        page = requests.get(url % (x,y), headers=headers)
        with open('./tile/%d_%d.jpg' % (x, y), "wb") as f:
            f.write(page.content)