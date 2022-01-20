from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Max, Min

from world_data.models import WorldHappiness
from world_data.models import WorldCities
from world_data.models import AirWaterQuality
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

def res_city_size(city_size_optimal, city, city_data):
    # na razie zrobiłam bez zakresów, ale to można zmienić potem idk
    city_size = city_size['city']
    if city_size is None:
        return 0.5
    max_size = joined_table.aggregate(maxval=Max('City size'))['maxval']
    min_size = joined_table.aggregate(minval=Min('City size'))['minval']
    return abs(city_size - city_size_optimal)/(max_size-min_size)

def res_temperature(temperature_optimal, city, city_data, joined_table):
    city_temp = city_data['city']
    if city_temp is None:
        return 0.5
    max_temp = joined_table.aggregate(maxval=Max('Temperature'))['maxval'] #to chyba jendak nie tak się robi ale jeszcze nie wiem 
    min_temp = joined_table.aggregate(minval=Min('Temperature'))['minval']
    return abs(city_temp - temperature_optimal)/(max_temp-min_temp)

def res_rental_costs(city, city_data, joined_table):
    rentals = city_data['rental costs']
    if rentals is None:
        return 0.5
    max_rentals = joined_table.aggregate(maxval=Max('Rental costs'))['maxval']
    return rentals/max_rentals

def res_living_costs(city, city_data, joined_table):
    living = city_data['living costs']
    if living is None:
        return 0.5
    max_rentals = joined_table.aggregate(maxval=Max('Living costs'))['maxval']
    return living/max_living

def res_gdp(city):
    iso_tab = WorldCities.objects.filter(city = city).values_list('iso3', flat=True)
    iso = iso_tab[0]
    '''print("iso: ")
    print(iso)
    print(WorldHappiness.objects.all())
    print("row: ")
    print(WorldHappiness.objects.filter(country_iso = iso))'''
    gdp_tab = WorldHappiness.objects.filter(country_iso = iso, year = 2019).values_list('log_GDP_per_capita', flat = True)
    if len(gdp_tab) == 0:
        return 0.5
    gdp = gdp_tab[0]
    max_gdp_dict = WorldHappiness.objects.all().aggregate(Max('log_GDP_per_capita'))
    min_gdp_dict = WorldHappiness.objects.all().aggregate(Min('log_GDP_per_capita'))
    max_gdp = max_gdp_dict.get('log_GDP_per_capita__max')
    min_gdp = min_gdp_dict.get('log_GDP_per_capita__min')
    print("min gdp = " + str(min_gdp))
    print("max gdp = " + str(max_gdp))
    print("this gdp = ")
    print(gdp)
    return (gdp - min_gdp)/(max_gdp-min_gdp)

def res_air_pollution(city):
    air_tab = AirWaterQuality.objects.filter(city = city).values_list('air_quality', flat = True)
    if len(air_tab) == 0:
        return 0.5
    air = air_tab[0]
    max_air_dict = AirWaterQuality.objects.all().aggregate(Max('air_quality'))
    min_air_dict = AirWaterQuality.objects.all().aggregate(Min('air_quality'))
    max_air = max_air_dict.get('air_quality__max')
    min_air = min_air_dict.get('air_quality__min')
    '''print("min air = " + str(min_air))
    print("max air = " + str(max_air))
    print("this air = ")
    print(air)'''
    return (max_air - air)/(max_air - min_air)

