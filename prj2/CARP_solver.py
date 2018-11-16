#!/bin/python3
'''
Description: CARP
Data       : 20181114
'''
import sys
import numpy as np

# some global constant
infinite = 999999999
capacity = 0

def generateGraph(path):
    graph_txt = open(path, "r")
    #print(graph_txt.readline())
    name = graph_txt.readline()[7:-1]
    vertices = int(graph_txt.readline()[11:-1])
    depot = int(graph_txt.readline()[8:-1])
    required_edges = int(graph_txt.readline()[17:-1])
    no_required_edges = int(graph_txt.readline()[21:-1])
    vehicles = int(graph_txt.readline()[11:-1])
    capacity = int(graph_txt.readline()[11:-1])
    total_cost = int(graph_txt.readline()[31:-1])
    graph_txt.readline() # pass by
    graph_dm = np.zeros([required_edges, required_edges])

    graph_ct = np.zeros([required_edges +no_required_edges, required_edges + no_required_edges])

    for i in range(required_edges + no_required_edges):
        line = graph_txt.readline().split()
        if int(line[3]) > 0 :
            graph_dm[(int(line[0]), int(line[1]))] = int(line[3])
        graph_ct[(int(line[0]), int(line[1]))] = int(line[2])
    return graph_dm, graph_ct

# cal dijkstra distance
def dijkstra(graph, source):
    print("find shortest distance")
    Q = []
    dist = []
    prev = []
    for vertex in g:
        pre;
    print(S)
    U = {}
    return dist, prev

# return a martix with min distance betweent two points
def genDijkstraDist(graph_dm, graph_ct):
    shortestDist={}  # shortest distance and path betweent required edge
    dist, prev = dijkstra(graph_ct, pivot)
    print("dict of shortest distance")
    return shortestDist

# sub rule to choose candidate point
def better(now, pre):
    print("choose better point ")
    np.random.seed(seed)
    return np.random.random() > 0.5

# usine path Scanning to choose suitable point
def pathScan(required_graph, cost_graph, capacity, shortest_dist):
    print("path-Scanning")
    R = [] # successive routes
    #free = required_graph  # copy required_edges from graph
    free = [(1,1)] # should be two direction
    k = 0 # required_edges label
    d = 0 # shortest distance away from source(initialize at source)
    while( len(free) > 0 ) : # for remaining required edge
        k = k + 1  # car number
        R_k = []   # this car route set
        load_k = 0 # this car load
        cost_k = 0 # this car cost
        i = 1      # each car start from depot
        while(len(free) > 0  and not(d == infinite)): #
            print("Searching inside required graph")
            d = infinite    # reset distance
            u_candidate = 0 # reset candidate edge
            for u in free.keys() and (cost_k + load_k + required_graph[u] < capacity):
                if shortest_dist[i,u[0]] < d : # closest path  betweent 2 vertex
                    d = shortest_dist[i, u[0]]
                    u_candidate = u
                elif (shortest_dist[i, u[0]] == d) and better(u, u_candidate):
                    u_candidate = u
            R_k.append(u_candidate) ## TODO: should add no no_required_edges
            load_k = load_k + required_edges(u_candidate) # update load
            cost_k = cost_k + d + cost_graph[u_candidate]# update cost
            i = u_candidate[-1] # update u_candidate end vertex to new start
            free.remove((u_candidate[-1], u_candidate[0])) # opposite egde
            free.remove(u_candidate) # pop chosen edge from required_edges set
        R.append(R_k) # add each route together after car is full or no require
        cost_k = cost_k + shortest_dist((i,1)) # add back home distance
        print("Dealing with required_edges:", k)
    return R, cost_k

# formatlize output string
def s_format(s):
    s_print = []
    for p in s:
        s_print.append(0)
        s_print.extend(p)
        s_print.append(0)
    return s_print

# main function
if __name__ == "__main__" :
    time_limit = 60
    file_name = 'gdb10.dat'
    seed = 1

    if len(sys.argv) == 6:
        file_name = sys.argv[1]
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])
    # Generate graph form data file
    graph_demand, graph_cost = generateGraph(file_name)
    # Generate shortest distance of two vertex
    shortest_dist = genDijkstraDist(graph_demand, graph_cost)
    # Return final decision
    result_path, final_cost = pathScan(graph_demand, graph_cost, capacity, shortest_dist)

    print("\nOutput result:")
    s = [[(1,2),(2,3),(3,8),(8,12),(12,10),(10,9),(9,1)],[(1,4),(4,2),(2,7),(7,4),(4,6),(6,11)],[(1,10),(12,11),(11,4),(4,3),(3,9),(9,8),(8,1)],[(1,11),(6,5),(5,2),(7,5),(5,1)]]
    cost = 275
    print("s", (",".join(str(d) for d in s_format(s))).replace(" ", ""))
    print("q", final_cost)
