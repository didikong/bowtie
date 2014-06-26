import networkx as nx
import matplotlib.pyplot as plt
from main import Graph
from main import GraphCollection
from main import Plotting
from bow_tie import BowTie

def readSource(filename):
	G = nx.DiGraph()
	txtfile = open(filename, 'r')
	for line in txtfile:
		edge = line.split('\t')
		edge[1] = edge[1].rstrip('\n')
		G.add_edge(edge[0], edge[1])

	txtfile.close()
	return G



print "start"
language = "en"
index = [2006, 2008, 2013, 2014]
gc = GraphCollection(language)
for i in index:    
	print "read..."
	G = readSource("wiki_source/" + language + "/" + language +"-" + str(i) + ".txt")
	print "Graph constructed"
	print G.number_of_nodes()
	print G.number_of_edges()
	graph = BowTie(G)
	gc.append(graph)
graphs = []
graphs.append(gc)
for g in graphs:
	print "calculate..."
	g.compute()
	P = Plotting(graphs)
