from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class MySpider(CrawlSpider):
    name = 'doc'
    allowed_domains = ['v.360.cn']
    start_urls = [
	'http://list.iqiyi.com/www/3/----------0--3-1-1-1---.html'
    ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        Rule(SgmlLinkExtractor(allow=('/jilupian/\w+\.html')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='bd']/div[@class='content clearfix']/div[@class='video-list gclearfix']/dl[@class='section']")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("dt[@class='video-title']/a/text()").extract()
            item['score'] = site.select("dd[@class='video-grade']/a[@class='grade-score']/text()").extract()
            detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            items.append(item)
            #items.append(request)

        #link = hxs.select("//div[@id='gpage']/a[@class='page-next']/@href").extract()
        #if len(link):
        #    items.append(Request(link[0],callback=self.parse_item))

        return items

    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        site = hxs.select("//div[@class='v-details-wrap clearfix']/dl[@class='v-details']")
        item['video_url'] = site.select("dd[@class='v-play line-b clearfix']/a/@href").extract() 
        item['video_name'] = site.select("dd[@class='v-title']/span[@id='film_name']/text()").extract() 
        item['introduction'] = site.select("dd[@class='v-main-info clearfix']/p[@class='intro']/span[1][@class='text']/text()").extract() 
        item['video_thumbnail'] = site.select("dd[@class='v-poster']/a[@class='play_btn']/img/@src").extract() 
        item['thumbnail'] = item['video_thumbnail'] 
        item['publish_time'] = site.select("dd[@class='v-main-info clearfix']/p[@class='date']/a/text()").extract()        
        item['director'] = " ".join(site.select("dd[@class='v-main-info clearfix']/p[@class='info']/a/text()").extract()) 
        actors_list = site.select("dd[@class='v-main-info clearfix']/p[@class='starring']/a/text()").extract() 
        item['actors'] = " ".join(actors_list) 
        item['area'] = site.select("dd[@class='v-other-info']/p[2][@class='item']/text()").extract() 
        item['video_view_cnt'] = 0 
        return item 
