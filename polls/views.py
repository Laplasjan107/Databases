from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from world_data.models import WorldHappiness
from .forms import CityForm

def compute_result(form):
    pass #tu bedzie obliczanie wyniku dla kazdego miasta

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
            rendered = render(request, 'polls/submited.html', {'name': name}, {'languages': languages[0]}) 
            return rendered

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    
    return render(request, 'polls/name.html', {'form': form})
