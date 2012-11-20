from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class MySpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['v.360.cn']
    start_urls = ['http://v.360.cn']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('dianying/list\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='bd']/div[@class='content clearfix']/div[@class='video-list gclearfix']/dl[@class='section']")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("dt[@class='video-title']/a/text()").extract()
            detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            #print(result)
            #yield request
            items.append(request)
        return items
        #return Request(detail_url,callback=self.parse_detail) 

    def parse_detail(self,response):
        self.log('Hi, this is an deatil item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        item['video_url'] = '112'
        return item 

