from GraphBase import genGraph
from collections import Counter, deque

def dfs(node, visited):
    if not visited[node]:
        visited[node] = 1
        print(node.val)
        for child in node.children:
            dfs(child, visited)

def bfs(start):
    q = deque([start])
    visited = Counter()
    while(q):
        node = q.popleft()        
        if not visited[node]:
            visited[node] = 1
            print(node.val)
            for child in node.children:
                q.append(child)
    

    

visited = Counter()
graph = genGraph("1:2,3 2:1 3:4 4:5")
node = list(graph.keys())[0]
dfs(node, visited)
# bfs(node)