#!/usr/bin/python
import os, sys

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.db import connection
'''
@author: anant bhardwaj
@date: Feb 12, 2013

load prefs
'''


def get_id(paper_id):
		ret = 0
		if(paper_id.startswith('alt')):
			ret= long('9999' + paper_id[3:])
		elif(paper_id.startswith('case')):
			ret= long('8888' + paper_id[4:])
		elif(paper_id.startswith('crs')):
			ret= long('7777' + paper_id[3:])
		elif(paper_id.startswith('pan')):
			ret= long('6666' + paper_id[3:])
		elif(paper_id.startswith('pn')):
			ret= long('5555' + paper_id[2:])
		elif(paper_id.startswith('sig')):
			ret= long('4444' + paper_id[3:])
		elif(paper_id.startswith('tochi')):
			ret= long('3333' + paper_id[5:])
		return ret

class Prefs:

	def __init__(self):
		self.author_prefs = {}
		self.paper_prefs = {}
		self.author_likes = {}
		self.__load__()


	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT authorId , id, great, ok, notsure, notok, interested FROM authorsourcing;")
		data = cursor.fetchall()
		for row in data:
			author_prefs = {}
			# rate his own paper as great
			if(row[1]!=''):
				self.paper_prefs[get_id(row[1])] = {}
				author_prefs.update({get_id(row[1]):5.0})
			# great: 5, ok: 3.0, not_sure: 2.0, not_ok: 1.0
			if(row[2]!=''):
				author_prefs.update({get_id(p):5.0 for p in row[2].split(',')})
			if(row[3]!=''):
				author_prefs.update({get_id(p):3.0 for p in row[3].split(',')})
			if(row[4]!=''):
				author_prefs.update({get_id(p):2.0 for p in row[4].split(',')})
			if(row[5]!=''):
				author_prefs.update({get_id(p):1.0 for p in row[5].split(',')})

			if(row[0]!='' and row[6]!=''):
				self.author_likes[row[0]] = row[6].split(',')
			if(row[1]!=''):
				self.paper_prefs[get_id(row[1])].update(author_prefs)

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
