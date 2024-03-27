from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.makeListing, name="new_listing"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<int:id>", views.add, name="add"),
    path("display_watchlist", views.display_watchlist, name="display_watchlist"),
    path("new_comment/<int:id>", views.new_comment, name="new_comment"),
    path("new_bid/<int:id>", views.new_bid, name="new_bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("expired/", views.expired_listings, name="expired_listings"),
]
