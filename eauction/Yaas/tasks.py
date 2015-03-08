__author__ = 'eyob'
from Yaas.models import Auction, Bidder
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Max
from django.core.mail import send_mail


def do_task():
        auctions = Auction.objects.order_by('end_date').filter(state_id=1)
        for auction in auctions:
            if auction.end_date < datetime.now():
                b_price = Bidder.objects.filter(item=auction.id).aggregate(Max('price'))
                if b_price['price__max'] is None:
                    auction.state_id = 3
                    auction.save()
                    send_mail("Bid due", 'Your bid has been closed! No one had bid on your item!','eyob@eyob',
                              [auction.owner.email])
                else:
                    bidders = Bidder.objects.filter(item=auction.id)
                    bid_winner = Bidder.objects.filter(item=auction.id).get(price=Decimal(b_price['price__max']))
                    winner = bid_winner.bidder_name
                    for bidder in bidders:
                        recipient = bidder.bidder_name.email
                        send_mail("Bid closed", 'The winner of the auction is '+winner.username+' Thanks!','eyob@eyob',
                              [recipient])
                        auction.state_id = 4
                        auction.save()