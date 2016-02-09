import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from excursions.models import City
from excursions.models import Hotel


def explore(request):
    '''A main view for rendering City / Hotel selection
    '''
    cities = City.objects.all()
    return render(request, 'explore.html', {
        'cities': cities,
    })


def get_city_hotels(request):
    '''A view that returns JSON data for Hotels that belong to a POSTed City
    '''
    if request.method == 'POST' and request.is_ajax():
        city = City.objects.get(short_name=request.POST['city_short_name'])
        hotels = Hotel.objects.filter(city=city).order_by('full_name')
        response_data = serializers.serialize(
            'json',
            hotels,
            use_natural_foreign_keys=True,
        )
        return HttpResponse(response_data)
    else:
        return HttpResponse(status=401)  # forbidden
