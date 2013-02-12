from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import json, sys, re
from recommend import *
'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

def index(request):
	return render_to_response("index.html")

@csrf_exempt	
def recommend(request):
	if(request.POST):
		res = get_recommendations(request.POST['person'])
		return HttpResponse(json.dumps(res), mimetype="application/json")
	else:
		return HttpResponse("invalid request type")		


