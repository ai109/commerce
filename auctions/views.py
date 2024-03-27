from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listings, Comments, Bids

def listing(request, id):
    listing_data = Listings.objects.get(pk=id)
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    all_comments = Comments.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "listing_in_watchlist": listing_in_watchlist,
        "all_comments": all_comments,
        "is_owner": is_owner
    })

def expired_listings(request):
    expired_listings = Listings.objects.filter(active=False)
    return render(request, "auctions/expired_listings.html", {
        "expired_listings": expired_listings
    })

def close_auction(request, id):
    listing_data = Listings.objects.get(pk=id)
    listing_data.active = False
    listing_data.save()
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    all_comments = Comments.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "listing_in_watchlist": listing_in_watchlist,
        "all_comments": all_comments,
        "is_owner": is_owner,
        "update": True,
        "message": "Auction Closed."
    })

def new_bid(request, id):
    new_bid = request.POST["new_bid"]
    listing_data = Listings.objects.get(pk=id)
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    all_comments = Comments.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    if float(new_bid) > listing_data.price.bid:
        update_bid = Bids(user=request.user, bid=float(new_bid))
        update_bid.save()
        listing_data.price = update_bid
        listing_data.save()
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message":"Bid successfully updated",
            "update": True,
            "listing_in_watchlist": listing_in_watchlist,
            "all_comments": all_comments,
            "is_owner": is_owner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message":"Bid was not updated. Failed!",
            "update": False,
            "listing_in_watchlist": listing_in_watchlist,
            "all_comments": all_comments,
            "is_owner": is_owner,
        })

def new_comment(request, id):
    current_user = request.user
    listing_data = Listings.objects.get(pk=id)
    message = request.POST["new_comment"]

    new_comment = Comments(
        author=current_user,
        listing=listing_data,
        comment_text=message
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def display_watchlist(request):
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings,
    })


def remove(request, id):
    listing_data = Listings.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def add(request, id):
    listing_data = Listings.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def index(request):
    active_listings = Listings.objects.filter(active=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })

def displayCategory(request):
    if request.method == "POST":
        category_form = request.POST.get("category")
        if category_form:
            category = Category.objects.get(category_name=category_form)
            active_listings = Listings.objects.filter(active=True, category=category)
        else:
            active_listings = Listings.objects.filter(active=True)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_categories
        })
    else:
        return redirect('index')  # Redirect to all active listings if method is not POST

def makeListing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/new_listing.html", {
            "categories": all_categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user
        category_data = Category.objects.get(category_name=category)
        bid = Bids(bid=float(price), user=user)
        bid.save()
        newlisting = Listings(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=category_data,
            owner=user
        )
        newlisting.save()
        return HttpResponseRedirect(reverse(index))


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
