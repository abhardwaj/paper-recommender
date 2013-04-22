import json, sys, re, hashlib, smtplib, base64, urllib


from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from algorithm.recommend import *
from db.prefs import *
from db.entity import *
from db.session import *
from db.authors import *

p = os.path.abspath(os.path.dirname(__file__))
if(os.path.abspath(p+"/..") not in sys.path):
	sys.path.append(os.path.abspath(p+"/.."))


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''



r = Recommender()
e = Entity()
p = Prefs()
s = Session()

codes = open('/production/paper-recommender/data/letterCodes.json').read()


def send_email(addr, id):	
	email_subject = "Welcome to myCHI"
	from_addr="mychi@csail.mit.edu"
	to_addr = [addr]

	msg_body = """
	Dear %s,

	Thanks for registering! Please click the link below to start using myCHI:

	http://mychi.csail.mit.edu/verify/%s

	""" %(addr, id)
	
	msg = MIMEMultipart()
	msg['From'] = 'myCHI'
	msg['To'] = ",".join(to_addr)
	msg['Subject'] = email_subject
	msg.attach(MIMEText(msg_body))	
	
	
	username = 'anantb'
	password = 'JcAt250486'
	smtp_conn = smtplib.SMTP_SSL('cs.stanford.edu', 465)
	#smtp_conn.ehlo()
	#smtp_conn.starttls()
	#smtp_conn.ehlo()
	smtp_conn.login(username, password)	
	#smtp_conn.set_debuglevel(True)	
	smtp_conn.sendmail(from_addr, to_addr, msg.as_string())
	smtp_conn.close() 



@csrf_exempt
def email(request, login_email):
	send_email(base64.b64decode(login_email), login_email)
	return HttpResponse(json.dumps({'status':'ok'}),  mimetype="application/json")


def init_session(email):
	pass

def login_form(request, error=None):
	c = {}
	if(error != None):
		c.update(error)
	c.update(csrf(request))
	return render_to_response('desktop/login.html', c)



def login(request):
	if request.method == "POST":
		try:
			login_email = request.POST["login_email"]
			login_password = request.POST["login_password"].strip()
			if(login_email != ""):
				request.session.flush()
				cursor = connection.cursor()
				cursor.execute("""SELECT id, given_name, family_name, password, verified from pcs_authors where email1 like '%s' or 
					email2 like '%s' or email3 like '%s';""" %(login_email, login_email, login_email))
				data = cursor.fetchall()
				if(len(data) == 0):
					return login_form(request, error = { 'login_email':urllib.quote(base64.b64encode(login_email)), 'type': 'info', 'error': 'We have sent you a verification email. Please check your mailbox.'})
				password = hashlib.sha1(login_password).hexdigest()
				if(data[0][3]== None):
					cursor.execute("""UPDATE pcs_authors SET password = '%s' where id = '%s';""" %(password, data[0][0]))
				else:
					if(data[0][3]!=password):
						return login_form(request, error = {'type': 'error', 'error': 'Wrong password'})
				
				request.session['id'] = data[0][0]
				request.session['email'] = login_email
				if(data[0][1] != None ):
					request.session['name'] = data[0][1]
				else:
					request.session['name'] = login_email[0:login_email.index('@')]
				return HttpResponseRedirect('/home')
			else:
				return login_form(request, error = {'type': 'error', 'error': 'Enter an email address.'})
		except:
			print sys.exc_info()
			return login_form(request, error = {'type':'error', 'error': 'Something went wrong. We will look into it.'})
			return login_form(request)
	else:
		return login_form(request)


@csrf_exempt
def verify(request, addr):
	login_email = base64.b64decode(addr)
	cursor = connection.cursor()
	cursor.execute("""SELECT id from pcs_authors where email1 like '%s' or 
					email2 like '%s' or email3 like '%s';""" %(login_email, login_email, login_email))
	data = cursor.fetchall()
	if(len(data) == 0):
		cursor.execute("""INSERT into pcs_authors (id, email1) values('%s', '%s');""" %(addr, login_email))
	
	return login_form(request)
		


def logout(request):
	request.session.flush()
	return HttpResponseRedirect('/login')



def home(request):
	try:
		return render_to_response('desktop/main.html', 
		{'login_id': request.session['id'], 
		'login_name': request.session['name']})	
	except KeyError:
		return HttpResponseRedirect('/login')
	except:
		pass
	


def schedule(request):
	recs = []
	starred = {}
	try:
		return render_to_response('desktop/schedule.html', 
		{'login_id': request.session['id'], 
		'login_name': request.session['name']})		
	except KeyError:
		return HttpResponseRedirect('/login')
	except:
		pass
	

def paper(request):
	try:
		return render_to_response('desktop/paper.html', 
		{'login_id': request.session['id'], 
		'login_name': request.session['name']})
	except KeyError:
		return HttpResponseRedirect('/login')
	except:
		pass


@csrf_exempt
def data(request):
	user = request.session['id']
	recs = []
	starred = {}
	if(user in p.author_likes):
		starred = {s:True for s in p.author_likes[user]['likes']}
		recs = r.get_item_based_recommendations(starred)
	return HttpResponse(json.dumps({
		'login_id': request.session['id'], 
		'login_name': request.session['name'],
		'recs':recs, 
		'starred':starred, 
		'entities': e.entities, 
		'sessions':s.sessions,
		'codes': codes
		}), mimetype="application/json")

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




