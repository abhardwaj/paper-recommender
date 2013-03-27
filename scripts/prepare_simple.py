from math import sqrt
import sys, os, operator, json

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from models import *



def load_data():
	data = {}
	prefs = Prefs.objects.all()
	for p in prefs:
		if p.author.paper.p_id not in data:
			data[p.author.paper.p_id]={}
		data[p.author.paper.p_id][p.paper.p_id] = p.rating
	return data




def main():
	data = load_data()
	f = open('data_simple.txt','w')
	f.write(json.dumps(data))


if __name__ == "__main__":
	main()
