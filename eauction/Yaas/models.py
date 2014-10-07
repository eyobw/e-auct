from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class AuctionState(models.Model):
    state_name = models.CharField(max_length=30)


class AuctionCategory(models.Model):
    category_name = models.CharField(max_length=30)

class Auction(models.Model):
    auction_name = models.CharField(max_length=30)
    auction_description = models.TextField()
    price_min = models.DecimalField(max_digits=5, decimal_places=2)
    price_max = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.ForeignKey(AuctionCategory)
    state = models.ForeignKey(AuctionState)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)



# Create your models here.
