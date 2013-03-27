#!/usr/bin/python
import os, sys, MySQLdb


'''
@author: anant bhardwaj
@date: Feb 12, 2013

load prefs
'''


class Prefs:

	def __init__(self):
		self.author_prefs = {}
		self.paper_prefs = {}
		self.author_likes = {}
		self.__load__()

	def __load__(self):
		conn = MySQLdb.connect(host="mysql.csail.mit.edu", user="cobi", passwd="su4Biha", db="cobiDev")
		cursor = conn.cursor()
		cursor.execute("SELECT authorId , id, great, ok, notsure, notok, interested FROM authorsourcing;")
		data = cursor.fetchall()
		for row in data:
			author_prefs = {}
			# rate his own paper as great
			if(row[1]!=''):
				self.paper_prefs[row[1]] = {}
				author_prefs.update({row[1]:5.0})
			# great: 5, ok: 3.0, not_sure: 2.0, not_ok: 1.0
			if(row[2]!=''):
				author_prefs.update({p:5.0 for p in row[2].split(',')})
			if(row[3]!=''):
				author_prefs.update({p:3.0 for p in row[3].split(',')})
			if(row[4]!=''):
				author_prefs.update({p:2.0 for p in row[4].split(',')})
			if(row[5]!=''):
				author_prefs.update({p:1.0 for p in row[5].split(',')})

			if(row[0]!='' and row[6]!=''):
				self.author_likes[row[0]] = row[6].split(',')
			if(row[1]!=''):
				self.paper_prefs[row[1]].update(author_prefs)

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
