from django.shortcuts import render

from excursions.models import City


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
    pass
