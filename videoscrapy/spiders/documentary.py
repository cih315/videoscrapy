
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 


class DocumentarySpider(BaseSpider):
    name = 'documentary'
    allowed_domains = ['iqiyi.com']
    start_urls = [
        'http://list.iqiyi.com/www/3/----------0--3-1-1-1---.html',
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='wrapper']/div[@class='sideright']/div[@class='content_right']/div[@class='list_content']/div[@class='list0']/ul[@class='ulList jilupian']/li")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = "".join(site.select("a[@class='title']/text()").extract())
            item['thumbnail'] = site.select("div[@class='pic']/div[@class='inner']/img/@src").extract()
            item['area_name'] = '' 
            item['director'] = '' 
            item['actors'] = '' 
            item['score'] = 0  
            #item['publish_time'] = '' 
            item['publish_time'] = site.select("div[@class='txt']/ul[@class='info']/li[2]/text()").extract()
            
            detail_url = site.select("a[@class='title']/@href").extract()[0]
            self.log("detail page is "+detail_url) 
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item

            yield request 

        #for url in hxs.select("//div[@class='page']/a[@class='a1']/@href").extract():
        #    self.log("the next page is =====> "+url)
        #    yield Request(url, callback=self.parse)

    def parse_detail(self, response):
        hxs = HtmlXPathSelector(response)
        site = hxs.select("//div[@class='jlp_layout']/div[@class='jlp-left']")
        item = response.meta['item']
        item['introduction'] = "".join(hxs.select("//div[@id='j-album-more']/text()").extract()) 
        item['thumbnail'] = "".join(site.select("div[@class='ju_msg']/div[@class='pic']/p/a[@class='pic_cur']/img/@src").extract())
        item['view_cnt'] = hxs.select("//span[@id='playCount']/text()").extract()
        item['video_view_cnt'] = 0 
        item['video_name'] = hxs.select("//div[@id='j-pagelist-content']/div[@class='list_block1 align_c']/ul/li/p[@class='bt']/a/text()").extract()
        item['video_url'] = hxs.select("//div[@id='j-pagelist-content']/div[@class='list_block1 align_c']/ul/li/p[@class='bt']/a/@href").extract()
        item_list = []
        for video_list_url in hxs.select("//div[@id='j-dramalist-content']/div/text()").extract(): 
            request = Request("http://www.iqiyi.com"+video_list_url,callback=self.parse_list)
            request.meta['item'] = item 
            item_list.append(request)        

        item['video_introduction'] = item_list 
        yield item 

    def parse_list(self, response):
        #hxs = HtmlXPathSelector(response)
        print("the parse list is "+response.body)
        item = response.meta['item']
        item['video_url'] = '121'
        yield item
        
