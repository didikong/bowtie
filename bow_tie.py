import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from main import Graph

class BowTie(nx.DiGraph):

	def get_edges(self):
		edges = self.in_edges()
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
		self.in_edg = dict(zip(u,v))

		edges = self.out_edges()
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
		self.out_edg = dict(zip(u,v))


	def search(self, start_node, node_set, direction = 0):
		result = set()
		todo = []
		count = 0
		result.add(start_node)
		todo.append(start_node)
		while count < len(result):
			start_node = todo[count]
			if start_node not in node_set:
				count = count + 1
				continue
			try:
				if direction == 0:
					nodes = self.in_edg[start_node]
				else:
					nodes = self.out_edg[start_node]
			except:
				count = count + 1
				continue
			for node in nodes:
				if node not in result:
					result.add(node)
					todo.append(node)
			count = count + 1
		return result

	def getTendrilsAndTubes(self):
		in_tendrils = set()
		out_tendrils = set()
		tubes = set()
		other = set()
		all_nodes = self.nodes()
		unknown = set(all_nodes).difference(self.scc).difference(self.in_scc).difference(self.out_scc)
		for node in unknown:
			bool_in = 0
			bool_out = 0
			incoming = self.search(node, all_nodes, 0)
			if len(incoming) > 1:
				for in_node in incoming:
					if in_node in self.in_scc:
						bool_in = 1
		
			outgoing = self.search(node, all_nodes, 1)
			if len(outgoing) > 1:
				for out_node in outgoing:
					if out_node in self.out_scc:
						bool_out = 1
			if bool_in == 1 and bool_out == 1:
				tubes.add(node)
				continue
			elif bool_in == 1:
				in_tendrils.add(node)
				continue
			elif bool_out == 1:
				out_tendrils.add(node)
				continue
			else:
				other.add(node)
			self.in_tendrils = in_tendrils
			self.out_tendrils = out_tendrils
			self.tubes = tubes
			self.other = other
		return [100.*len(in_tendrils)/len(all_nodes), 100.*len(out_tendrils)/len(all_nodes), 100.*len(tubes)/len(all_nodes) , 100.*len(other)/len(all_nodes)]


	def getData(self):
		scc = set()
		number_of_nodes = self.number_of_nodes()
		set_of_nodes = set(self.nodes())
		len_scc = 0

		while len(set_of_nodes) > len_scc:
			print len(set_of_nodes)
			rand_node = random.sample(set_of_nodes, 1)[0]
			in_nodes = self.search(rand_node, set_of_nodes, 0)
			out_nodes = self.search(rand_node, set_of_nodes, 1)
			group = in_nodes.intersection(out_nodes)
			if len(group) > len_scc:
				len_scc = len(group)
				scc = group
			set_of_nodes = set_of_nodes.difference(group)

		rand_node = random.sample(scc, 1)[0]
		in_scc = self.search(rand_node, set(self.nodes()), 0)
		in_scc = in_scc.difference(scc)
		len_in = len(in_scc)
		out_scc = self.search(rand_node, set(self.nodes()), 1)
		out_scc = out_scc.difference(scc)
		len_out = len(out_scc)

		self.in_scc = in_scc
		self.scc = scc
		self.out_scc = out_scc

		rest = self.getTendrilsAndTubes()

		return [100.*len_in/number_of_nodes, 100.*len_scc/number_of_nodes, 100.*len_out/number_of_nodes]+ rest



	def __init__(self, graph=None):
		super(BowTie, self).__init__()
		self.lc_asp, self.lc_diam = 0, 0
		self.bow_tie, self.bow_tie_dict, self.bow_tie_changes = 0, 0, []
		self.in_edg, self.out_edg  = [], []
		self.in_scc, self.scc, self.out_scc, self.in_tendrils = set(), set(), set(), set()
		self.out_tendrils, self.tubes, self.other = set(), set(), set()
		if graph:
			self.add_nodes_from(graph)
			self.add_edges_from(graph.edges())
		self.G = graph
	
	def stats(self, prev_bow_tie_dict=None):
		self.get_edges()
		self.bow_tie = self.getData()
		zipped = zip(['inc', 'scc', 'outc', 'in_tendril', 'out_tendril',
			'tube', 'other'], range(7))
		c2a = {c: i for c, i in zipped}
		self.bow_tie_dict = {}
		for i, c in enumerate([self.in_scc, self.scc, self.out_scc, self.in_tendrils, self.out_tendrils, self.tubes,
			self.other]):
			for n in c:
				self.bow_tie_dict[n] = i
		if prev_bow_tie_dict:
			self.bow_tie_changes = np.zeros((len(c2a), len(c2a)))
			for n in self:
				if n >= len(prev_bow_tie_dict):
					self.bow_tie_changes[prev_bow_tie_dict[n],
							self.bow_tie_dict[n]] += 1
			self.bow_tie_changes /= len(self)
