from django.db import models


class City(models.Model):
    short_name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=50)


class Hotel(models.Model):
    city = models.ForeignKey(City)
    short_name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
