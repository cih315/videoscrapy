from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class MySpider(CrawlSpider):
    name = 'book_coay'
    allowed_domains = ['coay.com']
    start_urls = ['http://www.coay.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        Rule(SgmlLinkExtractor(allow=('catalog\.php\?id=\d+')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='left']/div[@class='c_box']")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = "".join(site.select("div[@class='r_b']/div/a/text()").extract())
            #item['sort_index'] = site.select("dt[@class='video-title']/em/text()").extract()[0].replace('.','').strip()
            item['score'] = 0 
            item['sec_classify'] = "".join(hxs.select("//div[@id='left']/h2/text()").extract()) 
            item['sec_classify_name'] = hxs.select("//div[@id='left']/h2/text()").extract() 
            item['introduction'] = "" 
            item['thumbnail'] = "".join(hxs.select("//div[@id='left']/div[2][@class='c_box']/div[1][@class='l_b']/a/img/@src").extract()) 
            item['director'] = " ".join(site.select("div[@class='r_b']/div[@class='author']/text()").extract()) 



            #detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            #request = Request(detail_url,callback=self.parse_detail)
            #request.meta['item'] = item
            #items.append(request)
            items.append(item)
            

        for link in hxs.select("//div[@id='left']/div/a"):
            if link.select("text()").extract()[0] == u'\u4e0b\u4e00\u9875':
                url = "http://www.coay.com" + link.select("@href").extract()[0]
                items.append(Request(url,callback=self.parse_item))

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
