from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class Spider(CrawlSpider):
    name = 'shows'
    allowed_domains = ['v.360.cn']
    start_urls = ['http://v.360.cn']

    rules = (
        Rule(SgmlLinkExtractor(allow=('zongyi/index\.php')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='bd']//div[@class='content gclearfix']/div[@class='video-list gclearfix']/dl[@class='section variety']")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("dt[@class='video-title']/a/text()").extract()
            item['sort_index'] = site.select("dt[@class='video-title']/em/text()").extract()[0].replace('.','').strip()
            item['score'] = 0 
            detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            items.append(request)
            #items.append(item)
        #link = hxs.select("//div[@id='gpage']/a[@class='page-next']/@href").extract()
        #if link:
        #    items.append(Request(link[0],callback=self.parse_item))

        return items

    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        site = hxs.select("//div[@id='bd']")
        video_list = site.select("//div[@class='content']/div[@class='content-bd gclearfix']/dl")
        item['video_url'] = video_list.select("dd[@class='poster']/a[@class='play_btn']/@href").extract() 
        item['video_name'] = video_list.select("dt/a/text()").extract() 
        item['video_introduction'] =  video_list.select("dd[@class='poster']/a[@class='play_btn']/div[2]").extract() 
        item['video_thumbnail'] = video_list.select("dd[@class='poster']/a[@class='play_btn']/img/@src").extract() 
        item['introduction'] = site.select("div[@class='span17']/div[@id='info']/div[2][@class='info-bd']/div[@class='intro gclearfix']/p[@id='part-intro']/text()").extract() 
        item['thumbnail'] = site.select("div[@id='left_info']/div[@id='poster']/a[@class='play_btn']/img/@src").extract() 
        item['publish_time'] = ""        
        item['director'] = " ".join(site.select("div[@id='left_info']/div[@id='otherinfo']/p[2]/span[@class='text']/text()").extract()) 
        item['actors'] = "" 
        item['area'] = site.select("div[@id='left_info']/div[@id='otherinfo']/p[4]/span[@class='text']/text()").extract() 
        item['sec_classify_name'] = "".join(site.select("div[@id='left_info']/div[@id='otherinfo']/p[3]/span[@class='text']/text()").extract()) 
        item['video_view_cnt'] = 0 

        return item 
