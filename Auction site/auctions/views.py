from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import *


def index(request):
    temp = Auction.objects.all()
    return render(request, "auctions/index.html",{
        "Lists" : temp
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        amnt = request.POST["bid"]
        url = request.POST["url"]
        cate = Category(categoryName=request.POST["category"])
        cate.save()
        owner = request.user
        bid = Bid(amnt = amnt, user = owner)
        bid.save()
        time = datetime.datetime.now().replace(microsecond=0)
        Auction(title=title,desc=desc,start_bid=bid, user=owner ,urls=url,category=cate, time=time).save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def listing(request, id):
    auction = Auction.objects.get(pk=id)
    comments = Comment.objects.filter(auction=auction)
    inlistwatchlist = request.user in auction.watchlist.all()
    if request.method == 'POST':
        prev_bid = (auction.start_bid.amnt)
        current_bid = int(request.POST["val1"])
        if current_bid > prev_bid:
            curr = Bid(user=request.user, amnt=current_bid)
            curr.save()
            auction.start_bid = curr
            auction.save()
            return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
        else:
            return render(request, "auctions/list.html",{
                "msg" : True,
                "list" : auction,
                "inlist" : inlistwatchlist,
                "comment" : comments                 
            })
    return render(request, "auctions/list.html", {
        "list" : auction,
        "inlist" : inlistwatchlist,
        "comment" : comments
    })

def close(request, id):
    auction = Auction.objects.get(pk=id)
    auction.isActive = False
    auction.save()
    inlistwatchlist = request.user in auction.watchlist.all()
    return render(request, "auctions/list.html", {
        "list" : auction,
        "inlist" : inlistwatchlist
    })

def comment(request, id):
    auction = Auction.objects.get(pk=id)
    user = request.user
    msg = request.POST["msg"]
    Comment(auction=auction, user=user, msg=msg).save()
    return HttpResponseRedirect(reverse("listing", args=(auction.id,)))


def displaywatchlist(request):
    curr = request.user
    lis = curr.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "list" : lis
    })

def addlist(request, id):
    if request.method == 'POST':
        curr = Auction.objects.get(pk=id)
        curr.watchlist.add(request.user)
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def removelist(request, id):
    if request.method == 'POST':
        curr = Auction.objects.get(pk=id)
        curr.watchlist.remove(request.user)
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def search(request):
    if request.method == "POST":
        val = request.POST["category"]
        cat = Category.objects.get(categoryName=val)
        lis = list(Auction.objects.filter(category=cat))  
        return render(request, "auctions/Category.html",{
            "list" : lis
        })
    return render(request, "auctions/search.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
