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
session_codes = open('/production/paper-recommender/data/sessionCodes.json').read()
offline_recs = open('/production/paper-recommender/data/offline_recs.txt').read()
acm_links = open('/production/paper-recommender/data/bib_final.txt').read()

bib_map = json.loads(acm_links)

def send_email(addr, subject, msg_body):	
	email_subject = subject
	from_addr="mychi@csail.mit.edu"
	to_addr = [addr, 'mychi@csail.mit.edu']
	
	msg = MIMEMultipart()
	msg['From'] = 'myCHI <mychi@csail.mit.edu>'
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
def verify_email(request, login_email):
	email_plain = base64.b64decode(login_email)
	subject = "Welcome to myCHI"
	email_encoded = login_email
	msg_body = """
	Dear %s,

	Thanks for registering! Please click the link below to start using myCHI:

	http://mychi.csail.mit.edu/verify/%s

	""" %(email_plain, email_encoded)
	send_email(email_plain, subject, msg_body)
	return HttpResponse(json.dumps({'status':'ok'}),  mimetype="application/json")


@csrf_exempt
def reset_email(request, login_email):
	email_plain = base64.b64decode(login_email)
	email_encoded = login_email
	subject = "myCHI password reset"
	msg_body = """
	Dear %s,

	Please click the link below to reset your myCHI password:

	http://mychi.csail.mit.edu/reset/%s

	""" %(email_plain, email_encoded)
	send_email(email_plain, subject, msg_body)
	return HttpResponse(json.dumps({'status':'ok'}),  mimetype="application/json")


def init_session(email):
	pass

def login_form(request, error=None):
	c = {}
	if(error != None):
		c.update(error)
	c.update(csrf(request))
	return render_to_response('desktop/login.html', c)


@csrf_exempt
def login(request):
	if request.method == "POST":
		try:
			login_email = request.POST["login_email"]
			login_password = request.POST["login_password"].strip()
			if(login_email != ""):
				login_email = login_email.strip()
				request.session.flush()
				cursor = connection.cursor()
				cursor.execute("""SELECT id, given_name, family_name, password, verified, auth_no from pcs_authors where email1 = '%s' or 
					email2 = '%s' or email3 = '%s';""" %(login_email, login_email, login_email))
				data = cursor.fetchall()
				if(len(data) == 0):
					return login_form(request, error = {'login_addr': login_email ,'login_email':urllib.quote(base64.b64encode(login_email)), 'type': 'info', 'verify':'yes', 'error': 'We have sent you a verification email. Please check your mailbox.'})

				password = hashlib.sha1(login_password).hexdigest()
				if(data[0][3]== None):
					cursor.execute("""UPDATE pcs_authors SET password = '%s' where id = '%s';""" %(password, data[0][0]))
				else:
					if(data[0][3]!=password):
						return login_form(request, error = {'login_addr': login_email, 'login_email':urllib.quote(base64.b64encode(login_email)), 'type': 'error', 'error': 'Wrong password.', 'wrong_password':True})
				
				request.session['id'] = data[0][0]
				request.session['auth_no'] = data[0][5]
				request.session['email'] = login_email
				if(data[0][1] != None ):
					request.session['name'] = data[0][1]
				else:
					request.session['name'] = login_email[0:login_email.index('@')]

				return HttpResponseRedirect('/home')
			else:
				return login_form(request, error = {'type': 'error', 'error': 'Enter an email address.'})
		except:
			return HttpResponseRedirect('/error')

	else:
		return login_form(request)



def error(request):
	return render_to_response('desktop/error.html')


@csrf_exempt
def verify(request, addr):
	login_email = base64.b64decode(addr)
	cursor = connection.cursor()
	cursor.execute("""SELECT id from pcs_authors where email1 like '%s' or 
					email2 like '%s' or email3 like '%s';""" %(login_email, login_email, login_email))
	data = cursor.fetchall()
	if(len(data) == 0):
		cursor.execute("""INSERT into pcs_authors (id, email1) values('%s', '%s');""" %(addr, login_email))
	
	return login_form(request, error = {'login_email':urllib.quote(base64.b64encode(login_email)), 'type': 'info', 'error': 'Thanks for verifying. Please enter your email and password.'})



