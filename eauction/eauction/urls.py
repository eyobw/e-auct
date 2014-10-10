from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^auctions/$', 'Yaas.views.index', name='home'),
    url(r'^item/(?P<e_id>\d+)/$', 'Yaas.views.item', name='home'),
    url(r'^register/$', 'Yaas.views.register', name='register'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
