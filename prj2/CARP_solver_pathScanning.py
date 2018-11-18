#!/bin/python3
'''
Description: CARP
Data       : 20181118
'''
import sys
import numpy as np

# some global constant
infinity = 999999999
capacity = 0
undefined = 0
debug = 0

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
    #graph_dm = np.zeros([required_edges, required_edges])
    graph_dm ={} # graph={(node-node):(cost, demand)}
    #graph_ct = np.zeros([required_edges +no_required_edges, required_edges + no_required_edges])
    graph_ct = {}
    for i in range(required_edges + no_required_edges):
        line = graph_txt.readline().split()
        if int(line[3]) > 0 :
            graph_dm[(int(line[0]), int(line[1]))] = int(line[3])
            graph_dm[(int(line[1]), int(line[0]))] = int(line[3])
        graph_ct[(int(line[0]), int(line[1]))] = int(line[2])
        graph_ct[(int(line[1]), int(line[0]))] = int(line[2])
    return graph_dm, graph_ct, capacity

## search the shortest distance away from souce
def dijkstra(dm_graph, cost_graph, source):
    #print("find shortest distance")
    Q = []
    dist = [] # distance
    prev = [] # previous path
    for edge in cost_graph.keys():
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
        for edge in cost_graph.keys():
            if edge[0] == u and edge[1] in Q:
                neighbor.append(edge[1])
        for u_nb in neighbor:
            alt = dist[u] + cost_graph[(u, u_nb)]
            if alt < dist[u_nb]:
                dist[u_nb] = alt
                prev[u_nb] = u
    return dist, prev

# Return a martix with min distance betweent two points
def genDijkstraDist(dm_graph, cost_graph):
    shortestDist={}  # ShortestDist={(vertex1,vertex2):(shortestDist, path[])}
    for source in dm_graph:
        pivot = source[0]
        dist, prev = dijkstra(dm_graph, cost_graph, pivot)
        shortestDist_pivot={}
        for target_edge in dm_graph:
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
    return np.random.random() > 0.5

# using path Scanning to choose suitable point
def pathScan(required_graph, cost_graph, shortest_dist):
    if debug: print("Path-Scanning")
    R = []      # successive routes
    free = []   # copy required_edges from graph
    for each in required_graph.keys():
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
                if (load_k + required_graph[e] <= capacity):
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
            load_k = load_k + required_graph[e_candidate] # update car k's load
            cost_k = cost_k + d + cost_graph[e_candidate] # update car k's cost
            i = e_candidate[-1] # update u_candidate end vertex to new start
            if debug: print('Choose ',e_candidate,'than',e,'Load:', load_k)
            free.remove(e_candidate) # pop chosen edge from required_edges set
            free.remove((e_candidate[-1], e_candidate[0])) # opposite egde
        cost_k = cost_k + shortest_dist[(i,1)][0] # add back home distance
        #if debug:
            #print("Backing home", shortest_dist[(i,1)][1], 'Cost',shortest_dist[(i,1)][0])
        #for each in shortest_dist[i, 1][1]:       # add back home path
        #    R_k.append(each)   # issue: avoid to walk with required
            # back as
        R_k_back = R_k.copy()
        R_k_back.reverse()
        #print(R_k)
        for cnt in range(len(R_k_back)):
            R_k_back[cnt]=(R_k_back[cnt][-1],R_k_back[cnt][0])
        #R_k = R_k + R_k_back
        #print(R_k_back)
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
    #print(file_name)
    graph_demand, graph_cost, capacity = generateGraph(file_name)
    # Generate shortest distance of two vertex
    shortest_dist = genDijkstraDist(graph_demand, graph_cost)
    #print(shortest_dist)
    # Return final decision
    result_path, final_cost = pathScan(graph_demand, graph_cost, shortest_dist)

    #print("\nOutput result:")
    #s = [[(1,2),(2,3),(3,8),(8,12),(12,10),(10,9),(9,1)],[(1,4),(4,2),(2,7),(7,4),(4,6),(6,11)],[(1,10),(12,11),(11,4),(4,3),(3,9),(9,8),(8,1)],[(1,11),(6,5),(5,2),(7,5),(5,1)]]
    #print("s", (",".join(str(d) for d in s_format(s))).replace(" ", ""))
    print("s", (",".join(str(d) for d in s_format(result_path))).replace(" ", ""))
    print("q", final_cost)
