from datetime import date
from django.db import models
from django.utils.timezone import *
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    pass


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    national_code = models.CharField(max_length=15)
    disease = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
