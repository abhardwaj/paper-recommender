#!/usr/bin/python
import re, sys, csv, os

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

from models import *

'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for preparing data in lenskit format
'''






# insert data
def prepare():
	f = open('data_lenskit.txt','w')
	prefs = Prefs.objects.all()
	for p in prefs:
		f.write("%s\t%s\t%s\t%s\tu'%s\t%s\t%s\n" %(p.author.id, p.paper.id, p.rating, 98765, \
			p.author.name.encode('ascii','ignore'), p.author.paper.p_id, p.paper.p_id))
		


	
	

def main():
  print "setting up the table..."
  prepare()
  print "done."
  

if __name__ == '__main__':
    main()
