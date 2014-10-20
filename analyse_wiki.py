import matplotlib.pyplot as plt
from main import Graph
from main import GraphCollection
from main import Plotting
from bow_tie import BowTie

def readSource(filename):
	txtfile = open(filename, 'r')
	graph = BowTie()
	set_of_nodes = set()
	for line in txtfile:
		edge = line.split('\t')
		edge[1] = edge[1].rstrip('\n')
		set_of_nodes.add(int(edge[0]))
		set_of_nodes.add(int(edge[1]))
		graph.set_edges(int(edge[0]), int(edge[1]))

	graph.set_nodes(set_of_nodes)
	txtfile.close()
	return graph



print "start"
language = "mn"
index = [1, 5, 10, 15]
gc = GraphCollection(language)
for i in index:    
	print "read..."
	graph = readSource("wiki_source/" + language + "/" + language +"-" + str(i) + ".txt")
	print "Graph constructed"
	gc.append(graph)
graphs = []
graphs.append(gc)
for g in graphs:
	print "calculate..."
	g.compute()
	P = Plotting(graphs)
