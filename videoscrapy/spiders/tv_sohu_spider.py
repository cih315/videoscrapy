
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 
import re


class MySpider(BaseSpider):
    name = 'tv_sohu'
    allowed_domains = ['sohu.com']
    start_urls = [
        'http://so.tv.sohu.com/list_p1101_p2_p3_u5185_u5730_p42012_p5_p6_p73_p82_p9-1_p101_p11.html',#leidi
       # 'http://so.tv.sohu.com/list_p1101_p2_p3_u6e2f_u5267_p42012_p5_p6_p73_p82_p9-1_p101_p11.html',#hk
    ]
  
    def __init__(self):
        self.sort_index = 0

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='videoData']/div[@class='vData clear']/div[@class='vInfo']")
        varea= hxs.select("//div[@id='seaKey' and @class='seaKey bord clear']/ul[3]/li[@class='now']/a/text()").extract()[0]
        if varea == u'\u5185\u5730':
            varea = u'\u5927\u9646'
        if varea == u'\u6e2f\u5267':
            varea = u'\u9999\u6e2f'
           
        for site in sites:
            item = VideoItem()
            item['area_name'] = varea 
            item['name'] = site.select("div[@class='vTxt']/h4/a/text()").extract()[0].replace("\t","").replace("\r","").replace("\n","")
            item['introduction'] = site.select("div[@class='vTxt']/p[@class='detail']/text()").extract()[0].replace("\t","").replace("\r","").replace("\n","")
            item['thumbnail'] = site.select("div[@class='vPic']/a/img/@src").extract()[0]
            item['sec_classify_name'] = [] 
            item['director'] = ",".join(site.select("div[@class='vTxt']/p[2]/a/@title").extract()) 
            item['actors'] = ",".join(site.select("div[@class='vTxt']/p[1]/a/@title").extract()) 
            item['score'] = "".join(site.select("div[@class='vPic']/div[@class='popInfo']/div[@class='popLay']/p[1]/strong/text()").extract()).replace(u"\u5206","") 
            item['publish_time'] = ''.join(site.select("div[@class='vTxt']/dl/dd[1]/a/text()").extract())
            item['view_cnt'] = "".join(site.select("div[@class='vTxt']/p/em/text()").extract()[0]).replace(u"\u6b21","").replace(",","")
            self.sort_index = self.sort_index + 1
            item["sort_index"] = self.sort_index
            detail_url = site.select("div[@class='vPic']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request 
            #yield item 

        for link in hxs.select("//div[@id='contentA']/div[@class='right']/div[@class='jumpB clear']/a[@class='pa']/@href").extract():
            url = "http://so.tv.sohu.com" + link
            #url = "http://so.tv.sohu.com" + link.select("@href").extract()[0]
            if (url in self.start_urls) == False:
                yield Request(url,callback=self.parse)


    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        self.log("the detail url is"+response.url)
        site = hxs.select("//div[@id='list_desc']/div[@class='pp similarLists']/ul/li/span")
        item = response.meta['item']
        item['sec_classify'] = ",".join(hxs.select("//div[@id='contentA' and @class='area']/div[@class='right']/div[@class='blockRA bord clear']/div[@class='cont']/p[4]/a/text()").extract()) 
        item['video_name'] = site.select("strong/a/text()").extract()
        item['video_url'] = site.select("strong/a/@href").extract() 
        item['video_thumbnail'] = ['']*len(item['video_url']) 
        item['video_introduction'] = ['']*len(item['video_url']) 
        item['video_sort_index'] = range(1,len(item['video_url'])+1) 
        item['video_view_cnt'] = [0]*len(item['video_url']) 

        yield item
