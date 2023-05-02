from flask import Flask, current_app, request, send_file
import re
from scrape import scrapeBytes
import asyncio


app = Flask(__name__)


@app.route('/')
def index():
    return current_app.send_static_file('index.html')


@app.route('/get-map', methods=['POST'])
def getmap():
    url = request.json['url']
    pattern = r'https:\/\/www.raremaps.com\/gallery\/detail\/(\d+)\/'
    result = re.search(pattern, url)
    code = result.group(1)
    file = asyncio.run(scrapeBytes(code))
    return send_file(
        file,
        download_name='raremap.jpg',
        mimetype='image/jpg'
    ), 201

if __name__ == '__main__':
    app.run()