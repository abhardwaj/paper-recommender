#!/usr/bin/python
import sys, os

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from db.prefs import *

'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for preparing data in lenskit format
'''






# insert data
def prepare(prefs):
	f = open('data/data_lenskit.txt','w')	
	for k,v in prefs.iteritems():
		for p, r in v.iteritems():
			f.write("%s\t%s\t%s\n" %(k, p, r))




def main():
	p = Prefs()
	prefs = p.get_paper_prefs()
  	prepare(prefs)
  	print "done."
  

if __name__ == '__main__':
    main()
