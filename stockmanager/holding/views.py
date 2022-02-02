# Loek van Steijn

from django.shortcuts import render, redirect
from .models import Holding, RealTime, Reminder, WatchHolding
from portfolio.models import Portfolio
from user.models import Securities
import decimal

# Create your views here.
def Buy(request):
    """Buys a specified number of securities"""
    ticker = request.POST["tickerb"]
    aprice = request.POST.get("apb", False)
    lprice = request.POST.get("lpb", False)
    hnumberb = request.POST["number_of_holdingsb"]

    # Gets all the required data
    try:
        security = Securities.objects.get(ticker=ticker)
    except:
        return redirect("portfolio")
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect("portfolio")
    try:
        current_holding = Holding.objects.get(user=request.user, hname=ticker, hnamef=security.name)
    except Holding.DoesNotExist:
        current_holding = Holding.objects.create(user=request.user, hname=ticker, hnamef=security.name, hnumber=0, hvalue=0, hvaluep=0, updownhp=0, updownhv=0)
    try:
        realtime = RealTime.objects.get(ticker=ticker)
    except RealTime.DoesNotExist:
        return redirect("portfolio")

    # Changes ask price to last price if askprice is unavailable
    if aprice == False:
        aprice = lprice

    # if current balance not sufficient the order will not continue
    if (int(hnumberb) * float(aprice)) > float(portfolio.cash):
        return redirect("portfolio")

    current_holding.hnumber += int(hnumberb)
    current_holding.hvalue = (float(current_holding.hnumber) * float(realtime.lastprice))
    portfolio.cash -= (decimal.Decimal(hnumberb) * decimal.Decimal(aprice))
    portfolio.pvalue += (decimal.Decimal(hnumberb) * decimal.Decimal(realtime.lastprice))
    current_holding.content = portfolio
    current_holding.save()
    portfolio.save()
    return redirect("portfolio")

def Sell(request):
    """Sell a specified number of securities"""
    ticker = request.POST["tickers"]
    bprice = request.POST.get("bps", False)
    lprice = request.POST.get("lps", False)
    hnumbers = request.POST["number_of_holdingss"]

    # Tries to collect data from database
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect("portfolio")
    try:
        current_holding = Holding.objects.get(user=request.user, hname=ticker)
    except Holding.DoesNotExist:
        return redirect("portfolio")
    try:
        realtime = RealTime.objects.get(ticker=ticker)
    except RealTime.DoesNotExist:
        return redirect("portfolio")

    # If bprice doesn't exist it is the last price
    if bprice == False:
        bprice = lprice

    # Checks if user has enough holdings to sell
    if int(hnumbers) > int(current_holding.hnumber):
        return redirect("portfolio")

    # Adjusts and saves data
    current_holding.hnumber -= int(hnumbers)
    current_holding.hvalue = (float(current_holding.hnumber) * float(realtime.lastprice))

    portfolio.cash += (decimal.Decimal(hnumbers) * decimal.Decimal(bprice))
    portfolio.pvalue -= (decimal.Decimal(hnumbers) * decimal.Decimal(realtime.lastprice))
    current_holding.content = portfolio
    current_holding.save()
    portfolio.save()
    if current_holding.hnumber == 0:
        current_holding.content = None
        current_holding.delete()

    # if every holding has been sold it puts all added security profit or loss into the funds
    holdings = Holding.objects.all().filter(user=request.user)
    if not holdings:
        portfolio.cash += portfolio.pvalue
        portfolio.pvalue = 0
        portfolio.save()

    return redirect("portfolio")

def AddReminder(request):
    """Allows user to add an alert"""
    ticker = request.POST["holding_name"]
    value_up = request.POST["holding_value_up"]
    value_down = request.POST["holding_value_down"]

    # Checks if units has been filled in
    try:
        unit = request.POST["holding_units"]
    except:
        return redirect("portfolio")

    realtime = RealTime.objects.get(ticker=ticker)

    # Checks if up/down limits are correct in comparison to the current last price of the security
    if unit == "$" and (decimal.Decimal(value_up) <= realtime.updownrv or decimal.Decimal(value_down) >= realtime.updownrv):
        return redirect("portfolio")
    if unit == "%" and (decimal.Decimal(value_up) <= realtime.updownrp or decimal.Decimal(value_down) >= realtime.updownrp):
        return redirect("portfolio")

    try:
        reminder = Reminder.objects.get(user=request.user, holdingname=ticker)
    except Reminder.DoesNotExist:
        reminder = Reminder.objects.create(user=request.user, holdingname=ticker, valueUp=value_up, valueDown=value_down, unit=unit)

    return redirect("Account")

def AddWatch(request, ticker):
    """Adds security to watchlist if it is not already on the watchlist"""
    try:
        realtime = RealTime.objects.get(ticker=ticker)
    except RealTime.DoesNotExist:
        return redirect("watchlist")
    try:
        watchholding = WatchHolding.objects.get(user=request.user, whnamef=realtime.name)
    except WatchHolding.DoesNotExist:
        watchholding = WatchHolding.objects.create(user=request.user, whnamef=realtime.name, whname=ticker, whvalue=realtime.lastprice, whvaluep=realtime.lastpricep, wupdownhp=realtime.updownrp, wupdownhv=realtime.updownrv)
    return redirect("watchlist")


def RemoveWatch(request, ticker):
    """Deletes a security from watchlist"""
    try:
        watchholding = WatchHolding.objects.get(user=request.user, whname=ticker)
    except WatchHolding.DoesNotExist:
        return redirect("watchlist")

    watchholding.delete()
    return redirect("watchlist")

def RemoveAlert(request, name):
    """Deletes a security from alert list"""
    try:
        reminder = Reminder.objects.get(user=request.user, holdingname=name)
    except Reminder.DoesNotExist:
        return redirect("Account")
    reminder.delete()
    return redirect("Account")
