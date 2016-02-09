from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


def create_admin_user():
    '''A method which automatically crates Admin user
    '''
    # we need this there because of the
    # AppRegistryNotReady("Apps aren't loaded yet.") error:
    from django.contrib.auth.models import User

    if not User.objects.filter(username=settings.ADMIN_USERNAME):
        admin_user = User.objects.create(
            username=settings.ADMIN_USERNAME,
        )
        admin_user.set_password(settings.ADMIN_PASSWORD)
        admin_user.is_staff = True
        admin_user.is_superuser = True

        print(_(
            'Admin user was created successfully using credentials ' +
            'specified in settings.py file. Please do not forget to change ' +
            'the password immediately.'
        ))
        admin_user.save()


def create_initial_data(sender, **kwargs):
    '''Initial data functions that will be ran after each migration
    '''
    create_admin_user()
    # more methods can be added here. . .


class ExcursionsConfig(AppConfig):
    '''Excursions app configuration
    '''
    name = 'excursions'
    verbose_name = 'The Excursions app'

    def ready(self):
        post_migrate.connect(create_initial_data, sender=self)
