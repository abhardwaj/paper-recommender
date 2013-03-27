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


def encode_author_id(paper_id, authorId):
	ret = 0
	author_id = 0
	if(authorId!=''):
		author_id = int(authorId[4:])
	if(paper_id.startswith('alt')):
		ret= '1%05d%06d' %(int(paper_id[3:]), author_id)
	elif(paper_id.startswith('case')):
		ret= '2%05d%06d' %(int(paper_id[4:]), author_id)
	elif(paper_id.startswith('crs')):
		ret= '3%05d%06d' %(int(paper_id[3:]), author_id)
	elif(paper_id.startswith('pan')):
		ret= '4%05d%06d' %(int(paper_id[3:]), author_id)
	elif(paper_id.startswith('pn')):
		ret= '5%05d%06d' %(int(paper_id[2:]), author_id)
	elif(paper_id.startswith('sig')):
		ret= '6%05d%06d' %(int(paper_id[3:]), author_id)
	elif(paper_id.startswith('tochi')):
		ret= '7%05d%06d' %(int(paper_id[5:]), author_id)
	return long(ret)


def encode_paper_id(paper_id):
	ret = ''
	if(paper_id.startswith('alt')):
		ret= '1%05d' %(long(paper_id[3:]))
	elif(paper_id.startswith('case')):
		ret= '2%05d' %(long(paper_id[4:]))
	elif(paper_id.startswith('crs')):
		ret= '3%05d' %(long(paper_id[3:]))
	elif(paper_id.startswith('pan')):
		ret= '4%05d' %(long(paper_id[3:]))
	elif(paper_id.startswith('pn')):
		ret= '5%05d' %(long(paper_id[2:]))
	elif(paper_id.startswith('sig')):
		ret= '6%05d' %(long(paper_id[3:]))
	elif(paper_id.startswith('tochi')):
		ret= '7%05d' %(long(paper_id[5:]))
	return long(ret)

def decode_paper_id(long_id):
	str_id = str(long_id)
	prefix = int(str_id[0:1])
	paper_id_str = str(int(str_id[1:]))
	paper_id_pre= ''
	if(prefix == 1):
		paper_id_pre= 'alt'
	elif(prefix == 2):
		paper_id_pre= 'case'
	elif(prefix == 3):
		paper_id_pre= 'crs'
	elif(prefix == 4):
		paper_id_pre= 'pan'
	elif(prefix == 5):
		paper_id_pre= 'pn'
	elif(prefix == 6):
		paper_id_pre= 'sig'
	elif(prefix == 7):
		paper_id_pre= 'tochi'
	return paper_id_pre+paper_id_str

class Prefs:

	def __init__(self):
		self.author_prefs = {}
		self.paper_prefs = {}
		self.author_likes = {}
		self.__load__()


	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT id, authorId, great, ok, notsure, notok, interested FROM authorsourcing;")
		data = cursor.fetchall()
		for row in data:
			paper_id = encode_author_id(row[0].strip(), row[1].strip())

			# rate his own paper as great
			author_prefs = {encode_paper_id(row[0].strip()):5.0}
						
			# great: 5, ok: 3.0, not_sure: 2.0, not_ok: 1.0
			if(row[2]!=''):
				author_prefs.update({encode_paper_id(p.strip()):5.0 for p in row[2].split(',')})
			if(row[3]!=''):
				author_prefs.update({encode_paper_id(p.strip()):3.0 for p in row[3].split(',')})
			if(row[4]!=''):
				author_prefs.update({encode_paper_id(p.strip()):2.0 for p in row[4].split(',')})
			if(row[5]!=''):
				author_prefs.update({encode_paper_id(p.strip()):1.0 for p in row[5].split(',')})

			self.paper_prefs[paper_id] = author_prefs

			# update author_likes
			if(row[1]!='' and row[6]!=''):
				self.author_likes[row[1].strip()] = [p.strip() for p in row[6].split(',')]
			
				

	

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
