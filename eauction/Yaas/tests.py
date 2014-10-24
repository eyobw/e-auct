from django.test import TestCase
from Yaas.models import Auction
from datetime import datetime, timedelta

# Create your tests here.


class CreateAuctionTests(TestCase):

    def setUp(self):
        Auction.objects.create(auction_name='laptop',auction_description='Brand new Toshiba computer',
                               price_min=199.99, end_date=(datetime.today()+timedelta(hours=73)),category_id=1,state_id=1,owner_id=2)

    def auction_created_test(self):
        laptop = Auction.objects.get(auction_name='laptop')
        self.assertEqual(laptop.auction_description, 'Brand new Toshiba computer')
        self.assertEqual(laptop.auction_name, 'lapt')