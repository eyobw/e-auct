from django.contrib import admin
from Yaas.models import Auction,AuctionCategory,AuctionState,Bidder

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('auction_name','owner')


class State(admin.ModelAdmin):
    list_display = ['state_name']

admin.site.register(AuctionCategory)
admin.site.register(AuctionState, State)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bidder)