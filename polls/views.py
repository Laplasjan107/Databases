from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from world_data.models import WorldHappiness
from .forms import CityForm

import pandas as pd


def country_values(form):
    my_data = []
    country = {}
    country['code3'] = "AFG"
    country['name'] = "Afganistan"
    country['value'] = 10
    country['code'] = "AF"
    my_data.append(country)
    country = {}
    country['code3'] = "ZWE"
    country['name'] = "Zimbabwe"
    country['value'] = 100
    country['code'] = "ZW"
    my_data.append(country)
    country = {}
    country['code3'] = "POL"
    country['name'] = "Poland"
    country['value'] = 10000
    country['code'] = "PL"
    my_data.append(country)
    return my_data
    # pass  # tu bedzie obliczanie wyniku dla kazdego miasta


def best_places(form):
    my_data = []
    place = {}
    place['name'] = "London"
    place['lat'] = 51.507222
    place['lon'] = -0.1275
    my_data.append(place)
    place = {}
    place['name'] = "Birmingham"
    place['lat'] = 52.483056
    place['lon'] = -1.893611
    my_data.append(place)
    place = {}
    place['name'] = "Leeds"
    place['lat'] = 53.799722
    place['lon'] = -1.549167
    my_data.append(place)
    place = {}
    place['name'] = "Myślenice"
    place['lat'] = 49.83383
    place['lon'] = 19.9383
    my_data.append(place)
    return my_data


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            languages = form.cleaned_data.get("languages")
            # z jakiegos powodu languages nie wypisuje sie do htmla, ale tutaj w kodzie mamy do niego dostep wiec nie ma problemu
            countries_list = WorldHappiness.objects.all()
            # możemy sobie tak pobrać całą kolumnę
            # print(countries_list)
            map_data = country_values(form)
            cities_data = best_places(form)
            context = {'name': name, 'map_data': map_data, 'cities_data': cities_data}
            return render(request, 'polls/submitted.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'polls/name.html', {'form': form})
