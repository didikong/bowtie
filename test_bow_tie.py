import networkx as nx
import bow_tie
import time
from main import Graph

G = nx.gnp_random_graph(2000, 0.0008, None, 1)
print "graph created. start calculation..."

t1 = time.time()

graph = Graph(G)
graph.stats()
print graph.bow_tie

t2 = time.time()

print bow_tie.BowTie(G)

t3 = time.time()
print "Time for the first programm: %s" %(t2-t1)
print "Time for the second programm: %s" %(t3-t2)
