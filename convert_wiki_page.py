import networkx as nx
import matplotlib.pyplot as plt
from main import Graph
from main import GraphCollection
from main import Plotting
import string
from bow_tie import BowTie

def readPageDetails(filename):
	txtfile = open(filename, 'r')
	name_list = list()
	id_list = list()
	i = 0
	for line in txtfile:
		if line.startswith("INSERT") == 1:
			line = line[27:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				if insert[1] == '0':
					id_list.append(insert[0])
					name_list.append(hash(insert[2]))
					i = i + 1
	lookup = dict(zip(name_list, id_list))
	txtfile.close()
	return lookup

def readPageLinks(filename, outname, lookup):
	txtfile = open(filename, 'r')
	outfile = open(outname, 'w')
	i = 0
	for line in txtfile:
		if line.startswith("INSERT") == 1:
			line = line[32:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				if len(insert) < 3:
					i = i + 1
					continue
				if insert[1] == '0':
					try:
						page_id = lookup[hash(insert[2])]
						outfile.write(insert[0] + "\t" + page_id + "\n")
					except:
						None
	print i
	txtfile.close()
	outfile.close()


print "start"
language = "en"
i = 2006
lookup = readPageDetails("wiki_source/" + language + "/" + language +"wiki-" + str(i) + "-page.sql")
print "Details read"
readPageLinks("wiki_source/" + language + "/" + language +"wiki-" + str(i) + "-pagelinks.sql", "wiki_source/" + language + "/" + language + "-" + str(i) + ".txt", lookup)

