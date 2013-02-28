from math import sqrt
import sys, os, operator

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")

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
		temp[paper_id] = 5.0
		for g in great_together.split(','):
			temp[g] = 5.0
		for o in ok_together.split(','):
			temp[o] = 2.0
		for d in do_not_know.split(','):
			temp[d] = 1.0
		
		data[paper_id]= temp
	return data



'''
returns a distance-base similarity score for person1 and person2
'''
def sim_ecld(prefs, p1, p2):
	# get the list of shared_items
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item] = 1

	# if they have no rating in common, return 0
	if len(si) == 0: 
		return 0

	# add up the squares of all differences
	d = sqrt(sum([pow((prefs[p1][item]-prefs[p2][item]),2) for item in prefs[p1] if item in prefs[p2]]))

	return 1 / (1 + d)




'''
returns the Pearson correlation coefficient for p1 and p2 
'''
def sim_pearson(prefs,p1,p2):
	# get the list of mutually rated items
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]: 
			si[item] = 1

	
	if len(si) == 0:
		return 0

	# sum calculations
	n = len(si)

	# sum of all preferences
	sum1 = sum([prefs[p1][it] for it in si])
	sum2 = sum([prefs[p2][it] for it in si])

	# sum of the squares
	sum1_sq = sum([pow(prefs[p1][it],2) for it in si])
	sum2_sq = sum([pow(prefs[p2][it],2) for it in si])

	# sum of the products
	prod_sum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

	# calculate r (Pearson score)
	num = (n*prod_sum) - (sum1 * sum2)
	den = sqrt(((n*sum1_sq) - pow(sum1,2)) * (n*(sum2_sq) - pow(sum2,2)))
	if den == 0:
		return 0

	r = num/den
	return r



'''
returns the best matches for p from the prefs dictionary 
'''
def get_top_matches(prefs, p, similarity=sim_pearson, n=10):
	scores = [(similarity(prefs,p,other),other)
				for other in prefs if other != p]
	scores.sort()
	scores.reverse()
	return scores





def get_similar_items(prefs):
	result = {}
	# invert the preference matrix to be item-centric
	item_prefs = transform_prefs(prefs)
	for item in item_prefs:
		scores = get_top_matches(item_prefs,item)
		result[item] = scores
	return result



'''
gets recommendations for a person by using a weighted average of every other user's rankings
'''
def get_user_based_recommendations(person, prefs, similarity=sim_pearson, n=10):
	totals = {}
	sim_sum = {}
	#print person
	#print prefs[person]
	for other in prefs:
		# don't compare to itself
		if other == person:
			continue
		sim = similarity(prefs,person,other)
		#print sim, person, other
		# ignore non-corelated users
		if sim <= 0: 
			continue
		for item in prefs[other]:
			# only score items you haven't seen yet
			if(item not in prefs[person]):
				#print item
				# similarity * score
				totals.setdefault(item,0)
				totals[item] += prefs[other][item] * sim
				# sum of similarities
				sim_sum.setdefault(item,0)
				sim_sum[item] += sim

	# the normalized list
	normalized = {}
	for item,total in totals.items():
		normalized[item] = total/sim_sum[item]
	
	rankings = sorted(normalized.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print rankings
	res = [{'item':item, 'score':score} for item,score in rankings]
	return res[0:n]
	


'''
gets recommendations for a person by using a weighted average of every other user's rankings
'''
def get_item_based_recommendations(person, prefs, similar_items, similarity=sim_pearson, n=10):
	ratings = prefs[person]
	totals = {}
	sim_sum = {}

	# loop over items rated by this user
	for (item, rating) in ratings.items():
		# loop over items similar to this one
		for (similarity, item2) in similar_items[item]:
			# ignore if this user has already rated this item
			if item2 in ratings:
				continue
			if(similarity<0.3):
				continue
			# weighted sum of rating times similarity
			totals.setdefault(item2,0)
			totals[item2] += similarity * rating
			#Sum of all the similarities
			sim_sum.setdefault(item2,0)
			sim_sum[item2]+=similarity

	normalized = {}
	for item,total in totals.items():
		normalized[item] = total

	rankings = sorted(normalized.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print rankings
	res = [{'item':item, 'score':score} for item,score in rankings]
	return res[0:n]




# transform Person, item - > Item, person
def transform_prefs(prefs):
	results = {}
	for p in prefs:
		for item in prefs[p]:
			results.setdefault(item,{})

			# flip item and person
			results[item][p] = prefs[p][item]
	return results




def main():
	data = load_data()
	similar_items = get_similar_items(data)
	#res = get_user_based_recommendations('pn1566', data)
	#print res
	#print "=============================="
	res = get_item_based_recommendations('pn1460', data, similar_items)
	print res


if __name__ == "__main__":
	main()
