
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from videoscrapy.items import VideoItem 


class MySpider(BaseSpider):
    name = 'micromovie'
    allowed_domains = ['tudou.com']
    start_urls = [
        'http://www.tudou.com/cate/ich99a-2b359c365d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c364d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c367d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c381d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c371d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c377d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
        'http://www.tudou.com/cate/ich99a-2b359c370d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so1pe-2pa1.html',
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='content']/div[@class='showcase']/div[@class='row']/div[@class='pack pack_video_card']")
        vcate = hxs.select("//div[@id='secMcol' and @class='m_col']/div[3][@class='category-filter']/div[4][@class='category-item ']/ul/li[@class='current']/a/text()").extract()[0]
        for site in sites:
            vname = site.select("div[@class='txt']/h6[@class='caption']/a/text()").extract()[0]
            vurl = site.select("div[@class='txt']/h6[@class='caption']/a/@href").extract()[0]
            vcount = site.select("div[@class='txt']/ul[@class='info']/li[@class='d_nums']/span[@class='d_play']/text()").extract()[0]
            vpic = site.select("div[@class='pic']/div[@class='inner']/img/@src").extract()[0]
            yield VideoItem(name=vname,video_name=vname,sec_classify=vcate,view_cnt=vcount,thumbnail=vpic,video_url=vurl,area_name='',introduction='',video_introduction='',video_thumbnail=vpic,video_view_cnt=vcount,director='',actors='',publish_time='',score=0)

        for url in hxs.select("//div[@class='page-nav']/div[@class='page-nav-bar']/a[@class='page-nav-next']/@href").extract():
            yield Request('http://www.tudou.com/cate/'+url, callback=self.parse)
