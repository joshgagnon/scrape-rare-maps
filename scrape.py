import requests
import sys
from lxml import etree
import math
import aiohttp
import asyncio
from collections import namedtuple
from PIL import Image, ImageChops
import io


Tile = namedtuple("Tile", "x y img")
Image.MAX_IMAGE_PIXELS = 933120000

tile_url = "https://storage.googleapis.com/raremaps/img/dzi/img_%s_files/%d/%d_%d.jpg"
metadata_url = "https://storage.googleapis.com/raremaps/img/dzi/img_%s.dzi"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

def calc_zoom(width, height):
    return math.ceil(math.log(max(width, height), 2))

def get_xml(code):
    page = requests.get(metadata_url % code, headers=headers)
    return etree.fromstring(page.content)

def parse_xml(xml):
    image = xml.find('.')
    attributes = dict(image.attrib)
    attributes.update(dict(image.getchildren()[0].attrib))
    for cast in ['Overlap', 'TileSize', 'Width', 'Height']:
        attributes[cast] = int(attributes[cast])
    return attributes


async def get_tile(session, x, y, url):
    print('Getting %s' % url)
    async with session.get(url) as resp:
        result = await resp.content.read()
        print('Got %s' % url)
        return Tile(x, y, io.BytesIO(result))


async def get_tiles(attributes):
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:

        tasks = []
        for x in range(0, attributes['X']):
            for y in range(0, attributes['Y']):
                url = tile_url % (attributes['Code'], attributes['Zoom'], x, y)
                tasks.append(asyncio.ensure_future(get_tile(session, x, y, url)))

        tiles = await asyncio.gather(*tasks)
        print('Got em')
        return tiles

def stitch(attributes, tiles):
    print('Stitching')
    img = Image.new('RGB', (attributes['Width'], attributes['Height']))
    for tile in tiles:
        tile_img = Image.open(tile.img)
        img.paste(im=tile_img, box=((tile.x * attributes['TileSize']) or 1, (tile.y * attributes['TileSize']) or 1))

    bg = Image.new(img.mode, img.size, img.getpixel((img.size[0]-1,img.size[1]-1)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)  
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)  
    return img
        

async def scrapeSave(code):
    attributes = parse_xml(get_xml(code))
    attributes['Zoom'] = calc_zoom(attributes['Width'], attributes['Height'])
    attributes['X'] = int(attributes['Width'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Y'] = int(attributes['Height'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Code'] = code
    tiles = await get_tiles(attributes)
    result = stitch(attributes, tiles)
    result.save('./output.jpg')

async def scrapeBytes(code):
    attributes = parse_xml(get_xml(code))
    attributes['Zoom'] = calc_zoom(attributes['Width'], attributes['Height'])
    attributes['X'] = int(attributes['Width'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Y'] = int(attributes['Height'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Code'] = code
    tiles = await get_tiles(attributes)
    result = stitch(attributes, tiles)
    img_byte_arr = io.BytesIO()
    result.save(img_byte_arr, 'JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

if __name__ == "__main__":
    asyncio.run(scrapeSave(sys.argv[1]))
