from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.desktop'),
	url(r'^index', 'server.views.desktop'),
	url(r'^schedule', 'server.views.schedule'),
	url(r'^mobile', 'server.views.mobile'),
    url(r'^paper/(\w+)$', 'server.views.paper'),
    url(r'^like/(\w+)/(\w+)$', 'server.views.like'),


    url(r'^login', 'server.views.login'),
	url(r'^logout', 'server.views.logout'),
)
