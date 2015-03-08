__author__ = 'eyob'
from rest_framework import serializers
from Yaas.models import Auction, AuctionCategory, Bidder, AuctionState
from datetime import datetime
from decimal import Decimal
from django.db.models import Max


class BidSerializer(serializers.ModelSerializer):
    #bidder_name = serializers.Field(source='bidder_name')

    class Meta:
        model = Bidder
        fields = ( 'price', 'item')
        read_only_fields = ['bidder_name']

    def validate_bidder_name(self, attrs, source):
        bidder = attrs
        product = attrs.get('item')
        b_price =Bidder.objects.filter(item=product.id).aggregate(Max('price'))
        if bidder == product.owner:
            raise serializers.ValidationError('You cannot bid on your own item')
        if b_price['price__max'] is not None:
            current_bid = Bidder.objects.filter(item=product.id).get(price=Decimal(b_price['price__max']))
            if current_bid.bidder_name.id == bidder.id:
                raise serializers.ValidationError('You cannot bid while you are winning')
        return attrs

    def validate_price(self, attrs, source):
        price = attrs[source]
        product = attrs.get('item')
        bidder = attrs.get('bidder_name')
        b_price =Bidder.objects.filter(item=product.id).aggregate(Max('price'))
        if b_price['price__max'] is None:
            if price <= product.price_min:
                raise serializers.ValidationError("You cannot bid with less price than the initial price")
        elif b_price['price__max'] >= price:
            raise serializers.ValidationError("You cannot bid with less price than the winning price")
        return attrs

    def validate_item(self, attrs, source):
        value = attrs[source]
        if value.end_date < datetime.now() and value.state is not 1:
            raise serializers.ValidationError("You cannot bid on due or banned auction")
        return attrs





class AuctionSerializer(serializers.ModelSerializer):
    bidders = serializers.RelatedField(many=True)


    class Meta:
        model = Auction
        fields = ('id','auction_name', 'auction_description', 'price_min','bidders', 'start_date',
                  'end_date', 'category',  'state','owner')




