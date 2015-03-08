__author__ = 'eyob'
from .models import Auction, Bidder
from .serializers import AuctionSerializer, BidSerializer
from django.http import HttpResponse
from datetime import datetime
import django_filters
from django.http import Http404
from rest_framework import status, serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONPRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONPRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class AuctionList(APIView):

    def get(self, request, format=None):
        auction = Auction.objects.filter(end_date__gt=datetime.now()).filter(state_id=1)
        serializer = AuctionSerializer(auction, many=True)
        return Response(serializer.data)

class AuctionDetail(APIView):

    def get_auction(self, pk):
        try:
            return Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return HttpResponse(status=404)

    def get(self, request, pk, format=None):
        auction = self.get_auction(pk)
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)

class BidFilter(APIView):

    def post(self, request, format=None):
        serializer = BidSerializer(request.DATA)
        return Response(serializer.data)


class BidAuctionView(viewsets.ModelViewSet,):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer
    queryset = Bidder.objects.filter(item__state=1)



   # def pre_save(self, obj):
       # obj.bidder_name = self.request.user



class BidAuction(ListCreateAPIView):
    model = Bidder.objects.filter(item__end_date__gt=datetime.now())
    serializer_class = BidSerializer