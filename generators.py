from __future__ import division, unicode_literals

import unittest
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from main import Graph
from main import Plotting
from main import GraphCollection

print "start"

n = 500
p_start = 0
p_end = 0.05
p_step = 0.005
number_of_average = 10

x = []
scc = []
legend = ["inc", "scc", "outc", "in_tendril", "out_tendril", "tube", "other"]

p = p_start
while p < p_end:
	average = np.array([0,0,0,0,0,0,0])
	for i in range(number_of_average):
		G = nx.gnp_random_graph(n, p, None, 1)
		graph = Graph(G)
		graph.stats()
		average = average + graph.bow_tie
	average = average / number_of_average
	x.append(p)
	scc.append(average)
	p = p + p_step



plt.plot(x, scc)
plt.legend(legend, loc='right', shadow=True)
plt.xlabel('probability for edge creation')
plt.ylabel('percent') 
plt.savefig('test.png')


print "stop"
