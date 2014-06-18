import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from main import Graph

in_edges = []
out_edges = []
G = nx.DiGraph()

def get_edges():
	global in_edges
	global out_edges

	edges = G.in_edges()
	number = 0
	u = list()
	v = list()
	in_list = list()
	for edge in edges:
		if number == edge[1]:
			in_list.append(edge[0])
		else:
			if in_list:
				u.append(number)
				v.append(in_list)
			number = edge[1]
			in_list = list()
			in_list.append(edge[0])
	u.append(number)
	v.append(in_list)
	in_edges = dict(zip(u,v))

	edges = G.out_edges()
	number = 0
	u = list()
	v = list()
	out_list = list()
	for edge in edges:
		if number == edge[0]:
			out_list.append(edge[1])
		else:
			if out_list:
				u.append(number)
				v.append(out_list)
			number = edge[0]
			out_list = list()
			out_list.append(edge[1])
	u.append(number)
	v.append(out_list)
	out_edges = dict(zip(u,v))




def search2(start_node, result, direction = 0):

	if start_node in result:
		return result
	result.append(start_node)
	try:
		if direction == 0:
			nodes = in_edges[start_node]
		else:
			nodes = out_edges[start_node]
	except:
		return result
	for node in nodes:
		result = search(node, result, direction)
	return result


def search(start_node, node_list, direction = 0):
	result = []
	count = 0
	result.append(start_node)
	while count < len(result):
		start_node = result[count]
		if start_node not in node_list:
			count = count + 1
			continue
		try:
			if direction == 0:
				nodes = in_edges[start_node]
			else:
				nodes = out_edges[start_node]
		except:
			count = count + 1
			continue
		for node in nodes:
			if node not in result:
				result.append(node)
		count = count + 1
	return result

def stats():
	number_of_nodes = G.number_of_nodes()
	list_of_nodes = G.nodes()
	len_scc = 0
	scc = []

	while len(list_of_nodes) > len_scc:
		rand_node = random.choice(list_of_nodes)
		in_nodes = search(rand_node, list_of_nodes, 0)
		out_nodes = search(rand_node, list_of_nodes, 1)
		group = list(set(in_nodes).intersection(set(out_nodes)))
		if len(group) > len_scc:
			len_scc = len(group)
			scc = group
		list_of_nodes = list(set(list_of_nodes).difference(set(group)))

	in_scc = search(scc[0], G.nodes(), 0)
	in_scc = list(set(in_scc).difference(set(scc)))
	len_in = len(in_scc)
	out_scc = search(scc[0], G.nodes(), 1)
	out_scc = list(set(out_scc).difference(set(scc)))
	len_out = len(out_scc)

	return [100.*len_in/number_of_nodes, 100.*len_scc/number_of_nodes, 100.*len_out/number_of_nodes]


def BowTie(Graph):
	global G
	G = Graph
	get_edges()
	bow_tie = stats()
	return bow_tie
