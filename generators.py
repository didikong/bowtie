from __future__ import division, unicode_literals

import unittest
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

from main import Graph
from main import Plotting
from main import GraphCollection


def barabasi_albert_graph_directed(n, m):
	if m < 1 or  m >=n:
		raise nx.NetworkXError("Barabasi-Albert network must have m>=1 and m<n, m=%d,n=%d"%(m,n))
	G = nx.DiGraph()
	G.add_nodes_from(range(n))
	G.name="barabasi_albert_graph(%s,%s)"%(n,m)
	targets=list(range(n))
	for i in range(0, n, 1):
		rand = random.sample(targets, m)
		while i in rand:
			rand = random.sample(targets, m)
		G.add_edges_from(zip([i]*m, rand))
	return G


def watts_strogatz_graph_directed(n, k, p):
	if k>=n/2: 
		raise nx.NetworkXError("k>=n/2, choose smaller k or larger n")
	G = nx.DiGraph()
	G.name="watts_strogatz_graph(%s,%s,%s)"%(n,k,p)
	nodes = list(range(n))
	for j in range(1, k // 2+1):
		targets = nodes[j:] + nodes[0:j]
		edges = zip(nodes, targets) + zip(targets, nodes)
		G.add_edges_from(edges)
	for j in range(1, k // 2+1): # outer loop is neighbors
		targets = nodes[j:] + nodes[0:j]
		edges = zip(nodes, targets) + zip (targets, nodes)
		for u,v in edges:
			if random.random() < p:
				w = u
				while w == u or w == v: 
					w = random.choice(nodes)
				G.remove_edge(u,v)  
				G.add_edge(u,w)
	return G






def erdoes(n, p_start, p_end, p_step, number_of_average):
	x = []
	bow_tie = []
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
		bow_tie.append(average)
		p = p + p_step

	plt.plot(x, bow_tie)
	plt.legend(legend, loc='right', shadow=True)
	plt.xlabel('probability for edge creation')
	plt.ylabel('percent') 
	plt.savefig('test.png')


def watts_strogatz(n, k, p_start, p_end, p_step, number_of_average):
	x = []
	bow_tie = []
	legend = ["inc", "scc", "outc", "in_tendril", "out_tendril", "tube", "other"]

	p = p_start
	while p < p_end:
		average = np.array([0,0,0,0,0,0,0])
		for i in range(number_of_average):
			G = watts_strogatz_graph_directed(n, k, p)
			graph = Graph(G)
			graph.stats()
			average = average + graph.bow_tie
		average = average / number_of_average
		x.append(p)
		bow_tie.append(average)
		p = p + p_step
	
	plt.plot(x, bow_tie)
	plt.legend(legend, loc='right', shadow=True)
	plt.xlabel('probability for edge rewiring')
	plt.ylabel('percent')
	plt.savefig('test.png')
	

def barabasi_albert(n, m_start, m_end, number_of_average):
	x = []
	bow_tie = []
	legend = ["inc", "scc", "outc", "in_tendril", "out_tendril", "tube", "other"]

	m = m_start
	while m < m_end:
		average = np.array([0,0,0,0,0,0,0])
		for i in range(number_of_average):
			G = barabasi_albert_graph_directed(n, m)
			graph = Graph(G)
			graph.stats()
			average = average + graph.bow_tie
		average = average / number_of_average
		x.append(m)
		bow_tie.append(average)
		m = m + 1

	plt.plot(x, bow_tie)
	plt.legend(legend, loc='right', shadow=True)
	plt.xlabel('number of edges from new node')
	plt.ylabel('percent')
	plt.savefig('test.png')




print "start"

#parameters
n = 500
p_start = 0
p_end = 1
p_step = 0.05
number_of_average = 10
k = 2
m_start = 1
m_end = 5

#erdoes(n, p_start, p_end, p_step, number_of_average)
watts_strogatz(n, k, p_start, p_end, p_step, number_of_average)
#barabasi_albert(n, m_start, m_end, number_of_average)

print "stop"



