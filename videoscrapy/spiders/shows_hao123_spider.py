
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 
import re

from selenium import selenium
import time
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver

class ShowsHaoSpider(BaseSpider):
    name = 'shows_hao123'
    allowed_domains = ['hao123.com']
    start_urls = [
        'http://video.hao123.com/zongyi_index/area-_type-',
    ]
  
    def __init__(self):
        self.sort_index = 0

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='subtamasha_show' and @class='mod-picarea']/div[@class='pa-normal']/div[@class='pa-normal-list']/ul[@class='video-item-list']/li")

        for site in sites:
            item = VideoItem()
            item['area_name'] = re.sub("[\w\s]+","",site.select("a/@d-area").extract()[0]).replace("%","").replace("-","").strip() 
            item['name'] = "".join(site.select("a/@d-title").extract())
            item['introduction'] = "".join(site.select("a/@d-intro").extract())
            item['thumbnail'] = "".join(site.select("a/img/@src").extract())
            sec = "".join(re.sub("[\w\s]+","",site.select("a/@d-type").extract()[0])).replace("%","").replace("-","").strip()
            item['sec_classify_name'] = sec.split(",") 
            item['sec_classify'] = sec 
            item['director'] = ",".join(site.select("div[@class='v-desc']/dl/dd[@class='v-s-actor']/a/text()").extract())
            item['actors'] = "" 
            item['score'] = "" 
            item['publish_time'] = "" 
            item['view_cnt'] = ""
            self.sort_index = self.sort_index + 1
            item["sort_index"] = self.sort_index
            detail_url = "http://video.hao123.com"+site.select("a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            item['video_url'] = [] 
            yield request 
            #yield item 

        for link in hxs.select("//div[@class='page-navgation']/a[last()]/@href").extract():
            url = "http://video.hao123.com" + link
            yield Request(url,callback=self.parse)


    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        self.log("the detail url is"+response.url)
        site = hxs.select("//div[@id='list_desc']/div[@class='pp similarLists']/ul/li/span")
        item = response.meta['item']
        item['video_url'] = hxs.select("//div[@id='VideoPcTVMenu']/div[@class='keysC']/a/@data-href").extract()
        item['video_name'] = hxs.select("//div[@id='VideoPcTVMenu']/div[@class='keysC']/a/text()").extract()
        item['video_thumbnail'] = ['']*len(item['video_url']) 
        item['video_introduction'] = ['']*len(item['video_url'])
        item['video_sort_index'] = range(1,len(item['video_url'])+1) 
        item['video_view_cnt'] = [0]*len(item['video_url']) 

        yield item
