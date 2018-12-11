#!/bin/python3
'''
Description: Return value of the estimated influence spread with given graph
             and seeds
Input : -i <social network> -s <seed set> -m <diffusion model> -t <time budget> 
Output: the value of the estimated influence spread

| Version | Commit
|   0.1   |   

matrix:
      in1 in2 ... inn
out1 [              ]
out2 [              ]
.    [              ]
outn [              ]
'''
import sys
import os
import argparse
import numpy as np
import time
np.set_printoptions(threshold=np.nan)
time_budget = 0
node_num = 0
graph = 0
seeds = 0
incoming = 0

def genSeeds(seed_file):
    seeds = []
    with open(seed_file) as f:
        for line in f:
            seeds.append(int(line))
    return seeds

## Generate graph matrix and incoming degree from input txt file
def genGraph(source_file):
    graph_txt = open(source_file, "r")
    header = graph_txt.readline().split()
    global node_num
    node_num = int(header[0])
    graph_matrix = np.zeros([node_num, node_num])
    node_incoming = np.zeros([node_num, 1])
    edge_num = int(header[1])
    for e in range(edge_num):
        edge = graph_txt.readline().split()
        #print(edge[0], int(edge[1]), float(edge[2]))
        source, dest, incoming = int(edge[0])-1,int(edge[1])-1,float(edge[2])
        graph_matrix[dest, source] = 1
        node_incoming[dest, 0] = incoming
    return graph_matrix, node_incoming

def calSpread(model):
    t_start = time.time()
    spread = 0
    if model == "LT":
        spread = LT(graph, seeds, incoming)
        t_cost = time.time() - t_start
        t_limit = time_budget - 10*t_cost
        while (time.time() - t_start) < t_limit:
            print(t_limit, time.time() - t_start, spread)
            spread = (LT(graph, seeds, incoming) + spread)/2
    else:
        spread = IC(graph, seeds, incoming)
        t_cost = time.time() - t_start
        t_limit = time_budget - 10*t_cost
        while (time.time() - t_start) < t_limit:
            #print(t_limit, time.time() - t_start, spread)
            spread = (IC(graph, seeds, incoming) + spread)/2
            #spread = IC(graph, seeds, incoming)
    return spread

# Use Linear Threshold Model
def LT(graph, seeds, node_incoming):
    isActivated = np.zeros([node_num, 1]) > 0
    saturation = 0
    for seed in seeds: # use seeds activate all seed's nodes
        isActivated[seed-1][0] = 1
    # generate threshold
    threshold = np.random.rand(node_num,1) 
    #print(node_incoming)
    while(not saturation ): # Todo: add time limit later
        #print("1", (node_incoming*isActivated).shape)
        #print("2", ((1-isActivated)*graph).shape)
        newActivated=(np.dot((1-isActivated)*graph,(node_incoming*isActivated)))>threshold
        #print(newActivated.shape)
        if sum(newActivated)==False : #node_num==sum(isActivated):
            saturation = 1
        else:
            isActivated = isActivated + newActivated 
        #print(isActivated)
    return sum(isActivated)


## Using IC Model: the random value larget than incoming
def IC(graph, seeds, node_incoming):
    #print("Cal IC model ")
    spread = 0
    isActivated = np.zeros(node_num) > 0
    lastActivated = np.zeros(node_num) > 0
    for seed in seeds:
        isActivated[seed-1] = 1
        lastActivated[seed -1] = 1  # From seeds
    equal = 0
    #print("Act", isActivated)
    while(not equal):
        radm = np.random.rand(node_num, node_num)
        #print("Lst", lastActivated)
        #print("0", ((graph*lastActivated)[:,13]))
        #print("1", (graph*lastActivated*node_incoming)[:,13])
        #print("2", (graph*lastActivated*node_incoming)[6,:])
        newActivated=sum(((graph*lastActivated*node_incoming) > radm).T) > 0
        #newActivated=(graph*lastActivated*node_incoming > radm) #> 0
        #print("New", newActivated)
        isActivated = (isActivated + newActivated ) > 0
        #print("Act", isActivated)
        if (sum(newActivated)==False): #or(sum(isActivated)==node_num):
            equal = 1
        lastActivated = newActivated^((newActivated+isActivated)>1)
    return sum(isActivated)

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input_file', type=str, default='network.txt')
   parser.add_argument('-s', '--seed_file', type=str, default='sedds.txt')
   parser.add_argument('-m', '--model', type=str, default='IC')
   parser.add_argument('-t', '--time', type=int, default=600)
   args = parser.parse_args()
   input_file = args.input_file
   seed_file = args.seed_file
   model = args.model

   #global time_budget
   time_budget = args.time
   seeds = genSeeds(seed_file)
   #print(seeds)
   graph, incoming = genGraph(input_file)
   #print(input_file, seed_file, model, time_budget)

   spread = calSpread(model) 
   #spread = IC(graph, seeds, incoming)
   #spread = LT(graph, seeds, incoming)
   print(int(spread))


   
