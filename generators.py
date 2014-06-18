from __future__ import division, unicode_literals
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

import unittest
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math

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
	G.add_nodes_from(range(n))
	G.name="watts_strogatz_graph(%s,%s,%s)"%(n,k,p)
	nodes = list(range(n))
	for j in range(k):
		i =  int(j/2)
		targets = nodes[i+1:] + nodes[0:i+1]
		if j%2 == 0:
			edges = zip(nodes, targets)
		else:
			edges = zip(targets, nodes)
		G.add_edges_from(edges)
	
	edges = G.edges()
	for u,v in edges:
		if random.random() < p:
			w = u
			while w==u or G.has_edge(u,w):
				w = random.choice(nodes)
			G.remove_edge(u,v)
			G.add_edge(u,w)
	return G


def create_random_nm_graph(n, m):
	if(m >= n):
		raise nx.NetworkXError("m>=n, choose smaller m")
	G = nx.DiGraph()
	G.add_nodes_from(range(n))
	G.name="random_nm_graph(%s,%s)"%(n,m)
	for i in range(0, n, 1):
		for j in range(0, m, 1):
			rand = random.randint(0, n-1)
			while rand == i or G.has_edge(i, rand):
				rand = random.randint(0, n-1)
			G.add_edge(i, rand)
	return G


def create_random_nm_graph_with_preferential_attachment(n, m):
	if(m >= n):
		raise nx.NetworkXError("m>=n, choose smaller m")
	G = nx.DiGraph()
	G.add_nodes_from(range(n))
	G.name="random_nm_graph_with_preferential_attachment(%s,%s)"%(n,m)
	P = list(range(n))
	for j in range(0, m, 1):
		for i in range(0, n, 1):
			rand_p = random.randint(0, len(P)-1)
			rand = P[rand_p]
			while rand == i or G.has_edge(i, rand):
				rand_p = random.randint(0, len(P)-1)
				rand = P[rand_p]
			G.add_edge(i, rand)
			P.append(rand)
	return G


def create_stochastic_block_graph(n, m, p):
	if m >= n:
		raise nx.NetworkXError("m>=n, choose smaller m")
	if p > 0.99 and m > (n-1)%10:
		raise nx.NetworkXError("p>0.99 and m > (n-1)%10")
	G = nx.DiGraph()
	G.add_nodes_from(range(n))
	G.name="stochastic_block_graph(%s,%s,%s)"%(n,m,p)
	if n == 0:
		return G

	k = math.ceil(n/10)
	classes = list()
	nodes_in_classes = list()
	nodes = list()
	for i in range(0, n, 1):
		classes.append(int(math.floor(i/10)))
		if(i != 0 and i % 10 == 0):
			nodes_in_classes.append(nodes)
			nodes = list()
		nodes.append(i)
	nodes_in_classes.append(nodes)

	for i in range(0, n, 1):
		for j in range(0, m, 1):
			rand_node = i
			while rand_node == i or G.has_edge(i, rand_node):
				if random.random()< p:
					rand_node = random.choice(nodes_in_classes[classes[i]])
				else:
					if k < 2:
						rand_node = random.choice(nodes_in_classes[classes[i]])
					else:
						rand_class = random.randint(0, k-1)
						while(rand_class == classes[i]):
							rand_class = random.randint(0, k-1)
						rand_node = random.choice(nodes_in_classes[rand_class])
			G.add_edge(i, rand_node)
	return G


def create_stochastic_block_graph_model2(n, p_self, p_other):
	G = nx.DiGraph()
	G.add_nodes_from(range(n))
	G.name="stochastic_block_graph(%s,%s,%s)"%(n,p_self,p_other)
	if n == 0:
		return G

	classes = list()
	for i in range(0, n, 1):
		classes.append(int(math.floor(i/10)))
	
	for i in range(0, n, 1):
		for j in range(0, n, 1):
			if i != j:
				p = random.random()
				if (classes[i] == classes[j] and p<p_self) or (classes[i] != classes[j] and p<p_other):
					G.add_edge(i, j)

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


def stochastic_block_model2(number_of_average, p_self, p_other):
	N = np.arange(5, 100, 5)
	x = []
	bow_tie = []
	legend = ["inc", "scc", "outc", "in_tendril", "out_tendril", "tube", "other"]

	for i in range(len(N)):
		n = N[i]
		average = np.array([0,0,0,0,0,0,0])
		for av in range(number_of_average):
			G = create_stochastic_block_graph_model2(n, p_self, p_other)
			graph = Graph(G)
			graph.stats()
			average = average + graph.bow_tie
		average = average / number_of_average
		x.append(n)
		bow_tie.append(average)
	
	plt.plot(x, bow_tie)
	plt.legend(legend, loc="right", shadow=True)
	plt.xlabel('nodes')
	plt.ylabel('percent')
	plt.savefig('stochastic_block_model2.png')

def erdoes_3d_plot(number_of_average):
	N = np.arange(5, 105, 5)
	X = N
	P = arange(0, 0.2, 0.005)
	Y = P
	X, Y = np.meshgrid(X, Y)
	Z = X/2

	for i in range(len(N)):
		n = N[i]
		print n
		p = 0
		for j in range(len(P)):
			if n > 50 and p > 0.1:
				Z[j][i] = 100
				continue
			average = 0
			for av in range(number_of_average):
				G = nx.gnp_random_graph(n, p, None, 1)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average
			p = p + 0.01

	plot_3d(X, Y, Z, '3d_erdoes.png', 'nodes', 'probability of edge creation', 'scc [%]')


