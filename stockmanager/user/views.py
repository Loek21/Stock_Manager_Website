# Loek van Steijn

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Securities
from portfolio.models import Portfolio
from holding.models import Holding, RealTime, Reminder, WatchHolding
from datetime import datetime
import pytz
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint
from background_task import background
import decimal

# Create your views here.
def login_view(request):
    """Logs user in"""
    username = request.POST["username"]
    password = request.POST["password"]

    # Checks if user is authenticated and logs user in
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect((reverse("portfolio")))
    return redirect("index")

def portfolio_view(request):
    """Renders view of my portfolio"""

    # Tries to get the users portfolio
    try:
        portfolios = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        portfolios = None

    # Tries to get all the holdings belonging to that portfolio
    try:
        holdings = Holding.objects.filter(content=portfolios).all()
    except Holding.DoesNotExist:
        holdings = None

    # Generates data and labels for graph on the page
    data_labels = {"labels": [], "points": []}
    if portfolios != None:
        tz_UTC = pytz.timezone('UTC')
        now = datetime.now(tz_UTC)

        # range 9 covers all 9 previous days
        for i in range(9):
            day_change = now.replace(day= now.day - i)
            day = day_change.day
            if int(day) > int(now.day):
                month = now.replace(month= now.month - 1)
            else:
                month = now.month

            # adds 0 if day is under the 10
            if day < 10:
                day = f"0{day}"

            # adds 0 if month is under the 10
            if month < 10:
                month = f"0{month}"
            calander_date = f"{day}/{month}"
            data_labels["labels"].insert(0, calander_date)
        data_labels["points"] = [portfolios.updownpp8, portfolios.updownpp7, portfolios.updownpp6,
                                portfolios.updownpp5, portfolios.updownpp4, portfolios.updownpp3,
                                portfolios.updownpp2, portfolios.updownpp1, portfolios.updownpp]

    # These commented functions call the background task functions (meant to be inactive as it will create a new task everytime)
    # update(repeat=60, repeat_until=None)
    # update_portfolio_report(repeat=86400, repeat_until=None)

    context = {"stocks": Securities.objects.all().filter(currency="USD"), "portfolios": portfolios, "holdings": holdings, "data": data_labels}
    return render(request, "portfolio/index.html", context)

def DeleteAccount(request):
    """Deletes users account"""
    user = request.user
    user.delete()
    return redirect("index")

def ChangeEmail(request):
    """Changes users email adress if it contains a @"""
    user = request.user
    new_email = request.POST["new_email"]
    if "@" in new_email:
        user.email = new_email
        user.save()
    return redirect("portfolio")

