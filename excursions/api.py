"""API logic for Excursions project (downloading the data files, updating the
database with data).
"""

from django.conf import settings

import dropbox

# We're instantiating a new Dropbox instance:
dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)


def update_data_files():
    """A function that downloads and replaces data files from the cloud. A
    cronjob should manage this.
    """
    # Cities data file
    dropbox.Dropbox.files_download_to_file(
        dbx,
        settings.CITIES_LOCAL_DATA_FILE,
        settings.CITIES_REMOTE_DATA_FILE,
    )
    # Hotels data file
    dropbox.Dropbox.files_download_to_file(
        dbx,
        settings.HOTELS_LOCAL_DATA_FILE,
        settings.HOTELS_REMOTE_DATA_FILE,
    )
