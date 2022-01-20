from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Max, Min

from world_data.models import WorldHappiness
from world_data.models import WorldCities
from world_data.models import AirWaterQuality
from world_data.models import InternetPrices
from world_data.models import Iso
from .forms import CityForm

import pandas as pd


def res_freedom_country(country):
    iso_tab = Iso.objects.filter(country=country).values_list('iso3', flat=True)
    iso = iso_tab[0]
    freedom_tab = WorldHappiness.objects.filter(country_iso=iso, year=2019).values_list('freedom_of_life_choices',
                                                                                        flat=True)
    if len(freedom_tab) == 0:
        return 0.5
    freedom = freedom_tab[0]
    if freedom is None:
        return 0.5
    max_freedom_dict = WorldHappiness.objects.all().aggregate(Max('freedom_of_life_choices'))
    min_freedom_dict = WorldHappiness.objects.all().aggregate(Min('freedom_of_life_choices'))
    max_freedom = max_freedom_dict.get('freedom_of_life_choices__max')
    min_freedom = min_freedom_dict.get('freedom_of_life_choices__min')

    return (freedom - min_freedom) / (max_freedom - min_freedom)


def res_gdp_country(country):
    iso_tab = Iso.objects.filter(country=country).values_list('iso3', flat=True)
    iso = iso_tab[0]
    gdp_tab = WorldHappiness.objects.filter(country_iso=iso, year=2019).values_list('log_GDP_per_capita', flat=True)
    if len(gdp_tab) == 0:
        return 0.5
    gdp = gdp_tab[0]
    if gdp == None:
        return 0.5
    max_gdp_dict = WorldHappiness.objects.all().aggregate(Max('log_GDP_per_capita'))
    min_gdp_dict = WorldHappiness.objects.all().aggregate(Min('log_GDP_per_capita'))
    max_gdp = max_gdp_dict.get('log_GDP_per_capita__max')
    min_gdp = min_gdp_dict.get('log_GDP_per_capita__min')
    return (gdp - min_gdp) / (max_gdp - min_gdp)


def compute_result_country(form, country):
    results = {}
    results['gdp_per_capita'] = res_gdp_country(country) * form.cleaned_data['gdp_per_capita_importance'] / 10
    results['freedom'] = res_freedom_country(country) * form.cleaned_data['freedom_importance'] / 10
    result = 0
    for res in results:
        result = result + results[res]
    return result


def country_values(form):
    country_results = {}
    country_list = Iso.objects.values_list('country', flat=True)
    # licz = 0  #służy do debugowania żeby było 100 iteracji a nie 40000 bo to długo trwa
    for country in country_list:
        country_results[country] = compute_result_country(form, country)
    sorted_countries = {k: v for k, v in sorted(country_results.items(), key=lambda item: item[1])}
    best_countries = list(sorted_countries.keys())[
                     (len(sorted_countries.keys()) - 50): (len(sorted_countries.keys()) - 1)]
    print(best_countries)
    my_data = []
    for country in best_countries:
        place = {}
        place['name'] = country
        place['value'] = country_results[country] * 1000
        place['code3'] = Iso.objects.filter(country=country).values_list('iso3', flat=True)[0]
        my_data.append(place)
    return my_data


def res_temperature(temperature_optimal, city, city_data, joined_table):
    city_temp = city_data['city']
    if city_temp is None:
        return 0.5
    max_temp = joined_table.aggregate(maxval=Max('Temperature'))[
        'maxval']  # to chyba jendak nie tak się robi ale jeszcze nie wiem
    min_temp = joined_table.aggregate(minval=Min('Temperature'))['minval']
    return abs(city_temp - temperature_optimal) / (max_temp - min_temp)


def res_rental_costs(city, city_data, joined_table):
    rentals = city_data['rental costs']
    if rentals is None:
        return 0.5
    max_rentals = joined_table.aggregate(maxval=Max('Rental costs'))['maxval']
    return rentals / max_rentals


def res_living_costs(city, city_data, joined_table):
    living = city_data['living costs']
    if living is None:
        return 0.5
    max_rentals = joined_table.aggregate(maxval=Max('Living costs'))['maxval']
    return living / max_rentals


