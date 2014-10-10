from django.db import models
from django.conf import settings


class AuctionState(models.Model):
    state_name = models.CharField(max_length=30)

    def __str__(self):
        return self.state_name

class AuctionCategory(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

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

    def __str__(self):
        return self.auction_name


