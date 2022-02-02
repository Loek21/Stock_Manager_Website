from django.db import models
from django.contrib.auth.models import User
from portfolio.models import Portfolio

# Create your models here.
class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=True, blank=True)
    hnamef = models.CharField(max_length=60)
    hname = models.CharField(max_length=60)
    hnumber = models.IntegerField()
    hvalue = models.DecimalField(max_digits=11, decimal_places=2)
    hvaluep = models.DecimalField(max_digits=11, decimal_places=2)
    updownhp = models.DecimalField(max_digits=5, decimal_places=2)
    updownhv = models.DecimalField(max_digits=11, decimal_places=2)

class RealTime(models.Model):
    ticker = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    date =  models.CharField(max_length=60)
    last_price_hour = models.IntegerField()
    lastprice = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    askprice = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    bidprice = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    highprice = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    lowprice = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    updated = models.CharField(max_length=60)
    lastpricep = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    updownrp = models.DecimalField(max_digits=5, decimal_places=2)
    updownrv = models.DecimalField(max_digits=5, decimal_places=2)

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holdingname =  models.CharField(max_length=60)
    valueUp = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    valueDown = models.DecimalField(null=True, blank=True, max_digits=11, decimal_places=2)
    unit = models.CharField(max_length=1)

class WatchHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    whnamef = models.CharField(max_length=60)
    whname = models.CharField(max_length=60)
    whvalue = models.DecimalField(max_digits=11, decimal_places=2)
    whvaluep = models.DecimalField(max_digits=11, decimal_places=2)
    wupdownhp = models.DecimalField(max_digits=5, decimal_places=2)
    wupdownhv = models.DecimalField(max_digits=11, decimal_places=2)
