from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Bids(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user_bid")
    def __str__(self):
        return f"€{self.bid} from {self.user}"

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_price")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True, related_name = "category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    
    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user_comment")
    listing = models.ForeignKey(Listings, on_delete = models.CASCADE, blank = True, null = True, related_name = "listings_comment")
    comment_text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"