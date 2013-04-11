from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.index'),
	url(r'^index', 'server.views.index'),
	url(r'^users', 'server.views.users'),
	url(r'^papers', 'server.views.papers'),
	url(r'^schedule', 'server.views.schedule'),
    url(r'^user/(\w+)$', 'server.views.user'),
    url(r'^paper/(\w+)$', 'server.views.paper'),
    url(r'^like/(\w+)/(\w+)$', 'server.views.like'),


    url(r'^login', 'server.views.login'),
	url(r'^logout', 'server.views.logout'),
)
