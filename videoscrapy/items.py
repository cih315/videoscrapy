# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import os
from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem

os.environ['DJANGO_SETTINGS_MODULE'] = 'videosite.settings'

try:
    import django
except ImportError:
    django = None

if django:
    from video.models import Movie,MicroMovie
else:
    Movie = None


class VideoscrapyItem(DjangoItem):
    django_model = Movie
    
class MircoMovieItem(DjangoItem):
    django_model = MicroMovie
