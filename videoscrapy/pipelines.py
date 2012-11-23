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

    def process_item(self, item, spider):

        area = self.area_list.get(pk=1) 
        try:
            if item['area_name']:
                area = self.area_list.get(area_name=item['area_name'])
        except AreaDic.DoesNotExist:
            area = self.area_list.get(pk=10)

        top_classify = self.top_classify_list.get(spider_name=spider.name)        

        series, created = SeriesInfo.objects.get_or_create(name=item['name'],area=area,top_classify=top_classify)
	series.sec_classify = item['sec_classify'] 
        series.introduction =item['introduction']
	series.director=item['director']
	series.actors=item['actors']
	series.publish_time=item['publish_time']
	series.thumbnail=item['thumbnail']
	series.score=item['score']
	series.view_cnt=item['view_cnt']
	series.sort_index=item['sort_index'] 
        series.save()

        for i,v in enumerate(item['video_url']):
            cnt = 0
            if len(item['video_view_cnt']) > 0:
                cnt = item['video_view_cnt'][i]
            series.videoinfo_set.get_or_create(url=item['video_url'][i-1],
		defaults={'thumbnail':item['video_thumbnail'][i-1],
			  'view_cnt':cnt,'introduction':item['video_introduction'][i-1],
			  'website':spider.allowed_domains[0],'name':item['video_name'][i-1]})        

        for i,v in enumerate(item['sec_classify_name']): 
            sec_classify_id,seccreated = self.sec_classify_list.get_or_create(name=item['sec_classify_name'][i])
            VideoType.objects.get_or_create(series=series,sec_classify=sec_classify_id)
       
        return item 
