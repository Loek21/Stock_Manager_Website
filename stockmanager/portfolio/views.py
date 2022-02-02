# Loek van Steijn

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.models import Securities
from holding.models import RealTime, Holding, WatchHolding, Reminder
from .models import Portfolio
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint
import decimal
from datetime import datetime
import pytz
from django.http import JsonResponse, HttpResponse

# Create your views here.
def logout_view(request):
    """Logs user out and renders the homepage"""
    logout(request)
    return render(request, "home/index.html")

def AddPortfolio(request):
    """Creates a portfolio for a user with a user defined balance"""
    pname = request.POST["portfolio_name"]
    cash = request.POST["cash"]

    # if the name contains a space or the balanca is negative the portfolio wont be made
    if " " in pname or float(cash) < 0:
        return redirect("portfolio")
    portfolio = Portfolio.objects.create(user=request.user, cash=cash, pname=pname, pvalue=0, pvaluep=0, updownpp=0,
                                        updownpv=0, updownpp1=0, updownpp2=0, updownpp3=0, updownpp4=0, updownpp5=0,
                                        updownpp6=0, updownpp7=0, updownpp8=0)
    return redirect("portfolio")

def AddFunds(request):
    """Can add to a users portfolio balance"""
    funds = request.POST["fundsa"]

    # Checks if the entered amount is above 0
    if float(funds) < 0:
        return redirect("portfolio")
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect("portfolio")

    # Adds the amount to the portfolio and saves it
    portfolio.cash += decimal.Decimal(funds)
    portfolio.save()
    return redirect("portfolio")

def RemoveFunds(request):
    """Can remove from a users portfolio balance"""
    funds = request.POST["fundsr"]

    # Checks if the entered amount is above 0
    if float(funds) < 0:
        return redirect("portfolio")
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect("portfolio")

    # Checks if portfolio has enough funds to remove that amount
    if (portfolio.cash - decimal.Decimal(funds)) < 0:
        return redirect("portfolio")

    # Removes the amount from the portfolio and saves it
    portfolio.cash -= decimal.Decimal(funds)
    portfolio.save()
    return redirect("portfolio")

def Search(request):
    """Gets search request from search bar searches and redirects to holding"""
    search = request.POST["search"]
    search_list = search.split(" ")
    identifier = search_list[0]
    return redirect("holding", identifier)

def holding(request, ticker):
    """Gets search request from the search bar function and from links and renders the correct security page"""

    # Uses api to get intraday data
    identifier = ticker
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'OjliNTg3MDUwN2E3YTBiNDJlMjMxM2ViYzQ1NzJhN2E2'
    security_api = intrinio_sdk.SecurityApi()

    # Sets date to yesterday to obtain all intra day data from the api between yesterday and now
    tz_UTC = pytz.timezone('UTC')
    now = datetime.now(tz_UTC)

    # yesterday - 3 to take weekends into account as exchange is closed during the weekend
    yesterday = now.replace(day= now.day - 3)
    yesterday_year = int(yesterday.strftime("%Y"))
    yesterday_month = int(yesterday.strftime("%m"))
    yesterday_day = int(yesterday.strftime("%d"))
    yesterday_date = datetime(yesterday_year, yesterday_month, yesterday_day)
    yesterday_time = yesterday.strftime("%H, %M, %S")

    source = ""
    start_date = yesterday_date
    start_time = yesterday_time
    end_date = ''
    end_time = ''
    page_size = 100
    next_page = ''

    try:
        api_response_intra = security_api.get_security_intraday_prices(identifier, source=source, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, page_size=page_size, next_page=next_page)
    except ApiException as e:
        return redirect("portfolio")

    try:
        data = RealTime.objects.get(ticker=identifier)
    except RealTime.DoesNotExist:
        return redirect("portfolio")

    # Creating Graph data and labels
    intra = {"label":[], "lprice": []}
    counter = 0
    for each in api_response_intra.intraday_prices:

        # Gets first value and adds full date for graph label
        if counter == 0:
            minute = each.time.minute

            # adds 0 to minute if value is under 10
            if minute < 10:
                minute = f"0{minute}"
            date = f"{each.time.day}/{each.time.month} {each.time.hour}:{minute}"
            intra["label"].append(date)
            intra["lprice"].append(each.last_price)
            counter += 1

        # gets last value and adds full date for graph label
        elif counter == len(api_response_intra.intraday_prices) - 1:
            minute = each.time.minute
            if minute < 10:
                minute = f"0{minute}"
            date = f"{each.time.day}/{each.time.month} {each.time.hour}:{minute}"
            intra["label"].insert(0, date)
            intra["lprice"].insert(0, each.last_price)
        else:
            hour = each.time.hour
            minute = each.time.minute
            if minute < 10:
                minute = f"0{minute}"
            time = f"{hour}:{minute}"
            counter += 1
            if time not in intra["label"]:
                intra["label"].insert(0, time)
                intra["lprice"].insert(0, each.last_price)

    try:
        portfolios = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolios = None
    context = {"stocks": Securities.objects.all(), "portfolios": portfolios, "RealTime": data, "Intra": api_response_intra, "Graph": intra}
    return render(request, "holding/index.html", context)

def watchlist(request):
    """Gets all the data required to render the watchlist page"""
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolio = None
    try:
        holdings = Holding.objects.filter(content=portfolio).all()
    except Holding.DoesNotExist:
        holdings = None
    try:
        watchholding = WatchHolding.objects.filter(user=request.user).all()
    except WatchHolding.DoesNotExist:
        return redirect("portfolio")
    context = {"stocks": Securities.objects.all().filter(currency="USD"), "portfolio": portfolio, "holdings": holdings, "watchlist": watchholding}
    return render(request, "portfolio/watchlist.html", context)

def Account(request):
    """Gets all the data required to render the accounts page"""
    try:
        reminders = Reminder.objects.all().filter(user=request.user)
    except Reminder.DoesNotExist:
        reminders = None
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolio = None
    context = {"Alerts": reminders, "portfolio": portfolio}
    return render(request, "portfolio/account.html", context)
