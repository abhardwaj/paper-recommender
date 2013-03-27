#!/usr/bin/python
import os, sys, MySQLdb, json

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
		conn = MySQLdb.connect(host="mysql.csail.mit.edu", user="cobi", passwd="su4Biha", db="cobiDev")
		cursor = conn.cursor()
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
