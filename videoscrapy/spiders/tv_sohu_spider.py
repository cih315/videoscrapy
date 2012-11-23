
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 


class MySpider(BaseSpider):
    name = 'tv_sohu'
    allowed_domains = ['sohu.com']
    start_urls = [
        'http://so.tv.sohu.com/list_p1101_p2_p3_u5185_u5730_p42012_p5_p6_p73_p82_p9-1_p101_p11.html',#leidi
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='videoData']/div[@class='vData clear']/div[@class='vInfo']")
        varea= hxs.select("//div[@id='seaKey' and @class='seaKey bord clear']/ul[3]/li[3][@class='now']/a/text()").extract()[0]
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("div[@class='vTxt']/h4/a/text()").extract()[0].replace("\t","").replace("\r","").replace("\n","")
            item['video_name'] = site.select("div[@class='txt']/h6[@class='caption']/a/text()").extract()
            item['sec_classify'] = 'all'
            item['video_url'] = site.select("div[@class='txt']/h6[@class='caption']/a/@href").extract()
            item['view_cnt'] = "".join(site.select("div[@class='vTxt']/dl/dt/em/text()").extract()[0])
            item['thumbnail'] = site.select("div[@class='vPic']/a/img/@src").extract()[0]
            item['area_name'] = varea 
            item['introduction'] = site.select("div[@class='vTxt']/p[@class='detail']/text()").extract()[0].replace("\t","").replace("\r","").replace("\n","")
            item['video_introduction'] = '' 
            item['video_thumbnail'] = item['thumbnail'] 
            item['video_view_cnt'] = 0 
            item['director'] = " , ".join(site.select("div[@class='vTxt']/p[2]/a/@title").extract()) 
            item['actors'] = " , ".join(site.select("div[@class='vTxt']/p[1]/a/@title").extract()) 
            item['score'] = "".join(site.select("div[@class='vPic']/div[@class='popInfo']/div[@class='popLay']/p[1]/strong/text()").extract()) 
            #item['publish_time'] = '' 
            item['publish_time'] = ''.join(site.select("div[@class='vTxt']/dl/dd[1]/a/text()").extract())
            
            yield item

        #for url in hxs.select("//div[@class='page-nav']/div[@class='page-nav-bar']/a[@class='page-nav-next']/@href").extract():
        #    yield Request('http://www.tudou.com/cate/'+url, callback=self.parse)
