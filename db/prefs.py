#!/usr/bin/python
import os, sys, csv, re

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

from models import *

'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for inserting the prefs data in postgres db
'''


connection = None
cursor = None 
papers = []
names = []

def get_author(author_name, p_id):
	author = None
	paper = get_paper(p_id)
	try:
		author = Author.objects.get(name=author_name, paper= paper)		
	except Author.DoesNotExist:
		author = Author(name=author_name, paper=paper)
		author.save()
	return author

def get_paper(p_id):
	paper = None
	try:
		paper = Paper.objects.get(p_id=p_id)		
	except Paper.DoesNotExist:
		paper = Paper(p_id=p_id)
		paper.save()
	return paper

def insert_data(author, paper, rating):
	prefs = Prefs(author=author, paper=paper, rating = rating)
	prefs.save()


# insert data
def load_data():
	path = os.path.dirname(os.path.abspath(__file__))
	data_file = csv.reader(open( path + "/../data/prefs.csv", "rb"))
	data_file.next()
	for row in data_file:
		#print row
		author = get_author(row[2].strip(), row[3].strip())
		for x in re.split(',',row[6]):			
			paper = get_paper(x.strip())
			insert_data(author, paper, 5)
		for x in re.split(',',row[7]):
			paper = get_paper(x.strip())
			insert_data(author, paper, 3)
		for x in re.split(',',row[9]):
			paper = get_paper(x.strip())
			insert_data(author, paper, 1)
	

# delete data
def setup():
	Prefs.objects.all().delete()
	Author.objects.all().delete()
	Paper.objects.all().delete()
	load_data();
	
	

def main():
  print "setting up the table..."
  res = setup()
  if(res):
  	print "inserting the data..."
  	insert_data()
	connection.close()
  print "done."
  

if __name__ == '__main__':
    main()
