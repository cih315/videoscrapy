from video.models import MicroMovie,AreaDic
from django.contrib import admin

class AreaDicAdmin(admin.ModelAdmin):
    search_fields = ['areaName']    

    list_display = ('id','areaName')

    list_per_page = 10
 
admin.site.register(MicroMovie)
admin.site.register(AreaDic,AreaDicAdmin)
