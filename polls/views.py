from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from world_data.models import WorldHappiness
from .forms import CityForm

import pandas as pd


def compute_result(form):
    df_format = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population'
                             '-density.json')
    print(df_format)
    my_data = []
    country = {}
    country['code3'] = "AFG"
    country['name'] = "Afganistan"
    country['value'] = 10
    country['code'] = "AF"
    my_data.append(country)
    print(country)
    country = {}
    country['code3'] = "ZWE"
    country['name'] = "Zimbabwe"
    country['value'] = 100
    country['code'] = "ZW"
    print(country)
    my_data.append(country)
    print(my_data)
    return my_data
    # pass  # tu bedzie obliczanie wyniku dla kazdego miasta


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
            map_data = compute_result(form)
            print("map data ")
            print(map_data)
            print('siup')
            context = {'name': name, 'map_data': map_data}
            return render(request, 'polls/submitted.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'polls/name.html', {'form': form})
