# Scrapy settings for videoscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'videoscrapy'

SPIDER_MODULES = ['videoscrapy.spiders']
NEWSPIDER_MODULE = 'videoscrapy.spiders'

ITEM_PIPELINES = [
    'videoscrapy.pipelines.MoviePipeline',
]

DOWNLOADER_MIDDLEWARES = {
   'videoscrapy.middlewares.WebkitDownloader': 1000,
}
import os
os.environ["DISPLAY"] = ":0"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0'