@csrf_exempt
def reset(request, addr):
	login_email = base64.b64decode(addr)
	cursor = connection.cursor()
	cursor.execute("""UPDATE pcs_authors SET password = null where email1 like '%s' or 
					email2 like '%s' or email3 like '%s';""" %(login_email, login_email, login_email))	
	return login_form(request, error = {'login_email':urllib.quote(base64.b64encode(login_email)), 'type': 'info', 'error': 'Please enter a new password.'})
		


def logout(request):
	request.session.flush()
	return HttpResponseRedirect('/login')



def home(request):
	return render_to_response('desktop/main.html')
	
	


def schedule(request):
	return render_to_response('desktop/schedule.html')
	


def participate(request, val):
	try:
		user = request.session['id']
		if(val =='add'):
			return HttpResponse('We have added your name to the list of partipants for Meet experiment. To remove your name, you can click on <a href="/participate/remove">this link</a>', mimetype="text/html")	
		else:
			return HttpResponse('We have removed your name from the list of partipants for Meet experiment. To add your name again, you can click on <a href="/participate/add">this link</a>', mimetype="text/html")
	except KeyError:
		return HttpResponseRedirect('/login')


def meet(request):
	try:
		return render_to_response('desktop/meet.html', 
		{'login_id': request.session['id'], 
		'login_name': request.session['name']})		
	except KeyError:
		return HttpResponseRedirect('/login')
	except:
		return HttpResponseRedirect('/error')
	

def paper(request):
	try:
		return render_to_response('desktop/paper.html', 
		{'login_id': request.session['id'], 
		'login_name': request.session['name']})
	except KeyError:
		return HttpResponseRedirect('/login')
	except:
		return HttpResponseRedirect('/error')


def bib(request):
	try:
		user = request.session['id']
		cursor = connection.cursor()
		cursor.execute("""SELECT likes from pcs_authors where id = '%s';""" %(user))
		data = cursor.fetchall()
		likes = []
		bib_text = ''
		if(data[0][0] != None):
			likes = json.loads(data[0][0])
		for like in likes:
			if(like in bib_map.keys()):
				bib_text = bib_text + bib_map[like]['bib'] + '\n\n'
		return HttpResponse(bib_text, mimetype="text/plain")
		
	except:
		print sys.exc_info()
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")


@csrf_exempt
def data(request):
	try:
		user = request.session['id']
		recs = []
		own_papers = []
		s_likes = []
		likes = []
		cursor = connection.cursor()
		cursor.execute("""SELECT likes, s_likes from pcs_authors where id = '%s';""" %(user))
		data = cursor.fetchall()
		if(data[0][0] != None):
			likes.extend(json.loads(data[0][0]))
		if(data[0][1] != None):
			s_likes.extend(json.loads(data[0][1]))
		if(user in p.author_likes):
			if((data[0][0] == None) and ('likes' in p.author_likes[user].keys())):
				likes.extend(p.author_likes[user]['likes'])
			if('own_papers' in p.author_likes[user].keys()):
				own_papers = p.author_likes[user]['own_papers']
				likes.extend(p.author_likes[user]['own_papers'])
		if(data[0][0] == None):
			l = list(set(likes))
			cursor.execute("""UPDATE pcs_authors SET likes = '%s' where id = '%s';""" %(json.dumps(l), user))
		if(len(likes)>0):
			recs = r.get_item_based_recommendations(likes)
		user_recs =  get_similar_people(request)
		return HttpResponse(json.dumps({
			'login_id': request.session['id'], 
			'login_name': request.session['name'],
			'recs':recs, 
			'likes':likes, 
			's_likes':s_likes,
			'own_papers':own_papers,
			'entities': e.entities, 
			'sessions':s.sessions,
			'codes': codes,
			'offline_recs': offline_recs,
	    	'session_codes': session_codes,
	    	'acm_links' : acm_links,
	    	'user_recs': user_recs
			}), mimetype="application/json")
	except:
		print sys.exc_info()
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")




