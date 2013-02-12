#!/usr/bin/python
import psycopg2, re, sys, csv, os
from psycopg2.extensions import adapt

'''
@author: anant bhardwaj
@date: Feb 12, 2013

script for inserting the prefs data in postgres db
'''


connection = None
cursor = None 


# insert data
def insert_data():
	path = os.path.dirname(os.path.abspath(__file__))
	data_file = csv.reader(open( path + "/../data/prefs.csv", "rb"))
	data_file.next()
	for row in data_file:
		#print row	  
		try:
			qry = "INSERT into prefs \
			(name, paper_id, presenter, options, great_together, \
			ok_together, not_ok_together, do_not_know, interested_in) \
			values(%s, %s, %s, %s, %s, %s, %s, %s, %s);" \
			%(adapt(row[2]), adapt(row[3]), adapt(row[4]), adapt(row[5]), adapt(row[6]), \
			 adapt(row[7]),  adapt(row[8]),  adapt(row[9]),  adapt(row[10]))
			cursor.execute(qry)		
		except:
			connection.rollback()
			print "Unexpected error:", sys.exc_info()

		connection.commit()
	

# delete data
def setup():
	global connection
	global cursor
	try:
		connection = psycopg2.connect(host='localhost', database='chi2013', user='postgres', password='postgres')
		cursor = connection.cursor()
		qry = "DELETE from prefs;"
		cursor.execute(qry)
		connection.commit()
		return True
	except:
		print "Error:", sys.exc_info()
		return False
	
	

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
