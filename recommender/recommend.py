import sys, os, scikits
if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import *
from scikits.crab.similarities import *
from scikits.crab.recommenders.knn import *
from scikits.crab.recommenders.svd.classes import *
from scikits.crab.recommenders.knn.item_strategies import *
from models import *


def load_data():
	data = {}
	raw_data = Prefs.objects.all().values()
	for d in raw_data:
		great_together = d['great_together']
		ok_together = d['ok_together']
		not_ok_together = d['not_ok_together']
		do_not_know = d['do_not_know']
		paper_id = d['paper_id']
		name = d['name']
		temp = {}
		for g in great_together.split(','):
			temp[g] = 10.0
		for o in ok_together.split(','):
			temp[o] = 7.0
		for d in do_not_know.split(','):
			temp[d] = 3.0
		for n in not_ok_together.split(','):
			temp[n] = -10.0
		
		data[name]= temp
	return data






def main():	
	data = load_data()
	#print data
	matrix_model = MatrixPreferenceDataModel(data)
	print matrix_model.preferences_from_user('Jeff Huang')
	#items_strategy = AllPossibleItemsStrategy()
	items_strategy = ItemsNeighborhoodStrategy()
	#similarity = ItemSimilarity(matrix_model, euclidean_distances)
	#recommender = ItemBasedRecommender(matrix_model, similarity, items_strategy)
	recommender = MatrixFactorBasedRecommender(matrix_model, items_selection_strategy=items_strategy, with_preference=True)
	print recommender.recommend('Jeff Huang', how_many=10)
	

if __name__ == "__main__":
	main()
