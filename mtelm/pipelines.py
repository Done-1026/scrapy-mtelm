# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sqlite3

from mtelm.items import MtelmCatItem,MtelmSortItem,MtelmFbItem


class MtelmPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,MtelmCatItem):
            #print(item['category'])
            #print(type(item['category']))
            self.save_cat(item)
            #pass
        elif isinstance(item,MtelmSortItem):
            self.save_sort(item)
            #pass
        else :
            pass

    def open_spider(self,spider):
        self.conn = sqlite3.connect(r'mtelm\mtelm.db')
        self.c = self.conn.cursor()

    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()
        
    def save_cat(self,item):
        '''筛选出有用数据，并存入数据库，录入前删除旧数据'''
        self.c.execute("DELETE FROM cat")
        for cat in json.loads(item['category'])[1:]:
            for sub_cat in cat['sub_categories']:
                sub_cat['category'] = cat['name']
                del(sub_cat['image_url'])
                info = tuple(sub_cat.values())
                try :
                    self.c.execute("INSERT INTO cat ('count','id','level','name','category')\
                               VALUES(?,?,?,?,?)",info)
                    print(info)
                except sqlite3.IntegrityError as er:
                    #self.c.execute("DELETE FROM cat WHERE id="+str(sub_cat['id']))
                    print('id重复',info)
                
    def save_sort(self,item):
        '''筛选出有用数据，并存入数据库，录入前删除旧数据'''
        self.c.execute("DELETE FROM sort")
        for li in json.loads(item['sort']).values():
            for sort in li:
                type(sort)
                info = (sort['name'],sort['value'])
                try:
                    self.c.execute("INSERT INTO sort ('name','value') VALUES(?,?)",info)
                    print(info)
                except sqlite3.IntegrityError as er:
                    print('name重复',info)
                       
    def save_fb(self):
        pass
