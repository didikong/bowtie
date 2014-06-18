import networkx as nx
import matplotlib.pyplot as plt
from main import Graph
import string
import bow_tie

def readPageDetails(filename):
	txtfile = open(filename, 'r')
	name_list = list()
	id_list = list()
	for line in txtfile:
		if line.startswith("INSERT") == 1:
			line = line[27:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				id_list.append(insert[0])
				name_list.append(hash(insert[2]))

	lookup = dict(zip(name_list, id_list))
	txtfile.close()
	return lookup

def readPageLinks(filename, lookup):
	txtfile = open(filename, 'r')
	i = 0
	j = 0
	G = nx.DiGraph()
	for line in txtfile:
		if line.startswith("INSERT") == 1:
			line = line[32:]
			data = line.split("),(")
			for insert_line in data:
				insert = insert_line.split(',')
				try:
					page_id = lookup[hash(insert[2])]
					G.add_edge(insert[0], page_id)
					i = i + 1
				except:
					j = j + 1
	txtfile.close()
	return G


print "start"
lookup = readPageDetails("wiki_source/mnwiki-20140525-page.sql")
print "Details read"
G = readPageLinks("wiki_source/mnwiki-20140525-pagelinks.sql", lookup)
print "Graph constructed"
print "nodes: %i" %(G.number_of_nodes())
print "edges: %i" %(G.number_of_edges())

print bow_tie.BowTie(G)

#graph = Graph(G)
#graph.stats()
#print graph.bow_tie
print "end"
