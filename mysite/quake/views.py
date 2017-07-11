from django.shortcuts import render
from .models import quakedbs, Contact
from quake.forms import FilterResults, ContactForm
from django.core.mail import BadHeaderError
import urllib.request, urllib.parse, urllib.error
import json
import re
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template


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
    fhand = urllib.request.urlopen('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson').read()
    fhand = fhand.decode('UTF-8')
    lendb = check_table()
    print ('rows count:', lendb)
    if lendb > 0:
        return quakedbs.objects.all()
    else:
        data = json.loads(fhand)
        for item in data['features']:
            mag = item['properties']['mag']
            place = item['properties']['place']
            timestamp = item['properties']['time']
            realtime = datetime.fromtimestamp(timestamp / 1e3)
            latitude = item['geometry']['coordinates'][1]
            longitude = item['geometry']['coordinates'][0]
            title = item['properties']['title']
            remarks = item['properties']['tsunami']
            country = re.findall(', (\D+)', place)
            mags = quakedbs()
            mags.epicentre = place
            mags.tsunami = remarks
            mags.magnitude = mag
            mags.date = realtime
            mags.latitude = latitude
            mags.longitude = longitude
            for state in country:
                mags.country = state
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
    form = FilterResults()
    questions = quakedbs.objects.order_by('magnitude')
    #print(questions)
    if request.method == 'POST':
        # form = FilterResults(request.POST)
        status = request.POST.get('status')
        #form = FilterResults(request.POST)
        print("in home ", status)
        if status == "6":
            choices_filtering = quakedbs.objects.all().filter(magnitude__gte=7).order_by('magnitude')
        elif status == "5":
            choices_filtering = quakedbs.objects.all().filter(magnitude__gt=6).order_by('magnitude')
        elif status == "4":
            choices_filtering = quakedbs.objects.all().filter(magnitude__gte=5).order_by('magnitude')
        elif status == "3":
            choices_filtering = quakedbs.objects.all().filter(magnitude__gte=4).order_by('magnitude')
        elif status == "2":
            choices_filtering = quakedbs.objects.all().filter(magnitude__lte=4).order_by('magnitude')
        elif status == "1":
            choices_filtering = quakedbs.objects.all().filter(magnitude__lte=3).order_by('magnitude')
        else:
            status == "0"
            choices_filtering = quakedbs.objects.all().filter(magnitude__lt=7).order_by('magnitude')
        return render(request, 'quake/earthdata.html',
                      {'listdata': choices_filtering, 'questions': questions, 'form': form})
    else:
        form = FilterResults()
        return render(request, 'quake/earthdata.html', {'listdata': listdata, 'questions': questions, 'form': form})


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            emailAddress = form.cleaned_data['emailAddress']
            message = form.cleaned_data['message']
            try:
                obj = Contact(subject=subject, emailAddress=emailAddress, message=message)
                obj.save()
                # send_mail(subject, message, contactemail, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
    return render(request, "quake/contact.html", {'form': form})

