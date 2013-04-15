from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.main', {'req_url': 'desktop'}),
	url(r'^desktop$', 'server.views.main', {'req_url': 'desktop'}),
	url(r'^mobile$', 'server.views.main', {'req_url': 'mobile'}),    

    url(r'^recs', 'server.views.get_recs'),
    url(r'^like/(\w+)/(\w+)$', 'server.views.like'),

    url(r'^desktop/login', 'server.views.login',{'req_url': 'desktop'}),
    url(r'^mobile/login', 'server.views.login',{'req_url': 'mobile'}),

    url(r'^desktop/logout', 'server.views.logout', {'req_url': 'desktop'}),
    url(r'^mobile/logout', 'server.views.logout', {'req_url': 'mobile'}),
)
