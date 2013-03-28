import json, sys, re


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from algorithm.recommend import *
from db.prefs import *
from db.entity import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


r = Recommender()
e = Entity()
p = Prefs()



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
		recs = []
		likes = []
		papers_liked = p.author_likes[user]['likes']
		items = r.get_item_based_recommendations(papers_liked)
		for item in items:
			rec = {}
			id=item['id']
			rec['id']=id
			rec['title']= e.entities[id]['title']
			recs.append(rec)
		for like in papers_liked:
			l = {}
			id=like
			l['id']=id
			l['title']= e.entities[id]['title']
			likes.append(l)
		#print recs
		return render_to_response("index.html", {'login': user, 'recs':recs, 'likes':likes})
	except KeyError:
		return HttpResponseRedirect('login')


def user(request, author_id):
	try:
		user = author_id
		login = request.session[SESSION_KEY]
		recs = []
		likes = []
		papers_liked = p.author_likes[user]['likes']
		items = r.get_item_based_recommendations(papers_liked)
		for item in items:
			rec = {}
			id=item['id']
			rec['id']=id
			rec['title']= e.entities[id]['title']
			recs.append(rec)
		for like in papers_liked:
			l = {}
			id=like
			l['id']=id
			l['title']= e.entities[id]['title']
			likes.append(l)
		#print recs
		return render_to_response("user.html", {'login': login, 'user': user, 'recs':recs, 'likes':likes})
	except KeyError:
		return HttpResponseRedirect('login')	



def paper(request, paper_id):	
	items = r.get_item_based_recommendations([paper_id])
	user = request.session[SESSION_KEY]
	recs = []
	paper_title =e.entities[paper_id]['title']
	for item in items:
		rec = {}
		id = item['id']
		rec['id']=id
		rec['title']= e.entities[id]['title']
		recs.append(rec)
	return render_to_response("paper.html", {'login': user, 'id':paper_id, 'title': paper_title, 'recs':recs})



