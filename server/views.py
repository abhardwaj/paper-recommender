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

def login_form(request, req_url= 'desktop'):
	c = {}
	c.update(csrf(request))
	return render_to_response(req_url + '/login.html', c)

def login(request, req_url='desktop'):
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
				return HttpResponseRedirect('/' + req_url)
			else:
				return login_form(request, req_url)
		except:
			print sys.exc_info()
			return login_form(request, req_url)
	else:
		return login_form(request, req_url)
		


def logout(request, req_url='desktop'):
	request.session.flush()
	return HttpResponseRedirect('/'+req_url)






def main(request, req_url='desktop'):
	recs = []
	starred = {}
	try:
		user = request.session['id']
		if(user in p.author_likes):
			starred = {s:True for s in p.author_likes[user]['likes']}
			recs = r.get_item_based_recommendations(starred)		
	except KeyError:
		return HttpResponseRedirect(req_url+'/login')
	except:
		pass
	return render_to_response(req_url + "/main.html", 
		{
		'login_id': request.session['id'], 
		'login_name': request.session['name'],
		'recs':json.dumps(recs), 
		'starred':json.dumps(starred), 
		'entities': json.dumps(e.entities), 
		'sessions':json.dumps(s.sessions)
		})

@csrf_exempt
def get_recs(request):
	papers = json.loads(request.POST["papers"])
	recs = r.get_item_based_recommendations(papers)
	return HttpResponse(json.dumps(recs), mimetype="application/json")


@csrf_exempt
def like(request, like_str):
	papers = json.loads(request.POST["papers"])
	user = request.session['id']
	res = {}
	if(user not in p.author_likes):
		p.author_likes[user] = {}
		p.author_likes[user]['likes'] = []
	for paper_id in papers:
		if(like_str=='star' and (paper_id not in p.author_likes[user]['likes']) and paper_id != ''):
			p.author_likes[user]['likes'].append(paper_id)
		if(like_str=='unstar' and (paper_id in p.author_likes[user]['likes']) and paper_id != ''):
			p.author_likes[user]['likes'].remove(paper_id)
		if(paper_id in p.author_likes[user]['likes']):
			res[paper_id] = 'star'
		else:
			res[paper_id] = 'unstar'
	recs = r.get_item_based_recommendations(p.author_likes[user]['likes'])
	return HttpResponse(json.dumps({'recs':recs, 'likes':p.author_likes[user], 'res':res}), mimetype="application/json")