def random_graph_3d_plot(number_of_average):
	N = np.arange(5, 55, 5)
	X = N
	M = np.arange(1, 101, 5)
	Y = M
	X, Y = np.meshgrid(X, Y)
	Z = X/2

	for i in range(len(N)):
		n = N[i]
		print n
		for j in range(len(M)):
			m = M[j]
			average = 0
			for av in range(number_of_average):
				G = nx.gnm_random_graph(n, m, None, 1)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average

	plot_3d(X, Y, Z, '3d_random_graph.png', 'nodes', 'edges', 'scc [%]')


def watt_strogatz_3d_plot(p, number_of_average):
	N = np.arange(5, 105, 5)
	K = np.arange(0, 10, 1)
	X = N
	Y = K
	X, Y = np.meshgrid(X, Y)
	Z = X/2

	for i in range(len(N)):
		n = N[i]
		print n
		for j in range(len(K)):
			k = K[j]
			if k>=n/2:
				Z[j][i] = 100
				continue
			average = 0
			for av in range(number_of_average):
				G = watts_strogatz_graph_directed(n, k, p)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average
	
	plot_3d(X, Y, Z, '3d_watt_strognatz.png', 'nodes', 'number of outgoing edges per node', 'scc [%]')


def random_nm_3d_plot(number_of_average):
	N = np.arange(5, 105, 5)
	M = np.arange(0, 10, 1)
	X = N
	Y = M
	X, Y = np.meshgrid(X, Y)
	Z = X/2

	for i in range (len(N)):
		n = N[i]
		print n
		for j in range(len(M)):
			m = M[j]
			if m >= n:
				Z[j][i] = 100
				continue
			average = 0
			for av in range(number_of_average):
				G = create_random_nm_graph(n, m)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average

	plot_3d(X, Y, Z, '3d_random_nm.png', 'nodes', 'number of outgoing edges per node', 'scc [%]')
	

def random_nm_with_preferential_attachment_3d_plot(number_of_average):
	N = np.arange(5, 105, 5)
	M = np.arange(0, 10, 1)
	X = N
	Y = M
	X, Y = np.meshgrid(X, Y)
	Z = X/2

	for i in range (len(N)):
		n = N[i]
		print n
		for j in range(len(M)):
			m = M[j]
			if m >= n:
				Z[j][i] = 100
				continue
			average = 0
			for av in range(number_of_average):
				G = create_random_nm_graph_with_preferential_attachment(n, m) 
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average

	plot_3d(X, Y, Z, '3d_random_nm_with_preferential_attachment.png', 'nodes', 'number of outgoing edges per node', 'scc [%]')


def stochastic_block_3d_plot(p, number_of_average):
	N = np.arange(5, 105, 5)
	M = np.arange(0, 10, 1)
	X = N
	Y = M
	X, Y = np.meshgrid(N, M)
	Z = X/2

	for i in range(len(N)):
		n = N[i]
		print n
		for j in range(len(M)):
			m = M[j]
			if m >= n:
				Z[j][i] = 100
				continue
			average = 0
			for av in range(number_of_average):
				G = create_stochastic_block_graph(n, m, p)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average

	plot_3d(X, Y, Z, '3d_stochastic_block.png', 'nodes', 'number of edges per node', 'scc [%]')


def stochastic_block_model2_3d_plot(n, number_of_average):
	P_self = arange(0, 0.5, 0.05)
	P_other = arange(0, 0.1, 0.01)
	X, Y = np.meshgrid(P_self, P_other)
	Z = X/2

	for i in range(len(P_self)):
		p1 = P_self[i]
		print p1
		for j in range(len(P_other)):
			p2 = P_other[j]
			print p2
			average = 0
			for av in range(number_of_average):
				G = create_stochastic_block_graph_model2(n, p1, p2)
				graph = Graph(G)
				graph.stats()
				average = average + graph.bow_tie[1]
			average = average / number_of_average
			Z[j][i] = average

	plot_3d(X, Y, Z, '3d_stochastic_block.png', 'probability of edge with same class', 'probability of edge with other class', 'scc [%]')


def plot_3d(X, Y, Z, name, label_x, label_y, label_z):
	fig = plt.figure()
	ax = fig.gca(projection = '3d')

	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
	ax.set_zlim(0, 100)
	fig.colorbar(surf, shrink=0.5, aspect=5)
	ax.set_xlabel(label_x)
	ax.set_ylabel(label_y)
	ax.set_zlabel(label_z)
	fig.savefig(name)


print "start"

#parameters
'''n = 500
p_start = 0
p_end = 1
p_step = 0.05
number_of_average = 10
k = 2
m_start = 1
m_end = 5'''
#erdoes(n, p_start, p_end, p_step, number_of_average)
#watts_strogatz(n, k, p_start, p_end, p_step, number_of_average)
#barabasi_albert(n, m_start, m_end, number_of_average)

#erdoes_3d_plot(20)
#watt_strogatz_3d_plot(1, 20)
#random_graph_3d_plot(20)
#random_nm_3d_plot(20)
#random_nm_with_preferential_attachment_3d_plot(20)
#stochastic_block_3d_plot(0.97, 20)
#stochastic_block_model2_3d_plot(100, 20)


stochastic_block_model2(100, 0.15, 0.02)


'''
G = create_stochastic_block_graph_model2(35, 0.6, 0.01)
nx.draw(G)
plt.savefig("test.png")
'''
print "end"
