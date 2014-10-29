__author__ = 'eyob'
from Yaas.models import Auction
from datetime import datetime, timedelta


def do(self):
        auctions = Auction.objects.order_by('end_date').filter(state_id=1)
        for auction in auctions:
            if auction.end_date < datetime.now():
                auction.state_id = 4