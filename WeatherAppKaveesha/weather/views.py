from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import requests
import csv
from weather.models import Location
from weather.models import User
from django.http import *
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from weather.forms import SubscribeForm
from django.contrib import messages

def home(request):

    #Load the location database before the form is rendered so that we have location fields available in the form dropdown.
    with open('util/cityData.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        count=0
        for row in reader:
            #since we only want top 100 locations.
            if count>99:
                break
            _, created = Location.objects.update_or_create(city=(row[0]+","+row[2]))
            count=count+1

    if request.method == 'POST':
        form1 = SubscribeForm(request.POST)
        if form1.is_valid():
            email_id_form = form1.cleaned_data.get('email_id')
            city_form = form1.cleaned_data.get('City')
            location_form=Location.objects.filter(city=city_form)
            
            #If else loop to see if the user exists. Also to handle integrity errors.
            if User.objects.filter(email_id=email_id_form):
                obj=User.objects.filter(email_id=email_id_form)[0]
            else:
                obj=User(email_id=email_id_form)
            obj.location=location_form[0]
            obj.save()
            messages.success(request, 'Subscribed successfully')
            return HttpResponseRedirect('/home')
        
    else:
        form1 = SubscribeForm()
    return render(request, 'weather/home.html', {'form1': form1})
    


