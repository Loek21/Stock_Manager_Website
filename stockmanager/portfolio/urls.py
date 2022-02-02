from django.urls import path
from . import views

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("AddPortfolio/", views.AddPortfolio, name="AddPortfolio"),
    path("AddFunds/", views.AddFunds, name="AddFunds"),
    path("RemoveFunds/", views.RemoveFunds, name="RemoveFunds"),
    path("Search/", views.Search, name="Search"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("Security/<str:ticker>/", views.holding, name="holding"),
    path("Account/", views.Account, name="Account"),
]
