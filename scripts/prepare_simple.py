import sys, os, json

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))

from db.prefs import *


def main():
	p = Prefs()
	data = p.get_paper_prefs()
	f = open('data/data_simple.txt','w')
	f.write(json.dumps(data))


if __name__ == "__main__":
	main()
