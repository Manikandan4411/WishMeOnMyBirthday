from django.db import models
from datetime import datetime

class Users(models.Model):
  username = models.CharField(max_length=50, unique="True")
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  email = models.EmailField(max_length=100, unique="True")
  registration_confirmation = models.BooleanField(default="False")
  password = models.CharField(max_length=20)
  confirm_password = models.CharField(max_length=20)
  birth_date = models.DateField()
  age = models.IntegerField(default=0)
  class Meta:
    db_table = "user_details"