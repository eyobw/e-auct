from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime

class ConcurrentModificationError(Exception):
    def __init__(self, model, pk):
        super(ConcurrentModificationError, self).__init__(
            "Concurrent modification on %s #%s" % (model, pk))


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
    price_min = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField()
    category = models.ForeignKey(AuctionCategory)
    state = models.ForeignKey(AuctionState, default='1')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.auction_name

    def save(self, *args, **kwargs):
        cls = self.__class__
        if self.pk:
            rows = cls.objects.filter(
                pk=self.pk, version=self.version).update(
                version=self.version + 1)
            if not rows:
                raise ConcurrentModificationError(cls.__name__, self.pk)
            self.version += 1
        super(Auction, self).save(*args, **kwargs)

class Bidder(models.Model):
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    item = models.ForeignKey(Auction, related_name='bidders')
    bidder_name = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bidder')

    def __str__(self):
        return '%s: %d' %(self.bidder_name.username, self.price)