from django.db import models

# Create your models here.
class Securities(models.Model):
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
