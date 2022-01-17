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
