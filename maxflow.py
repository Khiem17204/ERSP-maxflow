from collections import deque 
adj_list = [{} for _ in range(180000)]

data = open("road-170k.txt","r").readlines()
for line in data:
    temp = line.split()
    adj_list[int(temp[1])][int(temp[2])] = 1
    adj_list[int(temp[2])][int(temp[1])] = 1
def max_flow(adj_list,start, end):
    def path(start, end):
        queue = deque([(start,float("inf"), [])])
        visited = [False]*180000
        while queue:
            node, capacity, path = queue.popleft()
            visited[node] = True
            new_path = path + [(node, capacity)]
            if node == end: 
                return (new_path,capacity)
            for neighbors in adj_list[node]:
                if not visited[neighbors] and adj_list[node][neighbors] > 0:
                    queue.append((neighbors,min(adj_list[node][neighbors],capacity), new_path))
        return []

    def update_residual_graph(path, min_capacity):
        for i in range(len(path) - 1):
            u, _ = path[i]
            v, _ = path[i + 1]
            adj_list[u][v] -= min_capacity
            adj_list[v][u] += min_capacity
    maxflow = 0
    khiem, min_capacity = path(start,end)
    while khiem:
        maxflow += min_capacity
        update_residual_graph(khiem,min_capacity)
        if not path(start,end):
            return maxflow
        else:
            khiem, min_capacity = path(start,end)
print(max_flow(adj_list,0,50000))