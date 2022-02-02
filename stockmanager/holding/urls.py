from django.urls import path
from . import views

urlpatterns = [
    path("Buy/", views.Buy, name="Buy"),
    path("Sell/", views.Sell, name="Sell"),
    path("AddReminder/", views.AddReminder, name="AddReminder"),
    path("AddWatch/<str:ticker>/", views.AddWatch, name="AddWatch"),
    path("RemoveWatch/<str:ticker>/", views.RemoveWatch, name="RemoveWatch"),
    path("RemoveAlert/<str:name>/", views.RemoveAlert, name="RemoveAlert"),
]
