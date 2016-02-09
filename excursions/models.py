from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    short_name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.full_name


class Hotel(models.Model):
    city = models.ForeignKey(City)
    short_name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
