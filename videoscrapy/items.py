# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import os
from scrapy.contrib.djangoitem import DjangoItem, Field

os.environ['DJANGO_SETTINGS_MODULE'] = 'videosite.settings'

try:
    import django
except ImportError:
    django = None

if django:
    from video.models import SeriesInfo 
else:
    Movie = None


class BaseVideoItem(DjangoItem):
    django_model = SeriesInfo 
    
class VideoItem(BaseVideoItem):
    area_name = Field() 
    top_classify_name = Field() 
    sec_classify_name = Field() 
    video_name = Field() 
    video_introduction = Field() 
    video_thumbnail = Field() 
    video_url = Field() 
    video_website = Field() 
    video_view_cnt = Field() 

    
    
