from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    car_type=models.CharField(max_length=255)
    car_number = models.CharField(max_length=8, unique = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.car_type} {self.car_number} {self.user}'