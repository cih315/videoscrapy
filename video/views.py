# Create your views here.
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from video.models import SeriesInfo, SecondClassify,VideoType,Classify,SecondClassify

def home(request):
    series_list = SeriesInfo.objects.all()
    paginator = Paginator(series_list,12)
    page = request.GET.get("page")
    cate_list = SecondClassify.objects.filter(classify__top_classify=1) 
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render_to_response('video/index.html',{'list':videos,'cate_list':cate_list,'currcate':'all'})
                                                              
def cate(request,cate):
    series_list = SeriesInfo.objects.filter(videotype__sec_classify=cate)
    paginator = Paginator(series_list,12)
    page = request.GET.get("page")
    cate_list = SecondClassify.objects.filter(classify__top_classify=1) 

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render_to_response('video/index.html',{'list':videos,'cate_list':cate_list,'currcate':cate})

def getshow(request):
    series_list = SeriesInfo.objects.all()
    paginator = Paginator(series_list,12)
    page = request.GET.get("page")
    cate_list = SecondClassify.objects.filter(classify__top_classify=5)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render_to_response('video/shows.html',{'list':videos,'cate_list':cate_list,'currcate':'all'})


def getShowByCate(request,cate):
    series_list = SeriesInfo.objects.filter(videotype__sec_classify=cate)
    paginator = Paginator(series_list,12)
    print(serires_list.count)
    page = request.GET.get("page")
    cate_list = SecondClassify.objects.filter(classify__top_classify=5)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render_to_response('video/shows.html',{'list':videos,'cate_list':cate_list,'currcate':cate})

