from django.urls import path
from . import views


urlpatterns = [
    path('', views.render_home_page, name='index'),
    path('home', views.render_home_page, name='get_name'),
]