def get_similar_people(request):
	user_recs=[]
	try:
		cursor = connection.cursor()
		auth_no = request.session['auth_no']
		res = r.get_users_recommendations([str(auth_no)])		
		for rec in res:
			cursor.execute("""SELECT id, given_name, family_name, email1, dept1, instituition1, city1, country1 from pcs_authors where auth_no = %d;""" %(int(rec['id'])))
			data = cursor.fetchall()
			if(len(data)>0):
				user_recs.append({'id':data[0][0], 
					'given_name':data[0][1],
					'family_name':data[0][2],
					'email':data[0][3],
					'dept':data[0][4],
					'inst':data[0][5],
					'country':data[0][6]
					})
	except:
		print sys.exc_info()
	return user_recs

@csrf_exempt
def refresh(request):
	try:
		user = request.session['id']
		recs = []
		own_papers = []
		s_likes = []
		likes = []
		cursor = connection.cursor()
		cursor.execute("""SELECT likes, s_likes from pcs_authors where id = '%s';""" %(user))
		data = cursor.fetchall()
		if(data[0][0] != None):
			likes.extend(json.loads(data[0][0]))
		if(data[0][1] != None):
			s_likes.extend(json.loads(data[0][1]))
		if(user in p.author_likes):
			if((data[0][0] == None) and ('likes' in p.author_likes[user].keys())):
				likes.extend(p.author_likes[user]['likes'])
			if('own_papers' in p.author_likes[user].keys()):
				likes.extend(p.author_likes[user]['own_papers'])
		if(data[0][0] == None):
			l = list(set(likes))
			cursor.execute("""UPDATE pcs_authors SET likes = '%s' where id = '%s';""" %(json.dumps(l), user))
		if(len(likes)>0):
			recs = r.get_item_based_recommendations(likes)
		user_recs =  get_similar_people(request)
		return HttpResponse(json.dumps({
			'login_id': request.session['id'], 
			'login_name': request.session['name'],
			'recs':recs, 
			'likes':likes, 
			's_likes':s_likes,
			'user_recs': user_recs
			}), mimetype="application/json")
	except:
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")



@csrf_exempt
def get_recs(request):
	try:
		papers = json.loads(request.POST["papers"])
		recs = r.get_item_based_recommendations(papers)
		return HttpResponse(json.dumps(recs), mimetype="application/json")
	except:
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")



@csrf_exempt
def log(request, page):
	try:
		cursor = connection.cursor()
		cursor.execute("""INSERT into logs (login_id, action, data) values ('%s', '%s', '%s');""" %(request.session['id'], page, 'load'))
		return HttpResponse(json.dumps({'error':False}), mimetype="application/json")
	except:
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")



@csrf_exempt
def like(request, like_str):
	try:
		papers = json.loads(request.POST["papers"])
		sessions = []
		if('session' in request.POST):
			sessions = json.loads(request.POST['session'])
		s = ','.join(papers)
		user = request.session['id']
		res = {}
		likes = []
		s_likes = []
		cursor = connection.cursor()
		cursor.execute("""SELECT likes, s_likes from pcs_authors where id = '%s';""" %(user))
		data = cursor.fetchall()
		print data
		if(data[0][0] != None):
			likes = json.loads(data[0][0])
		if(data[0][1] != None):
			s_likes = json.loads(data[0][1])
		cursor.execute("""INSERT into logs (login_id, action, data) values ('%s', '%s', '%s');""" %(request.session['id'], like_str, s))

		for paper_id in papers:
			if(like_str=='star' and (paper_id not in likes) and paper_id != ''):
				likes.append(paper_id)
			if(like_str=='unstar' and (paper_id in likes) and paper_id != ''):
				likes.remove(paper_id)
			if(paper_id in likes):
				res[paper_id] = 'star'
			else:
				res[paper_id] = 'unstar'
		l = list(set(likes))
		for session in sessions:
			if(like_str=='star' and (session not in s_likes) and session != ''):
				s_likes.append(session)
			if(like_str=='unstar' and (session in s_likes) and session != ''):
				s_likes.remove(session)
		s_l = list(set(s_likes))
		cursor.execute("""UPDATE pcs_authors SET likes = '%s', s_likes = '%s' where id = '%s';""" %(json.dumps(l), json.dumps(s_l), user))
		recs = r.get_item_based_recommendations(likes)
		return HttpResponse(json.dumps({'recs':recs, 'likes':l, 's_likes':s_l, 'res':res}), mimetype="application/json")
	except:
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")




