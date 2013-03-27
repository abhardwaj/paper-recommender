import json, sys, re


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from algorithm.recommend import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


r = Recommender()



SESSION_KEY = 'USER'

def init_session(email):
	pass

def login_form(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def login(request, redirect_url='index'):
	if request.method == "POST":
		try:
			user = request.POST["login_author"]
			if(user != ""):
				request.session.flush()
				request.session[SESSION_KEY] = user
				return HttpResponseRedirect(redirect_url)
			else:
				return login_form(request)
		except:
			return login_form(request)
	else:
		return login_form(request)
		


def logout(request):
	request.session.flush()
	return HttpResponseRedirect('index')



def index(request):
	try:
		user = request.session[SESSION_KEY]
		return render_to_response("index.html", {'user': r.prefs.author_likes[user]})
	except KeyError:
		return HttpResponseRedirect('login')


	
def similar_papers(request, paper_id):	
	res = r.get_item_based_recommendations(paper_id)
	user = request.session[SESSION_KEY]
	return render_to_response("paper.html", {'data': res, 'p_id':paper_id, 'user': r.prefs.author_likes[user] , 'u':user} )



