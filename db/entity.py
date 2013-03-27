#!/usr/bin/python
import os, sys, json


if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
from django.db import connection

'''
@author: anant bhardwaj
@date: Feb 12, 2013

load entities
'''


class Entity:

	def __init__(self):
		self.entities = {}
		self.__load__()

	def __load__(self):
		cursor = connection.cursor()
		cursor.execute("SELECT id , authors, title FROM entity;")
		data = self.cursor.fetchall()
		for row in data:
			if(row[0]!=''):
				self.entities[row[0]]={}
				self.entities[row[0]]['title']=row[2]
				self.entities[row[0]]['authors']=json.loads(row[1])


	def get_entities(self):
		return self.entities

	

def main():
  e = Entity()
  print e.get_entities()
  

if __name__ == '__main__':
    main()
