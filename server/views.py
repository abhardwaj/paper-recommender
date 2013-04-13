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

def init_session(email):
	pass

def login_form(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def login(request, redirect_url='/mobile'):
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
	return HttpResponseRedirect('/login')


def mobile(request):
	recs = []
	starred = {}
	try:
		user = request.session['id']
		if(user in p.author_likes):
			starred = {s:True for s in p.author_likes[user]['likes']}
			recs = r.get_item_based_recommendations(starred)		
	except KeyError:
		return HttpResponseRedirect('login')
	except:
		pass
	return render_to_response("mobile.html", 
		{
		'login_id': request.session['id'], 
		'login_name': request.session['name'],
		'recs':json.dumps(recs), 
		'starred':json.dumps(starred), 
		'entities': json.dumps(e.entities), 
		'sessions':json.dumps(s.sessions)
		})

def desktop(request):
	recs = []
	try:
		user = request.session['id']
		if(user in p.author_likes):
			papers_liked = p.author_likes[user]['likes']
			recs = r.get_item_based_recommendations(papers_liked)		
	except KeyError:
		return HttpResponseRedirect('login')
	except:
		pass
	return render_to_response("desktop.html", 
		{
		'login_id': request.session['id'], 
		'login_name': request.session['name'],
		'recs':json.dumps(recs), 
		'prefs':json.dumps(p.author_likes), 
		'entities': json.dumps(e.entities), 
		'sessions':json.dumps(s.sessions)
		})

@csrf_exempt
def get_recs(request):
	papers = json.loads(request.POST["papers"])
	recs = r.get_item_based_recommendations(papers)
	return HttpResponse(json.dumps(recs), mimetype="application/json")



def like(request, paper_id, like_str):
	if(paper_id.strip() == ''):
		return HttpResponse(json.dumps({'status':'notok'}), mimetype="application/json")
	user = request.session['id']
	if(user not in p.author_likes):
		p.author_likes[user] = {}
		p.author_likes[user]['likes'] = []
	if(like_str=='like' and (paper_id not in p.author_likes[user]['likes'])):
		p.author_likes[user]['likes'].append(paper_id)
		recs = r.get_item_based_recommendations(p.author_likes[user]['likes'])
		return HttpResponse(json.dumps({'status':'ok', 'recs':recs}), mimetype="application/json")
	if(like_str=='unlike' and paper_id in p.author_likes[user]['likes']):
		p.author_likes[user]['likes'].remove(paper_id)
		recs = r.get_item_based_recommendations(p.author_likes[user]['likes'])
		return HttpResponse(json.dumps({'status':'ok', 'recs':recs}), mimetype="application/json")
	return HttpResponse(json.dumps({'status':'notok'}), mimetype="application/json")



