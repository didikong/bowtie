import re
import os
import time, datetime
import sys
import bz2
import urllib
import gzip

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime


def crawl_page(website, conn):
	websitename = "https://dumps.wikimedia.org"
	linkset = set()
	urlfile = urlopen(website)
	content = urlfile.read()
	soup = BeautifulSoup(content)
	lookup = None
	for li in soup.findAll('li', {'class':'file'} ):
		hrefs=li.findAll('a')
		for href in hrefs:
			link = str(href)[9:]
			try:
				s = link.index('"')
				link = link[:s]
			except:
				continue
			if "pages-meta-history" in link and link.endswith(".bz2"):
				linkset.add(websitename + link)
			if "page.sql" in link:
				print "download page informations..."
				infofile = urllib.URLopener()
				infofile.retrieve(websitename + link, "temp/page.sql.gz")
				lookup = readPageDetails("temp/page.sql.gz")
				os.remove("temp/page.sql.gz")
	for link in linkset:
		i = 1
		zipfile = urllib.URLopener()
		print "download meta-history file " + str(i) + "..."
		zipfile.retrieve(link, "temp/file" + str(i) + ".bz2")
		print "extract file " + str(i) + "..."
		read_file("temp/file" + str(i) + ".bz2", conn, lookup)
		os.remove("temp/file" + str(i) + ".bz2")
		i = i + 1

def read_file(filename, conn, lookup):
	
	handler = bz2.BZ2File(filename,'r')

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

	for line in handler:
		line = line.lstrip()
		i = i + 1
		if i%100000 == 0:
			print '\r' + 'read History! Process: ' + str(float(i)/1000000) + 'm rows',
			sys.stdout.flush()
		if line.startswith("<title>") == 1:
			title = line[7:-9]
			page = 1
			previous_links = None
		if line.startswith("<ns>") == 1 and page == 1:
			namespace = line[4:-6]
		if line.startswith("<id>") == 1 and page == 1:
			page_id = line[4:-6]
			page = 2
		if line.startswith("<timestamp>"):
			timestamp = datetime.datetime.strptime(line[11:-13], "%Y-%m-%dT%H:%M:%SZ")
			if page == 2:
				page = 0
				try:
					title = title.lower()
					title.replace(" ", "_")
					lookup[title]
					ins = table_pages.insert().values(title=title, page_id=page_id, timestamp=timestamp)
					result = conn.execute(ins)
				except:
					pass
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
					if ":" in link:
						continue
					link = link.lower()
					link = link.replace(" ", "_")
					try:
						link_id = lookup[link]
						ins = table_links.insert().values(page_id=int(page_id), link_id=link_id, timestamp=timestamp, add_remove=1)
						result = conn.execute(ins)
						x = x + 1
					except:
						y = y + 1
				for link in old_links:
					if ":" in link:
						continue
					link = link.lower()
					link = link.replace(" ", "_")
					try:
						link_id = lookup[link]
						ins = table_links.insert().values(page_id=int(page_id), link_id=link_id, timestamp=timestamp, add_remove=0)
						result = conn.execute(ins)
					except:
						pass
				previous_links = links

	print '\r' + 'read History! Process: Finish!     '
	print"found"
	print x
	print "not found"
	print y
	handler.close()



def readPageDetails(filename):
	#txtfile = open(filename, 'r')
	f = gzip.open(filename, 'r')
	name_list = list()
	id_list = list()
	i = 0
	for line in f:
		if line.startswith("INSERT") == 1:
			line = line[27:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				if insert[1] == '0':
					name = insert[2].replace("'", "")
					name = name.lower()
					name = name.replace(" ", "_")
					id_list.append(insert[0])
					name_list.append(name)
					i = i + 1
					if i%100000 == 0:
						print '\r' + 'read link list! Process: ' + str(float(i)/1000000) + 'm rows',
						sys.stdout.flush()
	print '\r' + 'read link list! Finish!     '
	lookup = dict(zip(name_list, id_list))
	f.close()
	return lookup


print "start"

website = "https://dumps.wikimedia.org/pdcwiki/20141118/"
user = "postgres"
password = ""
language = website.split('/')[3]
print language


#create new DB
engine = create_engine('postgres://' + user + ':' + password + '@localhost/postgres')
conn = engine.connect()
conn.execute("commit")
conn.execute("create database " + language)
conn.close()

#connect to DB
engine = create_engine('postgresql://' + user + ':' + password + '@localhost/' + language)
conn = engine.connect()
metadata = MetaData()

#create table link
table_links = Table('links', metadata,
		Column('page_id', Integer),
		Column('link_id', Integer),
		Column('timestamp', DateTime),
		Column('add_remove', Integer))

#create table title
table_pages = Table('pages', metadata,
		Column('title', String),
		Column('page_id', Integer, primary_key=True),
		Column('timestamp', DateTime))

metadata.create_all(engine)

crawl_page(website, conn)

print "end"



