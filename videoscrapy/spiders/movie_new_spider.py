from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from videoscrapy.items import VideoItem

class MySpider(CrawlSpider):
    name = 'm'
    allowed_domains = ['v.360.cn']
    start_urls = ['http://v.360.cn']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        Rule(SgmlLinkExtractor(allow=('/dianying/list\.php$')), callback='parse_item'),

        #Rule(SgmlLinkExtractor(allow=('/dianying/list\.php\?cat=\w+')), callback='parse_cat'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='bd']/div[@class='content clearfix']/div[@class='video-list gclearfix']/dl[@class='section']")
        items = []
        for site in sites:
            item = VideoItem()
            item['name'] = site.select("dt[@class='video-title']/a/text()").extract()[0]
            item['sort_index'] = site.select("dt[@class='video-title']/em/text()").extract()[0].replace('.','').strip()
            item['score'] = "".join(site.select("dd[@class='video-grade']/a[@class='grade-score']/text()").extract())
            detail_url =self.start_urls[0]+site.select("dt[@class='video-title']/a/@href").extract()[0]
            request = Request(detail_url,callback=self.parse_detail)
            request.meta['item'] = item
            items.append(request)
            #items.append(item)

        link = hxs.select("//div[@id='gpage']/a[@class='page-next']/@href").extract()
        if len(link):
            items.append(Request(link[0],callback=self.parse_item))

        return items

    def parse_detail(self,response):
        genre_list = [
                    u'\u559c\u5267',u'\u7231\u60c5',u'\u52a8\u4f5c',u'\u6050\u6016',u'\u79d1\u5e7b',
                    u'\u5267\u60c5',u'\u72af\u7f6a',u'\u5947\u5e7b',u'\u6218\u4e89',u'\u60ac\u7591',
                    u'\u52a8\u753b',u'\u6587\u827a',u'\u4f26\u7406',u'\u7eaa\u5f55',u'\u4f20\u8bb0',
                    u'\u6b4c\u821e',u'\u53e4\u88c5',u'\u5386\u53f2',u'\u60ca\u609a'
        ]
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        site = hxs.select("//div[@class='v-details-wrap clearfix']/dl[@class='v-details']")
        classify_item = site.select("dd[@class='v-main-info clearfix']/p[@class='gene']/a/i/text()").extract()
        classify_list = list(set(genre_list) & set(classify_item)) 
        if len(classify_list) == 0:
            classify_list = [u'\u5176\u4ed6']

        item['video_url'] = site.select("dd[@class='v-play line-b clearfix']/a/@href").extract() 
        item['video_name'] = site.select("dd[@class='v-title']/span[@id='film_name']/text()").extract() 
        item['video_thumbnail'] = site.select("dd[@class='v-poster']/a[@class='play_btn']/img/@src").extract() 
        item['video_introduction'] = site.select("dd[@class='v-main-info clearfix']/p[@class='intro']/span[1][@class='text']/text()").extract() 
        item['video_view_cnt'] = [] 
        item['sec_classify_name'] = classify_list 
        item['introduction'] = site.select("dd[@class='v-main-info clearfix']/p[@class='intro']/span[1][@class='text']/text()").extract()[0].strip() 
        item['thumbnail'] =  site.select("dd[@class='v-poster']/a[@class='play_btn']/img/@src").extract()[0].strip() 
        item['publish_time'] = site.select("dd[@class='v-main-info clearfix']/p[@class='date']/a/text()").extract()[0] 
        item['director'] = ",".join(site.select("dd[@class='v-main-info clearfix']/p[@class='info']/a/text()").extract())
        actors_list = site.select("dd[@class='v-main-info clearfix']/p[@class='starring']/a/text()").extract() 
        item['actors'] = ",".join(actors_list) 

        for other_list in site.select("dd[@class='v-other-info']/p[@class='item']"):
            if other_list.select("i/text()").extract()[0] == u'\u5730\u533a\uff1a':
                item['area_name'] = other_list.select("text()").extract()[0]

        item['sec_classify'] =  ",".join(classify_list) 
        item['view_cnt'] = 0
        return item 


