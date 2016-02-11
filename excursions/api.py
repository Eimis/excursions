"""API logic for Excursions project (downloading the data files, updating the
database with data).
"""
import csv

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from excursions.models import City
from excursions.models import Hotel

import dropbox

# We're instantiating a new Dropbox instance here:
dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)


def update_data_files(
        CITIES_LOCAL_DATA_FILE_PATH,
        HOTELS_LOCAL_DATA_FILE_PATH,
        CITIES_REMOTE_DATA_FILE_PATH,
        HOTELS_REMOTE_DATA_FILE_PATH
        ):
    """A function that updates data files from the cloud. The required
    arguments are paths to where the file should be saved and paths to remote
    locations of the files.
    Note about remote file location: The files must be placed in the root
    directory for this app in Dropbox cloud ('/Dropbox/Apps/excursions/'), the
    path to the remote file at the root dir will the look like this: '/file.csv'
    """
    # Cities data file
    dropbox.Dropbox.files_download_to_file(
        dbx,
        CITIES_LOCAL_DATA_FILE_PATH,  # local file path
        CITIES_REMOTE_DATA_FILE_PATH,  # remote file path
    )
    # Hotels data file
    dropbox.Dropbox.files_download_to_file(
        dbx,
        HOTELS_LOCAL_DATA_FILE_PATH,
        HOTELS_REMOTE_DATA_FILE_PATH,
    )


def validate_file(file_to_validate):
    """A function that validates the data file.
    """
    try:
        # TODO: proper validation is probably needed:
        dialect = csv.Sniffer().sniff(
            file_to_validate,
        )
        return dialect
    except Exception as e:
        # for debugging:
        print(e)
        print(e)
        print(e)
        # Data file probably is not a csv file or it is empty:
        return False


def database_update_cities(cities_file):
    """A function that updates our database with data from csv files.
    """
    try:
        f = open(cities_file)

        # file validation:
        decoded_file = f.read(1024)
        dialect = validate_file(decoded_file)
        if not dialect:
            raise Exception(_('Something is wrong with data file, make ' +
                              'sure the file is valid'))

        # get back to the beginning of the file:
        f.seek(0)

        reader = csv.reader(f, delimiter=dialect.delimiter)

        for row in reader:
            city_short_name = row[0]
            city_full_name = row[1]

            city, created = City.objects.get_or_create(
                short_name=city_short_name,
                full_name=city_full_name,
            )
    finally:
        f.close()


def database_update_hotels(hotels_file):
    """A function that updates our database with data from csv files.
    """
    try:
        f = open(hotels_file)

        # file validation:
        decoded_file = f.read(1024)
        dialect = validate_file(decoded_file)
        if not dialect:
            raise Exception(_('Something is wrong with data file, make ' +
                              'sure the file is valid'))

        # get back to the beginning of the file:
        f.seek(0)

        reader = csv.reader(f, delimiter=dialect.delimiter)

        for row in reader:
            hotel_city = row[0]
            hotel_short_name = row[1]
            hotel_full_name = row[2]

            hotel, created = Hotel.objects.get_or_create(
                city=City.objects.get(short_name=hotel_city),
                short_name=hotel_short_name,
                full_name=hotel_full_name,
            )
    finally:
        f.close()


def update_database():
    """A function that updates our database with data from csv files. A
    cronjob should manage this.
    """
    # download and replace old data files with new ones:
    update_data_files(
        settings.CITIES_LOCAL_DATA_FILE_PATH,
        settings.HOTELS_LOCAL_DATA_FILE_PATH,
        settings.CITIES_REMOTE_DATA_FILE_PATH,
        settings.HOTELS_REMOTE_DATA_FILE_PATH,
    )

    # update the database with data from csv files:
    database_update_cities(settings.CITIES_LOCAL_DATA_FILE_PATH)
    database_update_hotels(settings.HOTELS_LOCAL_DATA_FILE_PATH)
