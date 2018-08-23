# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import sqlite3
import json
import re

import scrapy

from mtelm.items import FoodItem


class ElemeRest(scrapy.Spider):
    name = 'eleme_rest'

    start_urls = [r'https://h5.ele.me/restapi/shopping/v3/restaurants']
    headers = {
        'referer': 'https://h5.ele.me/msite/food/',
        # 'x-shard': 'loc=114.273655,30.59086'
            }
    params = {
        'latitude': '30.59086',
        'longitude': '114.273655',
        'keyword': '',
        'offset': '0',
        'limit': '8',
        'extras[]': ['activities', 'tags'],
        # 'extras[]': 'tags',
        'terminal': 'h5',
        'rank_id': '',
        'order_by': '6',
        # 'cost_from': '',
        # 'cost_to': '',
        'restaurant_category_ids[]': ['-100'],
        'rank_id': ''
        }
    resp = True

    def start_requests(self):
        return self.make_requests_from_url(self.start_urls[0])

    def make_requests_from_url(self, url):
        for offset in range(0, 8, 8):
            self.params['offset'] = str(offset)
            if self.resp:
                yield scrapy.FormRequest(
                    url, formdata=self.params, method='GET',
                    headers=self.headers, callback=self.parse)
            else:
                break

    def parse(self, response):
        # print(response.text)
        cont = json.loads(response.text)
        self.params['rank_id'] = cont['meta']['rank_id']
        url = r'https://h5.ele.me/restapi/batch/v2?trace=shop_detail_h5'
        params = {
            'timeout': 15000,
            'requests': {'menu':
                         {
                           'method': 'GET',
                           'url': '/shopping/v2/menu?restaurant_id=161122822\
                           &terminal=h5'
                           }
                         }
            }
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['referer'] = 'https://h5.ele.me/shop/'
        if cont['items'] == []:
            self.resp = False
            print("已到尾页")
        else:
            meta = {}
            for item in cont['items']:
                info = item['restaurant']
                meta['restaurant_id'] = info['id']
                meta['permon_order_num'] = info['recent_order_num']
                print(info['name'])
                print(info['id'])
                p = re.compile(r'(?<=id=)\w+')
                params['requests']['menu']['url'] = p.sub(
                    str(info['id']), params['requests']['menu']['url'])
                print(params)
                yield scrapy.Request(
                    url, method='POST', body=json.dumps(params),
                    headers=headers, callback=self.parse1)

    def parse1(self, response):
        # print(type(json.loads((json.loads(response.text)['menu']['body']))))
        menu = json.loads((json.loads(response.text)['menu']['body']))
        item = FoodItem()
        for i in menu:
            for j in i['foods']:
                item['name'] = j['name']
                item['rating'] = j['rating']
                item['month_sales'] = j['month_sales']
                item['price'] = j['specfoods'][0]['price']
                # del(j['specfoods'])
                # item['name'] = j['specfoods']
                yield item
        # menu = json.loads(response.text)['menu']['body'][0]