def res_freedom(city):
    iso_tab = WorldCities.objects.filter(city = city).values_list('iso3', flat=True)
    iso = iso_tab[0]
    '''print("iso: ")
    print(iso)
    print(WorldHappiness.objects.all())
    print("row: ")
    print(WorldHappiness.objects.filter(country_iso = iso))'''
    freedom_tab = WorldHappiness.objects.filter(country_iso = iso, year = 2019).values_list('freedom_of_life_choices', flat = True)
    if len(freedom_tab) == 0:
        return 0.5
    freedom = freedom_tab[0]
    max_freedom_dict =  WorldHappiness.objects.all().aggregate(Max('freedom_of_life_choices'))
    min_freedom_dict = WorldHappiness.objects.all().aggregate(Min('freedom_of_life_choices'))
    max_freedom = max_freedom_dict.get('freedom_of_life_choices__max')
    min_freedom = min_freedom_dict.get('freedom_of_life_choices__min')
    print("min gdp = " + str(min_freedom))
    print("max gdp = " + str(max_freedom))
    print("this gdp = ")
    print(freedom)
    return (freedom - min_freedom)/(max_freedom-min_freedom)
    
    


def compute_result(form, city):
    # city_size_optimal, city_size_importance, temperature_optimal, temperature_importance, rental_costs_importance, living_costs_importance, pollution_importance, gdp_per_capita_importance, continents, continent_importance, air_pollution, freedom_importance, internet_price_importance 
    results = {}
    '''results['city_size'] = res_city_size(form.cleaned_data['city_size_optimal'], city, joined_table) * form.cleaned_data['city_size_importance'] / 10
    results['temperature'] = res_temperature(form.cleaned_data['temperature_optimal'], city, joined_table) * form.cleaned_data['temperature_importance'] / 10
    results['rental_costs'] = res_rental_costs(city, city_data) * form.cleaned_data['rental_costs_importance'] / 10
    results['living_costs'] = res_living_costs(city, city_data) * form.cleaned_data['living_costs_importance'] / 10
    results['pollution'] = res_pollution(city, city_data) * form.cleaned_data['pollution_importance'] / 10'''
    results['gdp_per_capita'] = res_gdp(city) * form.cleaned_data['gdp_per_capita_importance'] / 10
    # results['continent'] = res_continent(form.cleaned_data['continents'], city, joined_table) * form.cleaned_data['continent_importance'] / 10
    results['air_pollution'] = res_air_pollution(city) * form.cleaned_data['air_pollution_importance'] / 10
    results['freedom'] = res_freedom(city) * form.cleaned_data['freedom_importance'] / 10
    #results['internet_price'] = res_internet_price(city) * form.cleaned_data['internet_price_importance'] / 10
    # resztę funkcji się najwyżej potem dopisze
    result = 0
    print("results:")
    print(results)
    for res in results:
        result = result + results[res]
    return result
 

def best_places(form):
    city_results = {}
    city_list = WorldCities.objects.values_list('city', flat=True)
    # licz = 0  #służy do debugowania żeby było 100 iteracji a nie 40000 bo to długo trwa
    for city in city_list:
        '''licz = licz + 1
        if licz > 100:
            break'''
        city_results[city] = compute_result(form, city)
    sorted_cities = {k: v for k, v in sorted(city_results.items(), key=lambda item: item[1])}
    print("sorted cities:")
    print(sorted_cities)
    best_cities = list(sorted_cities.keys())[0:10]
    print(best_cities)
    my_data = []
    for city in best_cities:
        place = {}
        place['name'] = city
        lat_tab = WorldCities.objects.filter(city = city).values_list('latitude', flat=True)
        lat = lat_tab[0]
        place['lat'] = lat
        lon_tab = WorldCities.objects.filter(city = city).values_list('longitude', flat=True)
        lon = lon_tab[0]
        place['lon'] = lon
        my_data.append(place)
    '''
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
    # mozna kolorowac miejsca od najlepszego
    place['color'] = '#ff000f'
    my_data.append(place)'''
    return my_data


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # z jakiegos powodu languages nie wypisuje sie do htmla, ale tutaj w kodzie mamy do niego dostep wiec nie ma problemu
            countries_list = WorldHappiness.objects.all()
            # możemy sobie tak pobrać całą kolumnę
            title = "Best places for you, " + name
            map_data = country_values(form)
            cities_data = best_places(form)
            context = {'name': name, 'title': title, 'map_data': map_data, 'cities_data': cities_data}
            return render(request, 'polls/submitted.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, 'polls/name.html', {'form': form})
