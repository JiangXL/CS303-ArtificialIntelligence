#!/bin/python3
'''
Description: CARP
Data       : 20181118
Version    : v1.0 Path Scanning work 0.156s
'''
import sys
import numpy as np

# Some global constant
infinity = 999999999
capacity = 0
undefined = 0
debug = 0
graph_dm = {}  # graph_dm = {(node-node):(vertex's cost)}
graph_ct = {}  # graph_ct = {(node-node):(vertex's demand)}

def generateGraph(path):
    graph_txt = open(path, "r")
    #print(graph_txt.readline())
    name = graph_txt.readline()[7:-1]
    vertices = int(graph_txt.readline()[11:-1])
    depot = int(graph_txt.readline()[8:-1])
    required_edges = int(graph_txt.readline()[17:-1])
    no_required_edges = int(graph_txt.readline()[21:-1])
    vehicles = int(graph_txt.readline()[11:-1])
    global capacity
    capacity = int(graph_txt.readline()[11:-1])
    total_cost = int(graph_txt.readline()[31:-1])
    graph_txt.readline() # pass by
    #graph_dm = np.zeros([required_edges, required_edges])
    #graph_ct = np.zeros([required_edges +no_required_edges, required_edges + no_required_edges])
    global graph_dm
    global graph_ct
    for i in range(required_edges + no_required_edges):
        line = graph_txt.readline().split()
        if int(line[3]) > 0 :
            graph_dm[(int(line[0]), int(line[1]))] = int(line[3])
            graph_dm[(int(line[1]), int(line[0]))] = int(line[3])
        graph_ct[(int(line[0]), int(line[1]))] = int(line[2])
        graph_ct[(int(line[1]), int(line[0]))] = int(line[2])

## search the shortest distance away from souce
def dijkstra(source):
    #print("find shortest distance")
    Q = []
    dist = [] # distance
    prev = [] # previous path
    for edge in graph_ct.keys():
        vertex = edge[0]
        dist.append(infinity)  # unknow distance from source to vertex
        prev.append(undefined) # previous node in optimal path from source
        # prev[source] = undefined
        Q.append(vertex)
    dist[source]= 0 # distance from source to source
    #print('dist', len(dist))

    while len(Q) > 0 :
        shortest_distance = infinity
        for vertex in Q: # find clost vertex
            if dist[vertex] <= shortest_distance:
                u = vertex
                shortest_distance = dist[vertex]
        Q.remove(u)
        neighbor = []
        for edge in graph_ct.keys():
            if edge[0] == u and edge[1] in Q:
                neighbor.append(edge[1])
        for u_nb in neighbor:
            alt = dist[u] + graph_ct[(u, u_nb)]
            if alt < dist[u_nb]:
                dist[u_nb] = alt
                prev[u_nb] = u
    return dist, prev

# Return a martix with min distance betweent two points
def genDijkstraDist():
    shortestDist={}  # ShortestDist={(vertex1,vertex2):(shortestDist, path[])}
    for source in graph_dm:
        pivot = source[0]
        dist, prev = dijkstra(pivot)
        shortestDist_pivot={}
        for target_edge in graph_dm:
            target_vertex = target_edge[1]
            shortestPath=[]
            k = target_vertex # Construct shortest path with stack S
            #while not(prev[k] is undefined) :
            #    shortestPath.insert(0,(prev[k],k))
            #    k = prev[k]
            shortestDist[(pivot, target_vertex)]=(dist[target_vertex], shortestPath)
    return shortestDist

# Subrule to choose candidate point
def better(now, pre):
    #print("choose better point ")
    np.random.seed(seed)
    if(graph_dm[now] < graph_dm[pre]):
        return True
    return False

# using path Scanning to choose suitable point
def pathScan(shortest_dist):
    if debug: print("Path-Scanning")
    R = []      # successive routes
    free = []   # copy required_edges from graph
    for each in graph_dm.keys():
        free.append(each)
    k = 0       # car number(start from 1)
    cost = 0    # total cost to finish all required edge
    while( len(free) > 0 ) : # if still remain required edge, new car
        k = k + 1  # car number
        R_k = []   # this car route set
        cost_k = 0 # car k cost
        load_k = 0 # this car load
        i = 1      # each car start from depot
        if debug: print("\n\nCar:", k, " Remaining require(%d):"%len(free), free)
        if debug: print("Searching in remaining required edge")
        while(len(free) > 0): # choose one or more required edge to carry
            d = infinity      # reset shortest distance away source
            e_candidate = -1  # reset candidate edge
            for e in free:    # choose one required edge
                if (load_k + graph_dm[e] <= capacity):
                    dist_now = shortest_dist[i, e[0]][0]
                    if dist_now < d : # closest path  betweent 2 vertex
                        d = dist_now
                        e_candidate = e
                    elif (dist_now == d) and better(e, e_candidate):
                        e_candidate = e
            if(d == infinity): break # equal to : car is full
            #for each in shortest_dist[i, e_candidate[0]][1]: # add middle path
                #R_k.append(each)
            R_k.append(e_candidate)
            load_k = load_k + graph_dm[e_candidate] # update car k's load
            cost_k = cost_k + d + graph_ct[e_candidate] # update car k's cost
            i = e_candidate[-1] # update u_candidate end vertex to new start
            if debug: print('Choose ',e_candidate,'than',e,'Load:', load_k)
            free.remove(e_candidate) # pop chosen edge from required_edges set
            free.remove((e_candidate[-1], e_candidate[0])) # opposite egde
        cost_k = cost_k + shortest_dist[(i,1)][0] # add back home distance
        #if debug:
            #print("Backing home", shortest_dist[(i,1)][1], 'Cost',shortest_dist[(i,1)][0])
        R.append(R_k) # add each route together after car is full or no require
        cost = cost + cost_k
    return R, cost

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
    generateGraph(file_name)
    # Generate shortest distance of two vertex
    shortest_dist = genDijkstraDist()
    #print(shortest_dist)
    # Return final decision
    result_path, final_cost = pathScan(shortest_dist)

    #print("\nOutput result:")
    print("s", (",".join(str(d) for d in s_format(result_path))).replace(" ", ""))
    print("q", final_cost)
