# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from video.models import Movie,MicroMovie 

class VideoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MoviePipeline(object):

    def __init__(self):
        MicroMovie.objects.all().delete()
   
    def process_item(self, item, spider):
        if spider.name == 'micromovie':
            #movie = Movie(name=name,url=item['url'], pic =item['pic'],description=item['description'])
            micromovie = MicroMovie(name=item['name'],url=item['url'], pic =item['pic'],count=item['count'],desc='',cate=item['cate'])
            micromovie.save()

        return item 
