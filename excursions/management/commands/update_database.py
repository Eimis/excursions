from django.core.management.base import BaseCommand

from excursions.api import update_database


class Command(BaseCommand):
    help = 'Updates the database with data from csv files in the cloud'

    def handle(self, *args, **options):

        update_database()

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated database with new data.'
        ))
