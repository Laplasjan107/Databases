from django import forms

class CityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    city_size_optimal = forms.IntegerField(label='Optimal number of inhabitants in your dream city?')
    city_size_importance = forms.IntegerField(label='How important is it to you (integer from 0 to 10)')
    temperature_optimal = forms.IntegerField(label='Optimal temperature')
    temperature_importance = forms.IntegerField(label='How important is it? (int from 0 to 10)')
    rental_costs_importance = forms.IntegerField(label='How important are low rental costs? (int from 0 to 10)')
    living_costs_importance = forms.IntegerField(label='How important are low living costs? (int from 0 to 10)')
    pollution_importance = forms.IntegerField(label='How important is low environmental pollution? (int from 0 to 10)')
    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = (
        ("1", "English"),
        ("2", "Spanish"),
        ("3", "Portugese"),
        ("4", "French"),
        ("5", "Polish"),
        ("6", "Romanian"),
        ("7", "Russian"),
        ("8", "Ukrainian")), label = 'Which languages do you know?')
    gdp_per_capita_importance = forms.IntegerField(label='How important is high gdp per capita?')
    continents = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = (
        ("1", "Europe"),
        ("2", "Asia"),
        ("3", "Africa"),
        ("4", "North America"),
        ("5", "South America"),
        ("6", "Australia")), label = 'Which continents would you like to live in?')
    continent_importance = forms.IntegerField(label='How important is continent to you?')
    air_pollution_importance = forms.IntegerField(label='How important is low air pollution? (int from 0 to 10)')
    freedom_importance = forms.IntegerField(label='How important is high level of freedom? (int from 0 to 10)')
    internet_price_importance = forms.IntegerField(label='How important are low internet prices? (int from 0 to 10)')
    


    # your_age = forms.IntegerField(label='Your age')
