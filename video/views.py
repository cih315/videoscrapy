# Create your views here.
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from video.models import SeriesInfo, SecondClassify,VideoType

def home(request):
    series_list = SeriesInfo.objects.all()
    paginator = Paginator(series_list,12)
    page = request.GET.get("page")

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render_to_response('video/index.html',{'list':videos})
                                                              
def cate(request,cate):
    secondClassify = SecondClassify.objects.get(pk=cate)
    print(secondClassify.name)
  
    #sec_list = secondClassify.videotype_set.all() 
    #sec_count = secondClassify.videotype_set.count() 
    videotype = VideoType.objects.filter(sec_classify=secondClassify)
    print(len(videotype))
    series_ids = []
    for video in videotype: 
        series_ids.append(video.series_id)
    print(series_ids)
    series_list = SeriesInfo.objects.filter(id__in =series_ids)
    print(series_list.count())
    #series_list.videotype_set.all()
    #series_list.videotype_set.all()
    #sec_list.videotype_set.all()
    #for sec in sec_list:
        #print(sec.seriesinfo_set)
    #VideoType.object.get()
    #series_list.videotype_set.filter(sec_classify=)
    paginator = Paginator(series_list,12)
    page = request.GET.get("page")

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)


    return render_to_response('video/index.html',{'list':videos})
