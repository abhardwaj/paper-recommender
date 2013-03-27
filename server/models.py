from django.db import models

'''
CHI2013 Recommender Models

@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

class Prefs(models.Model):
	id = models.AutoField(primary_key=True)
	author = models.ForeignKey('Author')
	paper = models.ForeignKey('Paper')
	rating=models.FloatField()

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = "prefs"
		app_label = 'recommender'


class Paper(models.Model):
	id = models.AutoField(primary_key=True)
	p_id = models.TextField()

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = "papers"
		app_label = 'recommender'



class Author(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField()
	paper = models.ForeignKey('Paper')
	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = "authors"
		app_label = 'recommender'
