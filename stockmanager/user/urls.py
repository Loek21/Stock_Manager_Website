from django.urls import path
from . import views

urlpatterns = [
    path("log in/", views.login_view, name="log in"),
    path("portfolio/", views.portfolio_view, name="portfolio"),
    path("DeleteAccount/", views.DeleteAccount, name="DeleteAccount"),
    path("ChangeEmail/", views.ChangeEmail, name="ChangeEmail"),
]
