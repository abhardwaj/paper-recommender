import sys, os, json, csv

if __name__ == "__main__":
	p = os.path.abspath(os.path.dirname(__file__))
	if(os.path.abspath(p+"/..") not in sys.path):
		sys.path.append(os.path.abspath(p+"/.."))
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")





def main():
	f = open('data/sigchiUsers.csv','r')
	reader = csv.reader(f)
	for row in reader:
		print len(row)


if __name__ == "__main__":
	main()
