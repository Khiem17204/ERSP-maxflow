import networkx as nx
import random as rd
import numpy as np
import time as t


def load_data(file):
    graph = nx.Graph()
    data = open(file, "r").readlines()
    for line in data:
        temp = line.split()
        graph.add_edge(int(temp[1]), int(temp[2]), capacity=1.0)
    return graph

def get_connected_component(graph, terminal):
    return nx.node_connected_component(graph, terminal)

def iso_cut(graph, t_set):
    # isolate group cut
    connected_component, minimum_cut_group = isolating_group(graph, t_set)
    # find minimum cut for each component
    minimum_cut = component_minimum_cut(graph, t_set, connected_component)
    for i in range(len(minimum_cut)):
        minimum_cut[i] = min(minimum_cut[i], minimum_cut_group)
    return minimum_cut

# return graph after isolating group cut, and minimum cut value
def isolating_group(g, t_set):
    connected_component = []
    graph = g.copy()
    # arbitrary source and sink
    s = 28000
    t = 30000
    # return minimum cut value
    minimum_cut = 0
    for bit in range(6):
        set_0 = []
        set_1 = []
        for terminal in t_set:
            if terminal & (1<<bit):
                set_1.append(terminal)
            else:
                set_0.append(terminal)
        # perform group cut
        for i in set_0:
            graph.add_edge(s, i)
        for i in set_1:
            graph.add_edge(t, i)
        # remove edge of minimum cut from graph
        cut_value, partition = nx.minimum_cut(graph, s, t)
        minimum_cut += cut_value
        cut_edges = set()
        node_set_1, node_set_2 = partition
        for u in node_set_1:
            for v in node_set_2:
                if graph.has_edge(u, v):
                    cut_edges.add((u,v))
        for u, v in cut_edges:
            graph.remove_edge(u, v)
        
        # remove added edge in the same component
        for i in set_0:
            graph.remove_edge(s, i)
        for i in set_1:
            graph.remove_edge(t, i)
    for terminal in t_set:
        connected_component.append(get_connected_component(graph, terminal)) 
    return connected_component, minimum_cut

# using graph after isolating group cut, find final minimum cut for each component
def component_minimum_cut(graph, t_set, connected_component):
    # contracting T/U_v to single node with U_v be the connected component of terminal v
    minimum_cut = [100000] * len(t_set)
    for i in range(len(t_set)):
        component = connected_component[i]
        # contracting node outside component into 1 node: new_node
        new_node = 100000 + i
        H = graph.copy()
        H.add_node(new_node)

        for node in component:
            for neighbor in graph.neighbors(node):
                if neighbor not in component:
                    H.add_edge(new_node, node, capacity=1.0)
        # call maxflow of (v, new_node) to find minimum cut
        cut_value, _ = nx.minimum_cut(H, t_set[i], new_node)
        minimum_cut[i] = cut_value
    return minimum_cut
    


if __name__=="__main__":
    graph = load_data('road.txt')
    # test on 100 terminal, need 7 bits to represent all 100 terminals
    
    start_time = t.time()
    res = iso_cut(graph, [rd.randint(1, 20000) for i in range(100)])
    end_time = t.time()
    print(end_time-start_time)
    print(res)
