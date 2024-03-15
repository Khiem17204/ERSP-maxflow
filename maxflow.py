import networkx as nx
import random as rd
import numpy as np


def load_data(file):
    graph = nx.DiGraph()
    data = open(file, "r").readlines()
    for line in data:
        temp = line.split()
        graph.add_edge(int(temp[1]), int(temp[2]), capacity=1.0)
        graph.add_edge(int(temp[2]), int(temp[1]), capacity=1.0)
    return graph

def iso_cut(graph, s, t_set):
    t = 23000
    cut_values = 0
    cut = set()
    for bit in range(16):
        #check bit of terminal sets
        set_0 = []
        set_1 = []
        source = (s>>bit)&1
        for terminals in t_set:
            if (terminals>>bit)&1:
                set_1.append(terminals)
            else:
                set_0.append(terminals)
        
        #add terminal set to t with infinity capacity
        if source:
            for i in set_1:
                graph.add_edge(s, i)
                graph.add_edge(i, s)
            for i in set_0:
                graph.add_edge(t, i)
                graph.add_edge(i, t)
            # set next components
            t_set = set_1
        else:
            for i in set_0:
                graph.add_edge(s, i)
                graph.add_edge(i, s)
            for i in set_1:
                graph.add_edge(t, i)
                graph.add_edge(i, t)
            t_set = set_0
        
        #remove edge of minimum cut from graph
        cut_value, partition = nx.minimum_cut(graph, s, t)
        cut_values += cut_value
        cut_edges = set()
        node_set_1, node_set_2 = partition

        for u in node_set_1:
            for v in node_set_2:
                if graph.has_edge(u, v):
                    cut_edges.add((u,v))
                    cut.add((u,v))
        for u, v in cut_edges:
            graph.remove_edge(u, v)
        
        # remove added edge in the same component
        if source:
            for i in set_1:
                graph.remove_edge(s, i)
                graph.remove_edge(i, s)
        else:
            for i in set_0:
                graph.remove_edge(s,i)
                graph.remove_edge(i,s)
    
    return cut, cut_values



if __name__=="__main__":
    graph = load_data('road.txt')
    print(iso_cut(graph, 100, [1,2,532,351,1532,1255,122]))