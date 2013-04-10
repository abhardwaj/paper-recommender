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
			login_email = request.POST["login_email"]

			if(login_email != ""):
				request.session.flush()
				cursor = connection.cursor()
				cursor.execute("""SELECT id, given_name, family_name from pcs_authors where email1 like '%s' or 
					email2 like '%s' or email3 like '%s';""" %(login_email, login_email, login_email))
				data = cursor.fetchall()
				request.session['id'] = data[0][0]
				request.session['email'] = login_email
				request.session['name'] = data[0][1] + ' ' + data[0][2]
				return HttpResponseRedirect(redirect_url)
			else:
				return login_form(request)
		except:
			print sys.exc_info()
			return login_form(request)
	else:
		return login_form(request)
		


def logout(request):
	request.session.flush()
	return HttpResponseRedirect('index')



def index(request):
	try:
		user = request.session['id']
		recs = []
		likes = []
		if(user in p.author_likes):
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
		return render_to_response("index.html", {'login': request.session['name'], 'recs':recs, 'user_likes':likes})
	except KeyError:
		print sys.exc_info()
		return HttpResponseRedirect('login')


def users(request):	
	user = request.session['id']
	users = []
	for u in p.author_likes:
		users.append({'id':u, 'name': p.author_likes[u]['name']})
	return render_to_response("users.html", {'login': request.session['name'], 'users':users})


def user(request, author_id):
	try:
		user = author_id
		login = request.session['id']
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
		return render_to_response("user.html", {'login': request.session['name'], 'user': p.author_likes[user]['name'], 'recs':recs, 'user_likes':likes, 'likes':p.author_likes[login]['likes']})
	except KeyError:
		return HttpResponseRedirect('login')	



def paper(request, paper_id):	
	items = r.get_item_based_recommendations([paper_id])
	user = request.session['id']
	recs = []
	paper = e.entities[paper_id]
	for item in items:
		rec = {}
		id = item['id']
		rec['id']=id
		rec.update(e.entities[id])
		recs.append(rec)
	return render_to_response("paper.html", {'login': request.session['name'], 'id':paper_id, 'paper': paper, 'recs':recs, 'likes':p.author_likes[user]['likes']})



def like(request, paper_id, like_str):	
	user = request.session['id']
	if(like_str=='like' and (paper_id not in p.author_likes[user]['likes'])):
		p.author_likes[user]['likes'].append(paper_id)
		return HttpResponse(json.dumps({'status':'ok'}), mimetype="application/json")
	if(like_str=='unlike' and paper_id in p.author_likes[user]['likes']):
		p.author_likes[user]['likes'].remove(paper_id)
		return HttpResponse(json.dumps({'status':'ok'}), mimetype="application/json")
	return HttpResponse(json.dumps({'status':'notok'}), mimetype="application/json")



def schedule(request):	
	user = request.session['id']
	sessions = s.sessions
	for session in sessions:
		for submission in sessions[session]['submissions']:
			sessions[session]['submissions'][submission].update(e.entities[submission])
	return render_to_response("schedule.html", {'login': request.session['name'], 'sessions':sessions, 'likes':p.author_likes[user]['likes']})

