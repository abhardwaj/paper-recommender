from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','recommender.views.index'),
	url(r'^index', 'recommender.views.index'),
    url(r'^recommend', 'recommender.views.recommend'),
    url(r'^paper/(\w+)$', 'recommender.views.similar_papers'),

    url(r'^login', 'recommender.views.login'),
	url(r'^logout', 'recommender.views.logout'),
)
