from django.db import models


# Create your models here.

#
class WorldHappiness(models.Model):
    country_name = models.CharField(max_length=200)
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
        return self.country_name


# https://www.kaggle.com/juanmah/world-cities
# Attribution 4.0 International (CC BY 4.0)
class WorldCities(models.Model):
    city = models.CharField(max_length=200)
    city_ascii = models.CharField(max_length=200, default=None, blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)
    country = models.CharField(max_length=200, default=None, blank=True, null=True)
    iso2 = models.CharField(max_length=5, default=None, blank=True, null=True)
    iso3 = models.CharField(max_length=5, default=None, blank=True, null=True)
    admin_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    capital = models.CharField(max_length=200, default=None, blank=True, null=True)
    population = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.city


class InternetPrices(models.Model):
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    price_usd = models.FloatField(default=None, blank=True, null=True)
