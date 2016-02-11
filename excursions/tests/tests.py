"""Functional tests for Excursions app.
TODO: JSON fixtures or Factory Boy implementation
"""
import csv
import os

from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from excursions.api import update_data_files
from excursions.api import database_update_cities
from excursions.api import database_update_hotels
from excursions.api import validate_file
from excursions.models import City
from excursions.models import Hotel


class ExcursionsInterfaceTestCase(WebTest):
    """Tests for mainly testing app's view functions
    """

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
        """Test main page http status
        """
        response = self.app.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)

    def test_filter_hotel_by_city(self):
        """Test if hotels are filtered by the city correctly
        """
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


class ExcursionsApiTestCase(WebTest):
    """Tests for testing app's api
    """

    def test_update_database(self):
        """Test if database is updated with data from csv files in the cloud.
        """
        # According to the current data in csv files used for testing, the
        # first city will contain 2 hotels, second one will only have one.
        # See these files in the cloud for refference.
        self.assertEqual(
            City.objects.all().count(),
            0
        )
        self.assertEqual(
            Hotel.objects.all().count(),
            0
        )
        # update the data files:
        update_data_files(
            settings.TEST_CITIES_LOCAL_DATA_FILE_PATH,
            settings.TEST_HOTELS_LOCAL_DATA_FILE_PATH,
            settings.TEST_CITIES_REMOTE_DATA_FILE_PATH,
            settings.TEST_HOTELS_REMOTE_DATA_FILE_PATH,
        )
        # update the temp. test database with data from csv files:
        database_update_cities(settings.TEST_CITIES_LOCAL_DATA_FILE_PATH)
        database_update_hotels(settings.TEST_HOTELS_LOCAL_DATA_FILE_PATH)

        # test object count:
        self.assertEqual(
            City.objects.all().count(),
            2
        )
        self.assertEqual(
            Hotel.objects.all().count(),
            3
        )

        # test field values:
        # city objects:
        try:
            f = open(settings.TEST_CITIES_LOCAL_DATA_FILE_PATH)

            # file validation:
            decoded_file = f.read(1024)
            dialect = validate_file(decoded_file)
            if not dialect:
                self.fail('Something is wrong with data file, make ' +
                          'sure the file is valid')

            # get back to the beginning of the file:
            f.seek(0)

            reader = csv.reader(f, delimiter=dialect.delimiter)

            for row in reader:
                city_short_name = row[0]
                city_full_name = row[1]

                assert City.objects.filter(
                    short_name=city_short_name,
                    full_name=city_full_name
                ).exists()
        finally:
            f.close()

        # hotel objects:
        try:
            f = open(settings.TEST_HOTELS_LOCAL_DATA_FILE_PATH)

            # file validation:
            decoded_file = f.read(1024)
            dialect = validate_file(decoded_file)
            if not dialect:
                self.fail('Something is wrong with data file, make ' +
                          'sure the file is valid')

            # get back to the beginning of the file:
            f.seek(0)

            reader = csv.reader(f, delimiter=dialect.delimiter)

            for row in reader:
                hotel_city = row[0]
                hotel_short_name = row[1]
                hotel_full_name = row[2]

                # we're also checking if Hotel > City relations are correct
                # here:
                assert Hotel.objects.filter(
                    city=City.objects.get(short_name=hotel_city),
                    short_name=hotel_short_name,
                    full_name=hotel_full_name,
                ).exists()
        finally:
            f.close()

    def tearDown(self):
        # remove csv files that were downloaded from the cloud:
        os.remove(settings.TEST_CITIES_LOCAL_DATA_FILE_PATH)
        os.remove(settings.TEST_HOTELS_LOCAL_DATA_FILE_PATH)
