import re
import time, datetime

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime

def read_file(filename, conn, titles):
	txtfile = open(filename, 'r')
	pagefile = open("page.txt", 'w')

	title = None
	namespace = None
	page_id = None
	page = 0
	timestamp = None
	text = None
	prev_links_set = None
	link_regex = re.compile('\[\[([^#\|\]]+)')
	
	x = 0
	y = 0
	i = 0
	for line in txtfile:
		line = line.lstrip()
		i = i + 1
		if i%470000 == 0:
			print float(i)/470000
		if line.startswith("<title>") == 1:
			title = line[7:-9]
			page = 1
			previous_links = None
			#print "Title: %s" %(title)
		if line.startswith("<ns>") == 1 and page == 1:
			namespace = line[4:-6]
		if line.startswith("<id>") == 1 and page == 1:
			page_id = line[4:-6]
			page = 2
		if line.startswith("<timestamp>"):
			timest = datetime.datetime.strptime(line[11:-13], "%Y-%m-%dT%H:%M:%SZ")
			if page == 2:
				page = 0
				#pagefile.write(title + "\t" + page_id + "\t" + timestamp + "\n")
		if line.startswith("<text"):
			text = line
			old_links = set()
			links = set(link_regex.findall(text))
			if len(links) > 0:
				if previous_links == None:
					new_links = links
				else:
					new_links = links.difference(previous_links)
					old_links = previous_links.difference(links)
				for link in new_links:
					if link.replace(" ", "_") in titles:
						x = x + 1
						print "found"
						print link
					else:
						y = y + 1
						print "not found"
						print link
					'''print "%s \t %s \t %s \t %d" %(page_id, link, timestamp, 1)
					ins = table_links.insert().values(page_id=int(page_id), link=link, timestamp=timest, add_remove=1)
					result = conn.execute(ins)'''
				'''for link in old_links:
					print "%s \t %s \t %s \t %d" %(page_id, link, timestamp, 0)
					ins = table_links.insert().values(page_id=int(page_id), link=link, timestamp=timestamp, add_remove=0)
					result = conn.execute(ins)'''
				previous_links = links
			#print "%s \t %s" %(page_id, text)
		if i > 1000000:
			break
	print "found"
	print x
	print "not found"
	print y
	txtfile.close()
	pagefile.close()


def read_titles(filename):
	txtfile = open(filename, 'r')
	titles = set()
	i = 0
	for line in txtfile:
		titles.add(line.replace("\n", ""))
		i = i + 1
		if i%337000 == 0:
			print float(i)/337000
	return titles


print "start"
#connect to DB
engine = create_engine('sqlite:///:memory:', echo=True)
conn = engine.connect()
metadata = MetaData()
#create table
table_links = Table('links', metadata,
		Column('id', Integer, primary_key=True),
		Column('page_id', Integer),
		Column('link', String),
		Column('timestamp', DateTime),
		Column('add_remove', Integer))
metadata.create_all(engine)

titles = read_titles("/windows/C/Users/Digikong/Desktop/Didikong/Uni/Master/Masterprojekt/enwiki/enwiki-20140903-all-titles")
#read_file("wiki_source/mn/mnwiki-short-history.xml")
read_file("/windows/C/Users/Digikong/Desktop/Didikong/Uni/Master/Masterprojekt/enwiki/enwiki-20140903-pages-meta-history3.xml-p000053453p000055000", conn, titles)
print "end"



