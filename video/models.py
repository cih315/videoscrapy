from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=200)
    pic = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    def __unicode__(self):
        return self.name

class MicroMovie(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    pic = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    cate = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class AreaDic(models.Model):
    areaName = models.CharField(max_length=32,db_column='area_name')
    class Meta:
        db_table = 'area_dic'
    
class SeriesInfo(models.Model):
    area_id = models.IntegerField() 
    sec_classify = models.CharField(max_length=32) 
    top_classify_id = models.IntegerField() 
    name = models.CharField(max_length=32)
    introduction = models.CharField(max_length=1024)
    director = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    publish_time = models.CharField(max_length=32)
    thumbnail = models.CharField(max_length=128)
    score = models.IntegerField(default=0) 
    view_cnt = models.IntegerField(default=0) 
    sort_index = models.IntegerField(default=0) 
    
    class Meta:
        db_table = 'series_info'
