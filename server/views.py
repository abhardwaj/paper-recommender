import json, sys, re


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from algorithm.recommend import *
from db.prefs import *
from db.entity import *
from db.session import *
from db.authors import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''


r = Recommender()
e = Entity()
p = Prefs()
s = Session()
#a = Authors()





def init_session(email):
	pass

def login_form(request):
	c = {}
	c.update(csrf(request))
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


def get_starred(request):
	starred = []
	try:
		login_user = request.session['id']	
		starred = p.author_likes[login_user]['likes']
	except:
		pass
	return starred


def index(request):
	try:
		user = request.session['id']
		recs = []
		likes = []
		if(user in p.author_likes):
			papers_liked = p.author_likes[user]['likes']
			papers_liked = filter(lambda x: x!='', papers_liked)
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
		return render_to_response("index.html", {'login': request.session['name'], 'recs':recs, 'likes':likes, 'papers': e.entities, 'starred':get_starred(request)})
	except KeyError:
		print sys.exc_info()
		return HttpResponseRedirect('login')




def papers(request):	
	return render_to_response("papers.html", {'login': request.session['name'], 'papers':e.entities, 'starred':get_starred(request)})




def paper(request, paper_id):
	items = r.get_item_based_recommendations([paper_id])
	recs = []
	paper = e.entities[paper_id]
	for item in items:
		rec = {}
		id = item['id']
		rec['id']=id
		rec.update(e.entities[id])
		recs.append(rec)
	return render_to_response("paper.html", {'login': request.session['name'], 'id':paper_id, 'paper': paper, 'recs':recs, 'starred':get_starred(request)})



def like(request, paper_id, like_str):	
	user = request.session['id']
	if(user not in p.author_likes):
		p.author_likes[user] = {}
		p.author_likes[user]['likes'] = []
	if(like_str=='like' and (paper_id not in p.author_likes[user]['likes'])):
		p.author_likes[user]['likes'].append(paper_id)
		return HttpResponse(json.dumps({'status':'ok'}), mimetype="application/json")
	if(like_str=='unlike' and paper_id in p.author_likes[user]['likes']):
		p.author_likes[user]['likes'].remove(paper_id)
		return HttpResponse(json.dumps({'status':'ok'}), mimetype="application/json")
	return HttpResponse(json.dumps({'status':'notok'}), mimetype="application/json")



def schedule(request):
	sessions = s.sessions
	for session in sessions:
		for submission in sessions[session]['submissions']:
			sessions[session].update({'timeslot': str(100/len(sessions[session]['submissions']))+'%'})
			sessions[session]['submissions'][submission].update(e.entities[submission])
	return render_to_response("schedule.html", {'login': request.session['name'], 'sessions':sessions, 'starred':get_starred(request)})

