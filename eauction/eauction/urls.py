from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^auctions/$', 'Yaas.views.index', name='home'),
    url(r'^item/(?P<e_id>\d+)/$', 'Yaas.views.item', name='home'),
    url(r'^register/$', 'Yaas.views.register', name='register'),
    url(r'^accounts/login/$', 'Yaas.views.login', name='login'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change',{'post_change_redirect': '/done/', 'template_name':'change_password.html'} ,name='edit'),
    url(r'^done/$', 'django.contrib.auth.views.password_change_done',{'template_name':'password_changed.html'}  ,name='done'),
    url(r'^edit_profile/$', 'Yaas.views.edit_profile', name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/../auctions/'}, name='logout'),
    url(r'^new_auction/$', 'Yaas.views.new_auction', name='new'),
    url(r'^new_category/$', 'Yaas.views.new_category', name='new_cat'),
    url(r'^search_results/$', 'Yaas.views.search', name='search'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
