# Uses python3

import sys
import itertools
import heapq


# this function is one of three operations of the priority queue used to calculate the shortest path in a directed weigthed graph
# read how this function interplays with the other two in distance()
def add_vertex(vertex, priority, pq, entry_finder, counter):
    'Add a new task or update the priority of an existing vertex'
    REMOVED = '<removed-task>'  # placeholder for a removed vertex
    if vertex in entry_finder:
        remove_vertex(vertex, entry_finder)
    count = next(counter)
    entry = [priority, count, vertex]
    entry_finder[vertex] = entry
    heapq.heappush(pq, entry)


# this function is one of three operations of the priority queue used to calculate the shortest path in a directed weigthed graph
# read how this function interplays with the other two in distance()
def remove_vertex(vertex, entry_finder):
    'Mark an existing vertex as REMOVED'
    REMOVED = '<removed-task>'  # placeholder for a removed vertex
    entry = entry_finder.pop(vertex)
    entry[-1] = REMOVED


# this function is one of three operations of the priority queue used to calculate the shortest path in a directed weigthed graph
# read how this function interplays with the other two in distance()
def pop_vertex(pq, entry_finder):
    'Remove and return the lowest priority task'
    REMOVED = '<removed-task>'  # placeholder for a removed task
    while pq:
        priority, count, vertex = heapq.heappop(pq)
        if vertex != REMOVED:
            del entry_finder[vertex]
            return vertex


# this function takes in an adjacent list representation of a directed weighted graph,
# a cost list representing the weights of edges corresponding to the edges in the adjacent list
# vertex s and vertex t.
# the function then calculates and returns the shortest path from s to t. return -1 if there's no such path
# this function implements the Dijstra's algorithm by using a priority queue (pq) to keep track of the vertices while exploring them and applying the edge relaxation procedure
# pq works as follows:
# --- pq stores entries which are lists consisting of vertex v, its priority (ie. dist[v]), and a unique identifier called 'count'
# --- example of an entry: [priority, count, vertex]
# --- pq operates as a binary-min heap with the entry on the top of the queue represents the node with the smallest distance value
# --- after each edge relaxation procedure, distance of one or more vertices might change
# --- so to accommodate this, entry_finder (a dict) will be used to keep track of vertices present in the pq
# --- there are 3 operations that can be performed with pq:
# --- (1) add_vertex: add a new vertex (in a form of an entry) to pq or update the priority of an existing vertex
# --- (2) pop_vertex: pop and return the vertex with the lowest priority from the queue
# --- (3) remove_vertex: when add_vertex() is called to update the priority of an existing vertex, we need to made such update to pq
# ------- since it's difficult to remove an arbitrary entry from pq,
# ------- instead of trying to remove such entry, we will keep it there but update its vertex as 'removed',
# ------- and a new entry representing the same vertex but with an updated priority is added to pq.
# ------- the same entry however does get removed from entry_finder
# ------- that said, pq should have a total of n entries with n = number of vertices + number of updates made
def distance(adj, cost, s, t):
    # initialize the distance (dist) of all vertices to infinite
    # except that distance from vertex s, the starting node, to itself is 0
    # distance value of a vertex (stored in dist) might change after each edge relaxation procedure
    n = len(adj) # number of vertices in the graph
    dist = [float('inf') for _ in range(n)]
    dist[s] = 0

    # create a priority queue, entry_finder, and counter which will be used 'count' in each entry
    pq = []
    entry_finder = {}
    counter = itertools.count()

    # after each edge relaxation procedure, the dist value of one or more vertices might change
    # in that case, an update needs to be made to keep dist accurate
    # n_updates will keeps track of number of updates made
    n_updates = 0

    # add all vertices in graph to priority queue
    for v in range(n):
        add_vertex(v, dist[v], pq, entry_finder, counter)

    # iterate through pq to perform an edge relaxation procedure to all vertices
    while len(pq) > n_updates: # pq should have a total of n entries with n = number of vertices + number of updates made
        # explore the vertex with the lowest priority from pq
        u = pop_vertex(pq, entry_finder)

        # if this vertex has outgoing edges, relax all of its outgoing edges
        # and make updates to priorities if needed
        if len(adj[u]) != 0:
            for i in range(len(adj[u])):
                v = adj[u][i]
                if dist[v] > dist[u] + cost[u][i]:
                    dist[v] = dist[u] + cost[u][i]
                    add_vertex(v, dist[v], pq, entry_finder, counter) # update the priority of v
                    n_updates += 1

    # return -1 if there's no path between s and t
    if dist[t] == float("inf"):
        return -1
    else:
        return dist[t]


# this program reads the input, builds a directed weighted graph from input,
# and return the shortest path from two vertices s and t
# return -1 if there's no path from s to t
# EXAMPLE
# input (and how to interpret input):
# 3 3 (n = number of vertices = 3; m = number of edges = 3)
# 1 2 7 (a directed edge of weight 7 going from 1 to 2)
# 1 3 5 (a directed edge of weight 5 going from 1 to 3)
# 2 3 2 (a directed edge of weight 2 going from 2 to 3)
# 3 2 (calculate and return the distance from vertex 3 to 2)
# output: -1
if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
