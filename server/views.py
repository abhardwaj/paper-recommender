import json, sys, re


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from algorithm.recommend import *
from db.prefs import *
from db.entity import *
from db.session import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


r = Recommender()
e = Entity()
p = Prefs()
s = Session()



SESSION_KEY = 'USER'

def init_session(email):
	pass

def login_form(request):
	c = {}
	c.update(csrf(request))
	users = {}
	for k in p.author_likes.keys():
		users[p.author_likes[k]['name']] = k

	c.update({'users': json.dumps(users)})
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
			rec.update(e.entities[id])
			recs.append(rec)
		for like in papers_liked:
			l = {}
			id=like
			l['id']=id
			l.update(e.entities[id])
			likes.append(l)
		#print recs
		return render_to_response("index.html", {'login': p.author_likes[user]['name'], 'recs':recs, 'likes':likes})
	except KeyError:
		return HttpResponseRedirect('login')


def users(request):	
	user = request.session[SESSION_KEY]
	users = []
	for u in p.author_likes:
		users.append({'id':u, 'name': p.author_likes[u]['name']})
	return render_to_response("users.html", {'login': p.author_likes[user]['name'], 'users':users})


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
			rec.update(e.entities[id])
			recs.append(rec)
		for like in papers_liked:
			l = {}
			id=like
			l['id']=id
			l.update(e.entities[id])
			likes.append(l)
		#print recs
		return render_to_response("user.html", {'login': p.author_likes[login]['name'], 'user': p.author_likes[user]['name'], 'recs':recs, 'likes':likes})
	except KeyError:
		return HttpResponseRedirect('login')	



def paper(request, paper_id):	
	items = r.get_item_based_recommendations([paper_id])
	user = request.session[SESSION_KEY]
	recs = []
	paper = e.entities[paper_id]
	for item in items:
		rec = {}
		id = item['id']
		rec['id']=id
		rec.update(e.entities[id])
		recs.append(rec)
	return render_to_response("paper.html", {'login': p.author_likes[user]['name'], 'id':paper_id, 'paper': paper, 'recs':recs})



def schedule(request):	
	user = request.session[SESSION_KEY]
	sessions = s.sessions
	for session in sessions:
		for submission in sessions[session]['submissions']:
			sessions[session]['submissions'][submission].update(e.entities[submission])
	return render_to_response("schedule.html", {'login': p.author_likes[user]['name'], 'sessions':sessions})

