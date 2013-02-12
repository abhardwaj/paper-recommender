from django.db import models

'''
CHI2013 Recommender Models

@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

class Prefs(models.Model):
	id = models.AutoField(primary_key=True)
	author_id = models.CharField(max_length=20, unique=True, null = True)
	name = models.TextField()
	paper_id = models.CharField(max_length=20)
	presenter = models.TextField()
	options = models.TextField()
	great_together = models.TextField()
	ok_together = models.TextField()
	not_ok_together = models.TextField()
	do_not_know = models.TextField()
	interested_in = models.TextField()

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = "prefs"
		app_label = 'paper_recommender'