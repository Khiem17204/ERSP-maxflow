from collections import defaultdict
adj_list = [[0,1,16], [0,2,13], [1,2,10], [2,1,4], [3,2,6],[2,4,14], [1,3,12],[3,2,9],[4,3,7],[4,5,4],[3,5,20]]
#to matrix
#to bfs
graph = defaultdict(list)
for i in adj_list:
    graph[i[0]].append((i[1],i[2]))
def path(start, end):
    stack = [(start,float("inf"), [])]
    visited = set()
    while stack:
        node, capacity, path = stack.pop()
        visited.add(node)
        path += [(node, capacity)]
        if node == end:
            return path
        for neighbors, capacities in graph[node]:
            if neighbors not in visited and capacities > 0:
                stack.append((neighbors,min(capacities,capacity), path))
    return []
def update_residual_graph(path, min_capacity):
    for i in range(len(path) - 1):
        u, _ = path[i]
        v, _ = path[i + 1]
        for j, (neighbor, cap) in enumerate(graph[u]):
            if neighbor == v:
                graph[u][j] = (v, cap - min_capacity)
                break
        edge = False
        for j, (neighbor, cap) in enumerate(graph[v]):
            if neighbor == u:
                graph[v][j] = (u, cap + min_capacity)
                edge = True
                break
        if not edge:
            graph[v].append((u, min_capacity))
max_flow = 0
khiem = path(0,5)
while khiem:
    min_capacity = min(khiem,key= lambda edge: edge[1])[1]
    max_flow += min_capacity
    update_residual_graph(khiem,min_capacity)
    khiem = path(0,5)
print(max_flow)