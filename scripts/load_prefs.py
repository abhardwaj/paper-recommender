#!/usr/bin/python
import psycopg2, re, sys, csv
from psycopg2.extensions import adapt

'''
@author: anant bhardwaj
@date: Jan 30, 2012

script for inserting the prefs data in postgres db
'''


connection = None
cursor = None 


# insert data
def insert_data():
	data_file = csv.reader(open("../data/prefs.csv", "rb"))
	data_file.next()
	for row in data_file:
		#print row	  
		try:
			qry = "INSERT into prefs values(%s, %s, %s, %s, %s, %s, %s, %s, %s);" %(adapt(row[2]), adapt(row[3]), adapt(row[4]), adapt(row[5]), adapt(row[6]),  adapt(row[7]),  adapt(row[8]),  adapt(row[9]),  adapt(row[10]))
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
	except psycopg2.ProgrammingError:
		connection.rollback()
		qry = "CREATE TABLE prefs (name TEXT, paper_id varchar(20), presenter TEXT, options TEXT, great_together TEXT, ok_together TEXT, not_ok_together TEXT, do_not_know TEXT, interested_in TEXT);"
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
