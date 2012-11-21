from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class TvSpider(CrawlSpider):
    name = 'tv'
    allowed_domains = ['v.360.cn']
    start_urls = ['http://v.360.cn']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/dianshi/list\.php\?cat=\w+')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='bd container24']/div[@id='tv-index-type']/div[@class='video-list gclearfix']/dl[@class='section tv']")
        cate = hxs.select("//div[@id='screening']/div[2][@class='screening-bd']/ul[@class='kinds gclearfix']/li/a[@class='on']/text()").extract()[0]
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("dt[@class='video-title']/a/text()").extract()
            item['sort_index'] = site.select("dt[@class='video-title']/em/text()").extract()[0].replace('.','').strip()
            item['score'] = 0 
            item['sec_classify'] = cate 
            detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            items.append(request)
            #items.append(item)

        link = hxs.select("//div[@id='gpage']/a[@class='page-next']/@href").extract()
        if link:
            items.append(Request(link[0],callback=self.parse_item))

        return items

    def parse_detail(self,response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        site = hxs.select("//div[@class='v-details-wrap clearfix']/dl[@class='v-details']")
        video_list = site.select("dd[@id='tv-play']/div[@class='box']/div[1][@class='content']/div[@class='full clearfix']")
        item['video_url'] = video_list.select("a/@href").extract() 
        item['video_name'] = video_list.select("a/text()").extract() 
        item['video_introduction'] =  video_list.select("a/text()").extract() 
        item['introduction'] = site.select("dd[@class='v-main-info clearfix']/p[@class='intro']/span[1][@class='text']/text()").extract() 
        item['video_thumbnail'] = site.select("dd[@class='v-poster']/a[@class='play_btn']/img/@src").extract() 
        item['thumbnail'] = item['video_thumbnail'] 
        item['publish_time'] = site.select("dd[@class='v-other-info']/p[5][@class='item']/text()").extract()        
        item['director'] = " ".join(site.select("dd[@class='v-other-info']/p[2][@class='item']/text()").extract()) 
        actors_list = site.select("dd[@class='v-main-info clearfix']/p[@class='starring']/a/text()").extract() 
        item['actors'] = " ".join(actors_list) 
        item['area'] = site.select("dd[@class='v-other-info']/p[3][@class='item']/text()").extract() 
        item['sec_classify_name'] = "".join(site.select("dd[@class='v-other-info']/p[4][@class='item']/text()").extract()) 
        item['video_view_cnt'] = 0 
        return item 
