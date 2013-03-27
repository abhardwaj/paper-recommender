import json, sys, re


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from algorithm.recommend_simple import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


f = open('data/data_simple.txt')
data = json.loads(f.read())
similar_items = get_similar_items(data)


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
			user = request.POST["email"]
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
		return render_to_response("index.html", {'user': user})
	except KeyError:
		return HttpResponseRedirect('login')


	
def similar_papers(request, paper_id):	
	res = get_item_based_recommendations(paper_id, data, similar_items)
	return render_to_response("paper.html", {'data': res})

@csrf_exempt	
def recommend(request):
	if(request.POST):
		res = get_item_based_recommendations(request.POST['person'], data, similar_items)
		return HttpResponse(json.dumps(res), mimetype="application/json")
	else:
		return HttpResponse("invalid request type")


