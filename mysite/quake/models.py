from django.db import models
from django.utils import timezone
import datetime
# Create your models here

class quakedbs(models.Model):
    date = models.DateTimeField(help_text='Date Published',auto_now_add=False,blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    magnitude = models.FloatField(default=0.0)
    remarks = models.CharField('Remarks ',max_length=200, help_text=('tsunami alert'))
    epicentre = models.CharField('Epicentre ',max_length=200)
    country = models.CharField('Country', max_length=500, null=True)
    # ""mag": 4.1, "place": "4km E of Citluk, Bosnia and Herzegovina", "time": 1497392951780
    #"title": "M 4.1 - 4km E of Citluk, Bosnia and Herzegovina"
    #"coordinates": [17.7499, 43.2245, 4.82]
    #"tsunami": 0
    def __str__(self):
        return self.epicentre
    def __int__(self):
        return self.magnitude + self.date + self.latitude + self.longitude

class Contact(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    emailAddress = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject