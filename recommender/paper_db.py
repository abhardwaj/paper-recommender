import os, re, sys
import MySQLdb

class AuthorSourceDatabase:

	def __init__(self):
		self.conn = MySQLdb.connect(host="mysql.csail.mit.edu", user="cobi", passwd="su4Biha", db="cobiDev")
		self.cursor = self.conn.cursor()
		print (self.conn)


	def get_all(self):
		self.cursor.execute("""SELECT authorId , interested FROM authorsourcing;""")
		data = self.cursor.fetchall()
		if data == None:
		       	return None
		for row in data:
			print row

	def get_author_data(self, id):
		self.cursor.execute("select authors, title from entity where id='%s'" %(id))
		data = self.cursor.fetchone()
		if data == None:
		       	return None
		else:
			#print data
			return data