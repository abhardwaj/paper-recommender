from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.index'),
	url(r'^index', 'server.views.index'),
    url(r'^recommend', 'server.views.recommend'),
    url(r'^paper/(\w+)$', 'server.views.similar_papers'),

    url(r'^login', 'server.views.login'),
	url(r'^logout', 'server.views.logout'),
)
