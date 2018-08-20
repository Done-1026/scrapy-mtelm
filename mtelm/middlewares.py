# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import sys
sys.path.append('mtelm\\ProxyPool')

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from mtelm.ProxyPool import getter
from twisted.internet.error import TCPTimedOutError

from mtelm import useragent

 

class MtelmSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MtelmDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
    
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MtelmUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self,user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls,crawler):
        o = cls(user_agent=useragent.MY_USER_AGENTS)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o
    
    def process_request(self,request,spider):
        if self.user_agent:
            #print(self.user_agent)
            request.headers.setdefault(b'User-Agent',random.choice(self.user_agent))
            print(request.headers.get(b'User-Agent'))
    

class ProxyMiddleware():
    def __init__(self):
        self.slt = getter.SqliteClient('mtelm\\proxies.db','proxy')
        #self.slt.new_proxies()
        self.proxy = self.slt.get_randproxy(protocol='https')
    
    def process_request(self,request,spider):
        request.meta['proxy'] = self.proxy
        print(request.meta['proxy'])
        print('*'*30)

    def process_exception(self,request,exception,spider):
        print('#'*20)
        print(exception)
        print(type(exception))
        if isinstance(exception,RetryMiddleware.EXCEPTIONS_TO_RETRY):
            print('f'*20)
            print(self.slt.ip)
            self.slt.delete(ip=self.slt.ip)
            self.slt.commit()
            self.proxy = self.slt.get_randproxy(protocol='https')
            print(self.proxy) 
            retryreq = request.copy()
            request.meta['proxy'] = self.proxy
            request.meta['download_timeout'] = 30
            request.dont_filter = True
            return request

    def process_response(self,request,response,spider):
        print(response.status)
        print('+'*20)
        if response.status != 200:
            ip = request.meta['proxy'].split(':')[0]
            self.slt.delete(ip=ip)
            self.proxy = self.slt.get_randproxy(protocol='https')
            request.meta['proxy'] = self.proxy
            return request
        else:
            return response

        
        
