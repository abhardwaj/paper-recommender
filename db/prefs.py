#!/usr/bin/python
import os, sys

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection
from algorithm.utils import *

'''
@author: anant bhardwaj
@date: Feb 12, 2013

load prefs
'''



class Prefs:

	def __init__(self):
		self.paper_prefs = {}
		self.author_likes = {}
		self.__load__()


	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT authorId, id, givenName, familyName FROM authors;")
		data = cursor.fetchall()
		for row in data:
			if(row[0].strip()==''):
				continue
			self.author_likes[unicode(row[0]).strip()] = {'name': unicode(row[2]).strip() + ' ' + unicode(row[3]).strip(), 'likes':[row[1].strip()]}



		cursor.execute("SELECT id, authorId, great, ok, notsure, notok, interested, name FROM authorsourcing;")
		data = cursor.fetchall()
		for row in data:
			if(row[0].strip()==''):
				continue
			paper_id = encode_author_id(unicode(row[0]).strip(), unicode(row[1]).strip())

			# rate his own paper as great
			author_prefs = {encode_paper_id(unicode(row[0]).strip()):5.0}
						
			# great: 5, ok: 3.0, not_sure: 2.0, not_ok: 1.0
			if(row[6]!=''):
				author_prefs.update({encode_paper_id(unicode(p).strip()):5.0 for p in row[6].split(',')})
			if(row[2]!=''):
				author_prefs.update({encode_paper_id(unicode(p).strip()):5.0 for p in row[2].split(',')})
			if(row[3]!=''):
				author_prefs.update({encode_paper_id(unicode(p).strip()):3.0 for p in row[3].split(',')})
			if(row[4]!=''):
				author_prefs.update({encode_paper_id(unicode(p).strip()):2.0 for p in row[4].split(',')})
			if(row[5]!=''):
				author_prefs.update({encode_paper_id(unicode(p).strip()):1.0 for p in row[5].split(',')})

			self.paper_prefs[paper_id] = author_prefs
			likes = [unicode(p).strip() for p in row[6].split(',')]
			

			# update author_likes
			if(row[1]!='' and row[6]!=''):
				self.author_likes[unicode(row[1]).strip()]['likes'].extend(likes)
	

	def get_paper_prefs(self):
		return self.paper_prefs

	def get_author_likes(self):
		return self.author_likes

def main():
  p = Prefs()
  print p.get_author_likes()
  print p.get_paper_prefs()
  

if __name__ == '__main__':
    main()
