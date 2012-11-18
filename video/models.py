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

