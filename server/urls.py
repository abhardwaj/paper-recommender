from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.home'),
	url(r'^home$', 'server.views.home'),
	url(r'^schedule$', 'server.views.schedule'),
	url(r'^paper', 'server.views.paper'),
	
	url(r'^data', 'server.views.data'),
	url(r'^manifest$', 'server.views.manifest'),
    url(r'^recs', 'server.views.get_recs'),
    url(r'^like/(\w+)$', 'server.views.like'),

    url(r'^login', 'server.views.login'),

    url(r'^logout', 'server.views.logout'),
)
