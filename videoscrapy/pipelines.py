# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
# -*- coding: utf-8 -*- 
from video.models import *

class VideoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MoviePipeline(object):

    def __init__(self):
	#print('this is init==========>')
        #MicroMovie.objects.all().delete()
        self.sec_classify_list = SecondClassify.objects.all()    
        self.top_classify_list = TopClassify.objects.all()    
        self.area_list = AreaDic.objects.all()    
        self.sort_index = 0    

    def process_item(self, item, spider):
        #if spider.name == 'micromovie':
            #movie = Movie(name=name,url=item['url'], pic =item['pic'],description=item['description'])
            #micromovie = MicroMovie(name=item['name'],url=item['url'], pic =item['pic'],count=item['count'],desc='',cate=item['cate'])
            #micromovie.save()
        #print(item['sec_classify'].encode('utf-8'))
        #if item['sec_classify'].encode('utf-8') in self.sec_classify_list:
        #    print(item['sec_classify'].encode('utf-8'))
        #print(self.sec_classify_list.count())
        self.sort_index = self.sort_index + 1;
        sec_classify = self.sec_classify_list.get(name=item['sec_classify'])
        area = self.area_list.get(pk=1) 
        if item['area_name']:
            area = self.area_list.get(area_name=item['area_name'])
        top_classify = self.top_classify_list.get(spider_name=spider.name)        
        series = SeriesInfo(area=area,top_classify=top_classify,sec_classify=item['sec_classify'],name=item['name'],introduction=item['introduction'],director=item['director'],actors=item['actors'],publish_time=item['publish_time'],thumbnail=item['thumbnail'],score=item['score'],view_cnt=item['view_cnt'],sort_index=self.sort_index)
        series.save()
        series.videoinfo_set.create(name=item['video_name'],introduction=item['video_introduction'],thumbnail=item['video_thumbnail'],url=item['video_url'],website=spider.allowed_domains[0],view_cnt=item['video_view_cnt'])        
        videotype = VideoType(series=series,sec_classify=sec_classify)
        videotype.save()
       
        return item 
