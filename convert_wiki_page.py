import networkx as nx
import matplotlib.pyplot as plt
from main import Graph
from main import GraphCollection
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

def readPageLinks(filename, lookup):
	txtfile = open(filename, 'r')
	G = nx.DiGraph()
	for line in txtfile:
		if line.startswith("INSERT") == 1:
			line = line[32:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				if insert[1] == '0':
					try:
						page_id = lookup[hash(insert[2])]
						G.add_edge(insert[0], page_id)
					except:
						None
	txtfile.close()
	return G


print "start"
language = "mn"
index = [1, 5, 10, 15]
gc = GraphCollection(language)
for i in index:
	lookup = readPageDetails("wiki_source/" + language + "/" + language +"wiki-" + str(i) + "-page.sql")
	print "Details read"
	G = readPageLinks("wiki_source/" + language + "/" + language +"wiki-" + str(i) + "-pagelinks.sql", lookup)
	print "Graph constructed"
	graph = BowTie(G)
	gc.append(graph)

graphs = []
graphs.append(gc)
for g in graphs:
	print "calculate..."
	g.compute()
P = Plotting(graphs)