def res_gdp(city):
    iso_tab = WorldCities.objects.filter(city=city).values_list('iso3', flat=True)
    iso = iso_tab[0]
    gdp_tab = WorldHappiness.objects.filter(country_iso=iso, year=2019).values_list('log_GDP_per_capita', flat=True)
    if len(gdp_tab) == 0:
        return 0.5
    gdp = gdp_tab[0]
    if gdp is None:
        return 0.5
    max_gdp_dict = WorldHappiness.objects.all().aggregate(Max('log_GDP_per_capita'))
    min_gdp_dict = WorldHappiness.objects.all().aggregate(Min('log_GDP_per_capita'))
    max_gdp = max_gdp_dict.get('log_GDP_per_capita__max')
    min_gdp = min_gdp_dict.get('log_GDP_per_capita__min')

    return (gdp - min_gdp) / (max_gdp - min_gdp)


def res_air_pollution(city):
    air_tab = AirWaterQuality.objects.filter(city=city).values_list('air_quality', flat=True)
    if len(air_tab) == 0:
        return 0.5
    air = air_tab[0]
    if air is None:
        return 0.5
    max_air_dict = AirWaterQuality.objects.all().aggregate(Max('air_quality'))
    min_air_dict = AirWaterQuality.objects.all().aggregate(Min('air_quality'))
    max_air = max_air_dict.get('air_quality__max')
    min_air = min_air_dict.get('air_quality__min')
    return (max_air - air) / (max_air - min_air)


def res_freedom(city):
    iso_tab = WorldCities.objects.filter(city=city).values_list('iso3', flat=True)
    iso = iso_tab[0]
    freedom_tab = WorldHappiness.objects.filter(country_iso=iso, year=2019).values_list('freedom_of_life_choices',
                                                                                        flat=True)
    if len(freedom_tab) == 0:
        return 0.5
    freedom = freedom_tab[0]
    if not freedom:
        return 0.5
    max_freedom_dict = WorldHappiness.objects.all().aggregate(Max('freedom_of_life_choices'))
    min_freedom_dict = WorldHappiness.objects.all().aggregate(Min('freedom_of_life_choices'))
    max_freedom = max_freedom_dict.get('freedom_of_life_choices__max')
    min_freedom = min_freedom_dict.get('freedom_of_life_choices__min')

    return (freedom - min_freedom) / (max_freedom - min_freedom)


def res_internet_price(city):
    price_tab = InternetPrices.objects.filter(city=city).values_list('price_usd', flat=True)
    if len(price_tab) == 0:
        return 0.5
    price = price_tab[0]
    max_price_dict = InternetPrices.objects.all().aggregate(Max('price_usd'))
    min_price_dict = InternetPrices.objects.all().aggregate(Min('price_usd'))
    max_price = max_price_dict.get('price_usd__max')
    min_price = min_price_dict.get('price_usd__min')

    return (max_price - price) / (max_price - min_price)


def compute_result(form, city):
    # city_size_optimal, city_size_importance, temperature_optimal, temperature_importance, rental_costs_importance, living_costs_importance, pollution_importance, gdp_per_capita_importance, continents, continent_importance, air_pollution, freedom_importance, internet_price_importance
    results = {}
    results['gdp_per_capita'] = res_gdp(city) * form.cleaned_data['gdp_per_capita_importance'] / 10
    # results['continent'] = res_continent(form.cleaned_data['continents'], city, joined_table) * form.cleaned_data['continent_importance'] / 10
    results['air_pollution'] = res_air_pollution(city) * form.cleaned_data['air_pollution_importance'] / 10
    results['freedom'] = res_freedom(city) * form.cleaned_data['freedom_importance'] / 10
    results['internet_price'] = res_internet_price(city) * form.cleaned_data['internet_price_importance'] / 10
    # resztę funkcji się najwyżej potem dopisze
    result = 0
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

    best_cities = list(sorted_cities.keys())[(len(sorted_cities.keys()) - 30): (len(sorted_cities.keys()) - 1)]

    my_data = []
    for city in best_cities:
        place = {}
        place['name'] = city
        lat_tab = WorldCities.objects.filter(city=city).values_list('latitude', flat=True)
        lat = lat_tab[0]
        place['lat'] = lat
        lon_tab = WorldCities.objects.filter(city=city).values_list('longitude', flat=True)
        lon = lon_tab[0]
        place['lon'] = lon
        my_data.append(place)

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
