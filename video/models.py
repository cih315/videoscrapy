from django.db import models

# Create your models here.

class AreaDic(models.Model):
    area_name = models.CharField(max_length=32)

    class Meta:
        db_table = 'area_dic'
    
class TopClassify(models.Model):  
    name = models.CharField(max_length=64)
    spider_name = models.CharField(max_length=64)
    area_serarch = models.IntegerField(default=0)
    time_serarch = models.IntegerField(default=0)
    sec_claaify_serarch = models.IntegerField(default=0)

    class Meta:
        db_table = 'top_classify'

class SecondClassify(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'second_classify'

class Classify(models.Model):
    top_classify = models.ForeignKey(TopClassify)
    sec_classify = models.ForeignKey(SecondClassify)

    class Meta:
        db_table = 'classify'

class SeriesInfo(models.Model):
    area = models.ForeignKey(AreaDic)
    top_classify = models.ForeignKey(TopClassify)
    sec_classify = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    introduction = models.CharField(max_length=2048,null=True)
    director = models.CharField(max_length=255,null=True)
    actors = models.CharField(max_length=255,null=True)
    publish_time = models.CharField(max_length=32,null=True)
    thumbnail = models.CharField(max_length=128)
    score = models.CharField(max_length=32,null=True) 
    view_cnt = models.CharField(max_length=32,null=True) 
    sort_index = models.IntegerField(default=0)

    def __unicode__(self):
        return seft.sec_classify   

    class Meta:
        db_table = 'series_info'
        ordering = ['sort_index']

class VideoInfo(models.Model):
    series = models.ForeignKey(SeriesInfo)
    name = models.CharField(max_length=64)
    introduction = models.CharField(max_length=2048,null=True)
    thumbnail = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    website = models.CharField(max_length=64)
    view_cnt = models.IntegerField(default=0)
    sort_index = models.IntegerField(default=0)

    class Meta:
        db_table = 'video_info'
        ordering = ['sort_index']

class VideoType(models.Model):
    series = models.ForeignKey(SeriesInfo)
    sec_classify = models.ForeignKey(SecondClassify)

    class Meta:
        db_table = 'video_type'
