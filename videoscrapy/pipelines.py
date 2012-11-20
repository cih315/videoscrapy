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
        self.sec_classify_list = SecondClassify.objects.all()    
        self.top_classify_list = TopClassify.objects.all()    
        self.area_list = AreaDic.objects.all()    
        self.sort_index = 0    

    def process_item(self, item, spider):
        self.sort_index = self.sort_index + 1
        sec_classify,seccreated = self.sec_classify_list.get_or_create(name=item['sec_classify'])
        area = self.area_list.get(pk=1) 
        if item['area_name']:
            area = self.area_list.get(area_name=item['area_name'])
        top_classify = self.top_classify_list.get(spider_name=spider.name)        

        series, created = SeriesInfo.objects.get_or_create(name=item['name'],area=area,top_classify=top_classify)
	series.sec_classify=item['sec_classify']
        series.introduction=item['introduction']
	series.director=item['director']
	series.actors=item['actors']
	series.publish_time=item['publish_time']
	series.thumbnail=item['thumbnail']
	series.score=item['score']
	series.view_cnt=item['view_cnt']
	#series.sort_index=self.sort_index 
        series.save()

        series.videoinfo_set.get_or_create(
	    url=item['video_url'],
            defaults={'thumbnail':item['video_thumbnail'],
                'view_cnt':item['video_view_cnt'],
		'introduction':item['video_introduction'],
		'website':spider.allowed_domains[0],
		'name':item['video_name']})        

        VideoType.objects.get_or_create(series=series,sec_classify=sec_classify)
       
        return item 
