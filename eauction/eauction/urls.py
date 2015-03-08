from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from Yaas import api
from Yaas.api import BidAuctionView
from rest_framework.urlpatterns import format_suffix_patterns
from django.utils.translation import ugettext_lazy as _
from rest_framework import renderers




urlpatterns = patterns('',
    # URLs:
    url(r'^auctions/$', 'Yaas.views.index', name='home'),
    url(r'^item/(?P<e_id>\d+)/$', 'Yaas.views.item', name='home'),
    url(r'^edit_auction/(?P<e_id>\d+)/$', 'Yaas.views.edit_auction', name='home'),
    url(r'^register/$', 'Yaas.views.register', name='register'),
    url(r'^accounts/login/$', 'Yaas.views.login', name='login'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change',{'post_change_redirect': '/done/',
                                                                            'template_name':'change_password.html'} ,name='edit'),
    url(r'^done/$', 'django.contrib.auth.views.password_change_done',{'template_name':'password_changed.html'}, name='done'),
    url(r'^edit_profile/$', 'Yaas.views.edit_profile', name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/../auctions/'}, name='logout'),
    url(r'^new_auction/$', 'Yaas.views.new_auction', name='new'),
    url(r'^new_category/$', 'Yaas.views.new_category', name='new_cat'),
    url(r'^search_results/$', 'Yaas.views.search', name='search'),
    url(r'^my_profile/$', 'Yaas.views.search', name='My profile'),
    url(r'^confirm/$', 'Yaas.views.confirm', name='confirm'),
    url(r'^bid_api/$', 'Yaas.views.bid_auction', name='bid'), #WS2
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #API
    url(r'^api/auction_list/$', api.AuctionList.as_view()), #WS1
    url(r'^api/auction_list/(?P<pk>\d+)/$', api.AuctionDetail.as_view()), #WS1
    url(r'^api/bidders/$', api.BidAuctionView.as_view({'get': 'list','post': 'create'})),
    url(r'^api/bid_auction/$', api.BidFilter.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns= format_suffix_patterns(urlpatterns)