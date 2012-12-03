# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
# -*- coding: utf-8 -*- 
from video.models import *
from scrapy.exceptions import DropItem

class VideoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MoviePipeline(object):

    def __init__(self):
        self.sec_classify_list = SecondClassify.objects.all()    
        self.top_classify_list = TopClassify.objects.all()    
        self.area_list = AreaDic.objects.all()    

    def process_item(self, item, spider):
        if len(item['video_url']) == 0:
            raise DropItem("Missing the deatil video %s" % item)

        if len(item['sec_classify_name']) == 0:
            raise DropItem("Missing the deatil video %s" % item)
          

        area,areaCreated = self.area_list.get_or_create(area_name=item['area_name'])
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

        for i in range(len(item['video_url'])):
            #i = i - 1
            series.videoinfo_set.get_or_create(url=item['video_url'][i],
            defaults={'thumbnail':item['video_thumbnail'][i],
			  'view_cnt':item['video_view_cnt'][i],'introduction':item['video_introduction'][i],
			  'website':spider.allowed_domains[0],'name':item['video_name'][i],
                          'sort_index':item['video_sort_index'][i]})        

        for i,v in enumerate(item['sec_classify_name']): 
            sec_classify_id,seccreated = self.sec_classify_list.get_or_create(name=v)
            VideoType.objects.get_or_create(series=series,sec_classify=sec_classify_id)
       
        return item 
