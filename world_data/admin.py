from django.contrib import admin

from django.shortcuts import render
from django.urls import path
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import WorldHappiness, WorldCities, InternetPrices


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class WorldHappinessAdmin(admin.ModelAdmin):
    list_display = ('country_name',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8").replace('\r', '0')
            csv_data = file_data.split("\n")
            first = True
            for x in csv_data:
                if len(x) == 0:
                    break
                if first:
                    first = False
                    continue
                fields = x.split(",")
                fields_with_nulls = []
                for i in range(11):
                    if not fields[i]:
                        fields_with_nulls.append(None)
                    else:
                        fields_with_nulls.append(fields[i])
                created = WorldHappiness.objects.update_or_create(
                    country_name=fields_with_nulls[0],
                    year=fields_with_nulls[1],
                    life_ladder=fields_with_nulls[2],
                    log_GDP_per_capita=fields_with_nulls[3],
                    social_support=fields_with_nulls[4],
                    healthy_life_expectancy=fields_with_nulls[5],
                    freedom_of_life_choices=fields_with_nulls[6],
                    generosity=fields_with_nulls[7],
                    perceptions_of_corruption=fields_with_nulls[8],
                    positive_affect=fields_with_nulls[9],
                    negative_affect=fields_with_nulls[10],
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class WorldCitiesAdmin(admin.ModelAdmin):
    list_display = ('city',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        WorldCities.objects.all().delete()
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8").replace('\r', '0')
            csv_data = file_data.split("\n")
            first = True
            for x in csv_data:
                if len(x) == 0:
                    break
                if first:
                    first = False
                    continue
                fields = x.split("\",\"")
                fields_with_nulls = []
                for field in fields:
                    if not field:
                        fields_with_nulls.append(None)
                    else:
                        fields_with_nulls.append(field.replace("\"", ""))

                try:
                    created = WorldCities.objects.update_or_create(
                        city=fields_with_nulls[0],
                        city_ascii=fields_with_nulls[1],
                        latitude=float(fields_with_nulls[2]),
                        longitude=float(fields_with_nulls[3]),
                        country=fields_with_nulls[4],
                        iso2=fields_with_nulls[5],
                        iso3=fields_with_nulls[6],
                        admin_name=fields_with_nulls[7],
                        capital=fields_with_nulls[8],
                        population=fields_with_nulls[9],
                    )
                except:
                    print("falied to create " + fields_with_nulls[0])
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class InternetPricesAdmin(admin.ModelAdmin):
    list_display = ('city',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        WorldCities.objects.all().delete()
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8").replace('\r', '0')
            csv_data = file_data.split("\n")
            skip = 2
            for x in csv_data:
                if len(x) == 0:
                    break
                if skip > 0:
                    skip -= 1
                    continue
                fields = x.split("\", ")
                print(fields)
                fields_with_nulls = []
                for field in fields:
                    if not field:
                        fields_with_nulls.append(None)
                    else:
                        fields_with_nulls.append(field.replace("\"", ""))
                print(fields_with_nulls)
                try:
                    created = InternetPrices.objects.update_or_create(
                        city=fields_with_nulls[0],
                        country=fields_with_nulls[2],
                        price_usd=float(fields_with_nulls[3]),
                    )
                except Exception:
                    print("falied to create " + fields_with_nulls[0])
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# Register your models here.


admin.site.register(WorldHappiness, WorldHappinessAdmin)
admin.site.register(WorldCities, WorldCitiesAdmin)
admin.site.register(InternetPrices, InternetPricesAdmin)
