from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.desktop'),
	url(r'^desktop', 'server.views.desktop'),
	url(r'^mobile', 'server.views.mobile'),
    

    url(r'^recs', 'server.views.get_recs'),
    url(r'^like/(\w+)/(\w+)$', 'server.views.like'),


    url(r'^login', 'server.views.login'),
	url(r'^logout', 'server.views.logout'),
)
