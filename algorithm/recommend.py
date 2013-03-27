import sys, os, operator, json

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from db.entity import *;
from db.prefs import *
from py4j.java_gateway import JavaGateway


class Recommender:
	def __init__(self):
		p = Prefs()
		self.gateway = JavaGateway()

	def get_item_based_recommendations(self, paper_id):
		recs = self.gateway.entry_point.recommend(str(encode_paper_id(paper_id)))
		res=[]
		for rec in recs:
			r = rec.split(',')
			res.append({'id': decode_paper_id(long(r[0])), 'score': float(r[1])})
		return res


def main():
	r = Recommender()
	res = r.get_item_based_recommendations('pn1460')
	print res


if __name__ == "__main__":
	main()
