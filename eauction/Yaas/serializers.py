__author__ = 'eyob'
from rest_framework import serializers
from Yaas.models import Auction, AuctionCategory, Bidder, AuctionState


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('auction_name', 'auction_description','price_min', 'start_date',
                  'end_date', 'category',  'state','owner')