from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def render_home_page(request):
    return render(request, 'home/home.html')
