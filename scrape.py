import requests
import json
import re
import sys
from lxml import etree
import math
import aiohttp
import asyncio
from collections import namedtuple

Tile = namedtuple("Tile", "x y img")

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
        return Tile(x, y, result)


async def get_tiles(attributes):
    connector = aiohttp.TCPConnector(limit=25)
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:

        tasks = []
        for x in range(0, 5): #attributes['X']):
            for y in range(0, 5): # attributes['Y']):
                url = tile_url % (attributes['Code'], attributes['Zoom'], x, y)
                tasks.append(asyncio.ensure_future(get_tile(session, x, y, url)))

        tiles = await asyncio.gather(*tasks)
        print('Got em')
        print(tiles)

async def scrape(code):
    attributes = parse_xml(get_xml(code))
    attributes['Zoom'] = calc_zoom(attributes['Width'], attributes['Height'])
    attributes['X'] = int(attributes['Width'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Y'] = int(attributes['Height'] / (attributes['TileSize'] - attributes['Overlap'])) + 1
    attributes['Code'] = code
    await get_tiles(attributes)

if __name__ == "__main__":
    asyncio.run(scrape(sys.argv[1]))

if None:

    page = requests.get(this_url, headers=headers)

    for x in range(0, x_size+1):
        for y in range(0, y_size+1):
            this_url = url % (x,y)
            print(this_url)
            page = requests.get(this_url, headers=headers)
            with open('./tile/%d_%d.jpg' % (zoom, x, y), "wb") as f:
                f.write(page.content)