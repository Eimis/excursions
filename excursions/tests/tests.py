"""Functional tests for Excursions app.
TODO: JSON fixtures or Factory Boy implementation
"""

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from excursions.models import City
from excursions.models import Hotel


class ExcursionsAppTestCase(WebTest):

    def setUp(self):
        # first city will contain 2 hotels, second one will only have one.
        self.first_city = City.objects.create(
            short_name='VNO',
            full_name='Vilnius',
        )
        self.second_city = City.objects.create(
            short_name='AMS',
            full_name='Amsterdam',
        )
        self.first_hotel = Hotel.objects.create(
            short_name='CRWNP',
            full_name='Crown Plazza',
            city=self.first_city,
        )
        self.second_hotel = Hotel.objects.create(
            short_name='RDSN',
            full_name='Raddison',
            city=self.first_city,
        )
        self.third_hotel = Hotel.objects.create(
            short_name='SHKSPR',
            full_name='Shakespeare hotel',
            city=self.second_city,
        )

    def test_explore_page_status(self):
        response = self.app.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)

    def test_filter_hotel_by_city(self):
        # We are testing the case of Hotel search in the 1st city:
        self.app.get(reverse('explore'))
        response = self.client.post(
            reverse('get_city_hotels'), {
                'city_short_name': self.first_city.short_name,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        # test response status:
        self.assertEqual(response.status_code, 200)

        # test if correct number of results are returned. json() method also
        # checks if HttpResponse has the correct content type:
        self.assertEqual(
            len(response.json()),
            2
        )

        # test if correct Hotels are returned:
        # 1st hotel:
        self.assertEqual(
            response.json()[0]['fields']['city'],
            self.first_city.full_name
        )
        self.assertEqual(
            response.json()[0]['fields']['full_name'],
            self.first_hotel.full_name
        )
        # 2nd hotel:
        self.assertEqual(
            response.json()[1]['fields']['city'],
            self.first_city.full_name
        )
        self.assertEqual(
            response.json()[1]['fields']['full_name'],
            self.second_hotel.full_name
        )
