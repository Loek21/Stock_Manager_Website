from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=11, decimal_places=2)
    pname = models.CharField(max_length=60)
    pvalue = models.DecimalField(max_digits=11, decimal_places=2)
    pvaluep = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp = models.DecimalField(max_digits=5, decimal_places=2)
    updownpv = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp1 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp2 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp3 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp4 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp5 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp6 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp7 = models.DecimalField(max_digits=11, decimal_places=2)
    updownpp8 = models.DecimalField(max_digits=11, decimal_places=2)
