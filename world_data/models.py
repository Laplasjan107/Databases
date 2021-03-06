from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save
)


# https://www.kaggle.com/timoboz/country-data?select=continent.json
class Iso(models.Model):
    country = models.CharField(max_length=200, default=None, primary_key=True)
    iso2 = models.CharField(max_length=2, default=None, blank=True, null=True)
    iso3 = models.CharField(max_length=3, default=None, blank=True, null=True, unique=True)
    numeric = models.IntegerField(default=None, blank=True, null=True)
    iso2_continent = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.country


# https://www.kaggle.com/juanmah/world-cities
# Attribution 4.0 International (CC BY 4.0)
class WorldCities(models.Model):
    city = models.CharField(max_length=200)
    iso3 = models.CharField(max_length=5, default=None, blank=True, null=False)
    iso3_link = models.ForeignKey(Iso, null=False, on_delete=models.CASCADE)
    city_ascii = models.CharField(max_length=200, default=None, blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)
    admin_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    capital = models.CharField(max_length=200, default=None, blank=True, null=True)
    population = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.city + ", " + self.iso3


class WorldHappiness(models.Model):
    country_iso = models.CharField(max_length=3, blank=False, null=False)
    iso3_link = models.ForeignKey(Iso, null=True, on_delete=models.CASCADE)
    year = models.IntegerField(default=None, blank=True, null=True)
    life_ladder = models.FloatField(default=None, blank=True, null=True)
    log_GDP_per_capita = models.FloatField(default=None, blank=True, null=True)
    social_support = models.FloatField(default=None, blank=True, null=True)
    healthy_life_expectancy = models.FloatField(default=None, blank=True, null=True)
    freedom_of_life_choices = models.FloatField(default=None, blank=True, null=True)
    generosity = models.FloatField(default=None, blank=True, null=True)
    perceptions_of_corruption = models.FloatField(default=None, blank=True, null=True)
    positive_affect = models.FloatField(default=None, blank=True, null=True)
    negative_affect = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.country_iso


# https://www.kaggle.com/cityapiio/world-cities-average-internet-prices-2020
# CC0: Public Domain
class InternetPrices(models.Model):
    city = models.CharField(max_length=200)
    # TODO: zmiana country na iso3?
    country = models.CharField(max_length=200)
    price_usd = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.city


# https://ourworldindata.org/grapher/main-religion-of-the-country-in
# Creative Commons BY license.
class CountryReligion(models.Model):
    iso3 = models.CharField(max_length=3, null=False, blank=False)
    year = models.IntegerField(default=None, blank=True, null=True)
    main_religion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.iso3


# https://www.kaggle.com/cityapiio/world-cities-air-quality-and-water-polution
# CC0: Public Domain
class AirWaterQuality(models.Model):
    city = models.CharField(max_length=200, null=False, blank=False)
    # TODO: zmiana country na iso3?
    country = models.CharField(max_length=200, null=False, blank=False)
    air_quality = models.FloatField(null=True, blank=True)
    water_quality = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.city + ", " + self.country


# Trigger for iso table
@receiver(pre_save, sender=AirWaterQuality)
def check_has_any_quality(sender, instance, *args, **kwargs):
    if not instance.air_quality and not instance.water_quality:
        raise Exception("Neither water, nor air quality specified")



@receiver(pre_save, sender=Iso)
def check_has_any_iso(sender, instance, *args, **kwargs):
    if not instance.iso3 and not instance.iso2:
        raise Exception("No iso uploaded")

    continent_codes = ["EU", "AS", "SA", "NA", "AF", "AS", "OC"]
    if instance.iso2_continent and instance.iso2_continent not in continent_codes:
        raise Exception("Invalid continent iso")

