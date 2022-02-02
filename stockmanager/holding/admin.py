from django.contrib import admin
from .models import Holding, RealTime, Reminder, WatchHolding

# Register your models here.
admin.site.register(Holding)
admin.site.register(RealTime)
admin.site.register(Reminder)
admin.site.register(WatchHolding)
