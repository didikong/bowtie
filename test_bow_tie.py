import networkx as nx
from bow_tie import BowTie
import time
from main import Graph

G = nx.gnp_random_graph(500, 0.005, None, 1)
print "graph created. start calculation..."

'''
x = []
y = set()
for i in range(1,60000):
	if i not in y:
		x.append(i)
		y.add(i)
	if i%100 == 0:
		print i



'''
t1 = time.time()

graph = Graph(G)
graph.stats()
print graph.bow_tie

t2 = time.time()

graph = BowTie(G)
graph.stats()
print graph.bow_tie

t3 = time.time()
print "Time for the first programm: %s" %(t2-t1)
print "Time for the second programm: %s" %(t3-t2)
