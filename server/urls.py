from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.home'),
	url(r'^home$', 'server.views.home'),
	url(r'^schedule$', 'server.views.schedule'),
	url(r'^paper', 'server.views.paper'),

	
	url(r'^data', 'server.views.data'),
    url(r'^refresh', 'server.views.refresh'),
    url(r'^recs', 'server.views.get_recs'),
    url(r'^like/(\w+)$', 'server.views.like'),
    url(r'^s_like/(\w+)$', 'server.views.s_like'),

    url(r'^login', 'server.views.login'),
    url(r'^verify/(.+)$', 'server.views.verify'),
    url(r'^reset/(.+)$', 'server.views.reset'),
    url(r'^verify_email/(.+)$', 'server.views.verify_email'),
    url(r'^reset_email/(.+)$', 'server.views.reset_email'),

    url(r'^logout', 'server.views.logout'),
    url(r'^error', 'server.views.error'),
)
