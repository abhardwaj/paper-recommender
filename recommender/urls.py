from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','recommender.views.index'),
	url(r'^index', 'recommender.views.index'),
    url(r'^recommend', 'recommender.views.recommend'),
)
