from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule

from videoscrapy.items import VideoscrapyItem

class VideoSpider(CrawlSpider):
   name = "video"
   allowed_domains = ["youku.com"]
   start_urls = [
      "http://movie.youku.com/"
   ]

   rules = (
         Rule(SgmlLinkExtractor(restrict_xpaths="//div[@class='showCatalog_S']/div[@class='catalogs']/div[@class='catalog showpaid']/ul/li[1]/a"),
         callback='parse_directory', follow=True),
   )

   def parse_directory(self, response):
       hxs = HtmlXPathSelector(response)
       self.log('hi,this item page %s'%response.url)
       sites = hxs.select("//div[@class='collgrid6t']/div[@class='items']/ul[@class='p pv']")
       items = []
       for site in sites:
           item = VideoscrapyItem()
           item['name'] = site.select("li[@class='p_link']/a/@title").extract()[0]
           item['url'] = site.select("li[@class='p_link']/a/@href").extract()[0]
           item['description'] = site.select("div[@class='info']/p[@class='discrib']/a/text()").extract()
           item['pic'] = site.select("li[@class='p_thumb']/img/@src").extract()[0]
           items.append(item)

       for link in hxs.select("//div[@class='LPageBar']/div[@class='page_index']/span[@class='next']/a"):
           if len(link.select('text()').extract()):
               if link.select('text()').extract()[0] == u'\u4e0b\u9875':
                   url = link.select('@href').extract()[0]
                   items.append(Request(url, callback=self.parse_directory))

       return items
