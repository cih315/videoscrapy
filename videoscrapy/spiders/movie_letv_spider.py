
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 
import re

#from selenium import selenium
import time
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium import webdriver

class ShowsHaoSpider(BaseSpider):
    name = 'm_letv'
    allowed_domains = ['letv.com']
    start_urls = [
        #'http://so.letv.com/list/c1_t-1_a-1_y-1_f_at_o1_i-1_p.html',
        'http://so.letv.com/list/c1_t8_a-1_y-1_f_at_o1_i-1_p.html',
    ]
  
    def __init__(self):
        self.sort_index = 0

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//ol[@id='tabx_c_1' and @class='on']/div[@class='soyall']/div[@class='info2_box']")

        for site in sites:
            item = VideoItem()
            #item['area_name'] = re.sub("[\w\s]+","",site.select("a/@d-area").extract()[0]).replace("%","").replace("-","").strip() 
            item['name'] = "".join(site.select("a/img/@alt").extract())
            #item['introduction'] = "".join(site.select("a/@d-intro").extract())
            item['thumbnail'] = "".join(site.select("a/img/@src").extract())
            item['video_name'] = site.select("a/img/@alt").extract() 
            item['video_thumbnail'] = site.select("a/img/@src").extract() 
            #sec = "".join(re.sub("[\w\s]+","",site.select("a/@d-type").extract()[0])).replace("%","").replace("-","").strip()
            #item['sec_classify_name'] = sec.split(",") 
            #item['sec_classify'] = sec 
            #item['director'] = ",".join(site.select("div[@class='v-desc']/dl/dd[@class='v-s-actor']/a/text()").extract())
            item['director'] = ",".join(site.select("dl[@class='info_dl']/dd[2]/a/text()").extract()) 
            item['actors'] = ",".join(site.select("dl[@class='info_dl']/dd[3]/a/text()").extract()) 
            item['score'] = "".join(site.select("dl[@class='info_dl']/dd[@class='tit']/span[@class='fr']/span[@class='sorce']/i/text()").extract())
            item['publish_time'] = "".join(site.select("dl[@class='info_dl']/dd[@class='year_dl']/span/a/text()").extract()) 
            item['view_cnt'] = ""
            self.sort_index = self.sort_index + 1
            item["sort_index"] = self.sort_index
            item['video_url'] = site.select("dl[@class='info_dl']/dd[@class='btn_dd']/a/@href").extract() 
            item['introduction'] = "".join(site.select("dl[@class='info_dl']/dd[@class='ind24']/text()").extract()).replace("\t","") 
            item['video_introduction'] = [item['introduction']] 
            item['video_sort_index'] = [1] 
            item['video_view_cnt'] = [0] 
            item['sec_classify'] = "".join(hxs.select("//a[@id='iq' and @class='on']/text()").extract()).replace("\t","") 
            item['sec_classify_name'] = [item['sec_classify']] 
            item['area_name']=u'\u5176\u4ed6'
            #detail_url = "".join(site.select("dt/a/@href").extract())
            #request = Request(detail_url,callback=self.parse_detail)
            #request.meta['item'] = item
            #item['video_url'] = [] 
            #yield request 
            yield item 

        for link in hxs.select("//div[@class='page']/a[last()]/@href").extract():
            if link != '#':
                yield Request(link,callback=self.parse)


    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        self.log("the detail url is"+response.url)
        site = hxs.select("//div[@id='list_desc']/div[@class='pp similarLists']/ul/li/span")
        item = response.meta['item']
        item['director'] = ",".join(hxs.select("span[@id='director_areadd']/a/text()").extract()) 
        item['sec_classify_name'] = hxs.select("span[@id='cate_areadd']/a/text()").extract() 
        item['sec_classify'] = ",".join(item['sec_classify_name']) 
        item['area_name'] = hxs.select("//div[@class='T-Info']/ul[@class='text']/li/p[@class='p2']/span[@class='s2']/a/text()").extract() 
        item['video_introduction'] = "".join(hxs.select("p[@id='j-descript']/text()")) 
        item['video_sort_index'] = [1] 
        item['video_view_cnt'] = [0] 

        yield item