@background()
def update():
    """
    Background updates the portfolio, holding, security and reminder databases every 60 seconds
    It contains print statements to show that background tasks are running in python manage.py process_tasks
    """

    # Updates the realtime value of securities
    securities = Securities.objects.all().filter(currency="USD")
    for security in securities:
        identifier = security.ticker
        name = security.name
        source = ""
        intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'OjliNTg3MDUwN2E3YTBiNDJlMjMxM2ViYzQ1NzJhN2E2'
        security_api = intrinio_sdk.SecurityApi()
        try:
            api_response_realtime = security_api.get_security_realtime_price(identifier, source=source)
        except ApiException as e:
            print("Exception when calling SecurityApi->get_security_intraday_prices: %s\r\n" % e)
        try:
            realtime = RealTime.objects.get(ticker=identifier)
        except RealTime.DoesNotExist:
            realtime = RealTime.objects.create(ticker=identifier)

        realtime.date = api_response_realtime.last_time
        # exchange closes at 9pm (hour = 21)
        realtime.last_price_hour = realtime.date.hour
        if realtime.last_price_hour == 21:
            realtime.lastpricep = api_response_realtime.last_price
        if api_response_realtime.last_price == "None":
            realtime.lastprice = None
        else:
            realtime.lastprice = api_response_realtime.last_price
        if api_response_realtime.ask_price == "None":
            realtime.askprice = None
        else:
            realtime.askprice = api_response_realtime.ask_price
        if api_response_realtime.bid_price == "None":
            realtime.bidprice = None
        else:
            realtime.bidprice = api_response_realtime.bid_price
        if api_response_realtime.high_price == "None":
            realtime.highprice = None
        else:
            realtime.highprice = api_response_realtime.high_price
        if api_response_realtime.low_price == "None":
            realtime.lowprice = None
        else:
            realtime.lowprice = api_response_realtime.low_price
        realtime.updated = api_response_realtime.updated_on
        realtime.updownrp = ((100 * decimal.Decimal(realtime.lastprice)) / decimal.Decimal(realtime.lastpricep)) - 100
        realtime.updownrv = decimal.Decimal(realtime.lastprice) - decimal.Decimal(realtime.lastpricep)
        realtime.name = name
        realtime.save()
        print(f"updated realtime data {security.name}")

    # Updating individual holdings
    holdings = Holding.objects.all()
    for holding in holdings:
        identifier = holding.hname
        realtime = RealTime.objects.get(ticker=identifier)
        if holding.hnumber != 0:
            holding.hvalue = decimal.Decimal(holding.hnumber) * decimal.Decimal(realtime.lastprice)
            holding.hvaluep = decimal.Decimal(holding.hnumber) * decimal.Decimal(realtime.lastpricep)
            holding.updownhp = ((100 * decimal.Decimal(realtime.lastprice)) / decimal.Decimal(realtime.lastpricep)) - 100
            holding.updownhv = (decimal.Decimal(holding.hnumber) * decimal.Decimal(realtime.lastprice)) - (decimal.Decimal(holding.hnumber) * decimal.Decimal(realtime.lastpricep))
        holding.save()
        print(f"updated holding {holding.hname}")

    # Updating individual portfolios
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        user = portfolio.user
        holdings = Holding.objects.all().filter(user=user)
        port_value = 0
        port_valuep = 0
        for holding in holdings:
            port_value += holding.hvalue
            port_valuep += holding.hvaluep

        if port_value != 0:
            portfolio.pvalue = port_value
            portfolio.pvaluep = port_valuep
            portfolio.updownpp = ((100 * decimal.Decimal(port_value)) / decimal.Decimal(port_valuep)) - 100
            portfolio.updownpv = decimal.Decimal(port_value) - decimal.Decimal(port_valuep)
            portfolio.save()
        print(f"updated portfolio {user}")

    # Updates watchlists
    watchholdings = WatchHolding.objects.all()
    for watchholding in watchholdings:
        ticker = watchholding.whname
        realtime = RealTime.objects.get(ticker=ticker)
        watchholding.whnamef=realtime.name
        watchholding.whname=ticker
        watchholding.whvalue=realtime.lastprice
        watchholding.whvaluep=realtime.lastpricep
        watchholding.wupdownhp=realtime.updownrp
        watchholding.wupdownhv=realtime.updownrv
        watchholding.save()
        print(f"Updates watchlist for {watchholding.user}")

    # Updates and sends reminder emails
    reminders = Reminder.objects.all()
    for reminder in reminders:
        user = reminder.user
        ticker = reminder.holdingname
        realtime = RealTime.objects.get(ticker=ticker)
        subject = f"Alert for {realtime.name} as been triggered!"
        user_data = User.objects.get(username=user)
        from_email = settings.EMAIL_HOST_USER
        to_list = [user_data.email]

        # Deletes all alerts at the end of trading day
        if realtime.last_price_hour == 21:
            reminder.delete()
        elif reminder.unit == "%" and (reminder.valueUp <= realtime.updownrp or reminder.valueDown >= realtime.updownrp):
            message = f"{realtime.name} is now at ${realtime.lastprice} and is up/down {realtime.updownrp}%"
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            reminder.delete()
        elif reminder.unit == "$" and (reminder.valueUp <= realtime.updownrv or reminder.valueDown >= realtime.updownrv):
            message = f"{realtime.name} is now at ${realtime.lastprice} and is up/down ${realtime.updownrv}"
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            reminder.delete()
        print(f"updated reminder alert for {user} on {ticker}")

    print("Cycle completed ------------------------------------------------:)")

@background()
def update_portfolio_report():
    """Updates all the portfolio margins daily"""
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        portfolio.updownpp8 = portfolio.updownpp7
        portfolio.updownpp7 = portfolio.updownpp6
        portfolio.updownpp6 = portfolio.updownpp5
        portfolio.updownpp5 = portfolio.updownpp4
        portfolio.updownpp4 = portfolio.updownpp3
        portfolio.updownpp3 = portfolio.updownpp2
        portfolio.updownpp2 = portfolio.updownpp1
        portfolio.updownpp1 = portfolio.updownpp
        portfolio.save()
        print(f"updated portfolio weekly report {portfolio.user}")
