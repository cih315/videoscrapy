
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 


class OpenClassSpider(BaseSpider):
    name = 'openclass'
    allowed_domains = ['open.163.com']
    start_urls = [
        'http://open.163.com/ocw/',
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='m-t-bg']/div[@class='m-conmt']/div[@class='m-clscnt m-clscnt-3']/ul[@class='f-cb']/li/div[@class='cnt']")
        vcate = '' 
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("h5/a/text()").extract()
            item['video_name'] = site.select("div[@class='txt']/h6[@class='caption']/a/text()").extract()
            item['sec_classify'] = vcate
            item['video_url'] = site.select("div[@class='txt']/h6[@class='caption']/a/@href").extract()
            item['view_cnt'] = site.select("div[@class='txt']/ul[@class='info']/li[@class='d_nums']/span[@class='d_play']/text()").extract()
            item['thumbnail'] = site.select("div[@class='pic']/div[@class='inner']/img/@src").extract()
            item['area_name'] = '' 
            item['introduction'] = '' 
            item['video_introduction'] = '' 
            item['video_thumbnail'] = item['thumbnail'] 
            item['video_view_cnt'] = item['view_cnt'] 
            item['director'] = '' 
            item['actors'] = '' 
            item['score'] = 0  
            #item['publish_time'] = '' 
            item['publish_time'] = site.select("div[@class='txt']/ul[@class='info']/li[2]/text()").extract()
            
            yield item

