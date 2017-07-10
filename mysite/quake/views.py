from django.shortcuts import render
from .models import quakedbs
from quake.forms import FilterResults
import json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from .models import Question, Choice
# Create your views here.
# from django.http import HttpResponse

def index(request):
    quake_list = quakedbs.objects.all()
    context = {'quake_list': quake_list}
    return render(request, 'quake/index.html', context)


def check_table():
    tabledb = quakedbs.objects.all()
    lendb = len(tabledb)
    return lendb


def usgs():
    lendb = check_table()
    print ('rows count:', lendb)
    if lendb > 0:
        return quakedbs.objects.all()
    else:
        file = 'quake/static/significant_month.json'
        with open(file, 'r+') as ff:
            data = json.load(ff)
            for item in data['features']:
                mag = item['properties']['mag']
                place = item['properties']['place']
                timestamp = item['properties']['time']
                realtime = datetime.fromtimestamp(timestamp / 1e3)
                latitude = item['geometry']['coordinates'][0]
                longitude = item['geometry']['coordinates'][1]
                title = item['properties']['title']
                remarks = item['properties']['tsunami']
                mags = quakedbs()
                mags.epicentre = place
                mags.tsunami = remarks
                mags.magnitude = mag
                # mags = quakedb( date = timestamp,
                #                  latitude = latitude,
                #                  longitude = longitude,
                #                  magnitude = mag,
                #                  remarks = remarks,
                #                  epicentre = place,
                #                  )
                mags.save()
        return quakedbs.objects.all()


def earthdata(request):
    listdata = usgs()
    page = request.GET.get('page', 1)
    paginator = Paginator(listdata, 50)
    try:
        listdata = paginator.page(page)
    except PageNotAnInteger:
        listdata = paginator.page(1)
    except EmptyPage:
        listdata = paginator.page(paginator.num_pages)
    return render(request, 'quake/earthdata.html', {'listdata': listdata})

def earthdata(request):
    template_name = 'quake/earthdata.html'
    form = FilterResults()
    questions = quakedbs.objects.order_by('pub_date')
    if request.method == 'POST':
        # form = FilterResults(request.POST)
        status = request.POST['filter_option']
        form = FilterResults(request.POST)
        print("in home ", status)
        if status == "6":
            choices_filtering = quakedbs.objects.all().filter(magnitude__lte=7).order_by('choice_text')
        elif status == "5":
            choices_filtering = quakedbs.objects.all().filter(magnitude__lte=6).order_by('choice_text')
        elif status == "4":
            choices_filtering = quakedbs.objects.all().filter(magnitude__lte=5).order_by('choice_text')
        elif status == "3":
            choices_filtering = quakedbs.objects.all().filter(magnitude__gte=4).order_by('choice_text')
        else:
            status == "2"
            choices_filtering = quakedbs.objects.all().filter(magnitude__lt=3).order_by('choice_text')

        return render(request, template_name,
                      {'title': 'T20 Index Page', 'head': 'T20 Index Head', 'questions': questions,
                       'form': form })
