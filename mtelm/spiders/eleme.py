# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

from scrapy.spiders import CrawlSpider
from mtelm.items import MtelmCatItem,MtelmSortItem,MtelmFbItem


class ElemeCategorySpider(CrawlSpider):
    '''获取饿了么平台，商品分类'''
    name = 'eleme_cat'

    custom_settings = {
        'ITEM_PIPELINES':{
        'mtelm.pipelines.MtelmPipeline': 300    
            }
        }
    start_urls=['https://h5.ele.me/restapi/shopping/v2/restaurant/category',
                'https://h5.ele.me/restapi/shopping/v1/restaurants/outside_filter/attributes',
                'https://h5.ele.me/restapi/shopping/v1/restaurants/filter-bar/attributes',
                ]
    headers = {
        'referer': 'https://h5.ele.me/msite/food/'       
        }
    params = {'latitude':'30.59086','longitude':'114.273655'}
    def start_requests(self):
        return self.make_requests_from_url(self.start_urls)   

    def make_requests_from_url(self,urls):
        for url in urls:
            yield scrapy.http.FormRequest(
                url,method='get',headers=self.headers,formdata=self.params)

    def parse(self,response):
        if 'category' in response.request.url:
            items = MtelmCatItem()
            items['category'] = response.text
        elif 'outside_filter' in response.request.url:
            items = MtelmSortItem()
            items['sort'] = response.text
        elif 'filter-bar' in response.request.url:
            items = MtelmFbItem()
            items['bar'] = response.text
        yield items
        
