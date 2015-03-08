from django.test import TestCase, Client
from django.contrib.auth.models import User
from Yaas.models import *
from Yaas.forms import AuctionForm
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import reverse

# Create your tests here.


class CreateAuctionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('jordan','jordan@jordan.com', 'jordan')
        Auction.objects.create(auction_name='laptop',auction_description='Brand new Toshiba computer',
                               price_min=199.99, end_date=(datetime.today()+timedelta(hours=73)),category_id=1,state_id=1,owner_id=2)

    def auction_created_test(self):
        laptop = Auction.objects.get(auction_name='laptop')
        self.assertEqual(laptop.auction_description, 'Brand new Toshiba computer')
        self.assertEqual(laptop.auction_name, 'laptop')

    #With valid input
    def create_auction_test_working(self):
        client = Client(enforce_csrf_checks=True)
        self.client.login(username='jordan', password='jordan')
        value = {'auction_name': 'laptop','auction_description': 'Brand new Toshiba computer',
                 'price_min': 199.99,'end_date': '2014-11-08 14:55:08','category': 1, 'create': True}
        self.client.post('/new_auction/', value)
        response = self.client.post('/new_auction/', {'confirm': True})
        #If auction created, it will be redirected to index.html
        self.assertTemplateUsed(response, 'index.html')


    #With wrong input e.g. end_date less than 72h from now.
    def create_auction_test_fail(self):
        client = Client(enforce_csrf_checks=True)
        self.client.login(username='jordan', password='jordan')
        value = {'auction_name': 'laptop','auction_description': 'Brand new Toshiba computer',
                 'price_min': 199.99,'end_date': '2014-10-29 14:55:08','category': 1, 'create': True}
        self.client.post('/new_auction/', value)
        response = self.client.post('/new_auction/', {'confirm': True})
        #If auction was successfully created, it will be redirected to index.html
        self.assertTemplateUsed(response, 'index.html')

    def bid_an_auction(self):
        client = Client(enforce_csrf_checks=True)
        self.client.login(username='jordan', password='jordan')
        value = {'price': 200}
        self.client.post('/item/55/', value)
        response = self.client.post('/item/55/', {'submit':True})
        self.assertEqual(response.status_code, 201)


    def auction_concurrency_test(self):
        laptop = Auction.objects.get(auction_name='laptop')
        self.pk = laptop.pk
        laptop1 = Auction.objects.get(auction_name='laptop')
        laptop.auction_name = 'computer'
        laptop1.auction_name = 'something'
        laptop.save()
        self.assertRaises(self, ConcurrentModificationError, laptop1.save())
