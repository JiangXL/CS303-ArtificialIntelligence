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

time_budget = 0
node_num = 0
isActivated = np.zeros(node_num) 


## Generate graph matrix and incoming degree from input txt file
def genGraph(source_file):
    graph_txt = open(source_file, "r")
    header = graph_txt.readline()
    global node_num = int(header[0])
    graph_matrix = np.zeros(node_num, node_num)
    node_incoming = np.zeros(node_num)
    edge_num = int(header[1)
    for e in range(edge_num):
        edge = graph_txt.readline()
        source, dest, incoming = int(edge[0]), int(edge[1]), int(edge[2])
        graph_matrix[dest, source] = 1
        graph_incoming[dest] = incoming
    return graph_matrix, incoming

## Use Linear Threshold Model
def LT(graph, seeds):
   saturation = 0
   for seed in seeds: # use seeds activate all seed's nodes
       isActivated[seed-1] = 1
   # generate threshold
   threshold = np.random.rand(node_num)
   
   while(not saturation ): # Todo: add time limit later
       new_isActivated = np.dot(graph, isActivated)*incoming
       if node_num == sum(isActivated) or sum(new_isActivated - isActivated)==0:
           saturation = 1
       else:
           isActivated = new_isActivated
   return sum(isActivated)


## Using IC Model
def IC(graph, seeds):
    return 4

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input_file', type=str, default='network.txt')
   parser.add_argument('-s', '--seed_file', type=str, default='sedds.txt')
   parser.add_argument('-m', '--model', type=str, default='IC')
   parser.add_argument('-t', '--time', type=int, default=60)
   args = parser.parse_args()
   input_file = args.input_file
   seed_file = args.seed_file
   model = args.model

   global time_budget = args.time
   netgraph, incoming = genGraph(input_file)
   print(input_file, seed_file, model, time_budget)

   if model is "LT":
       return LT(netgraph, seeds)
   else :
       return IC(netgraph, seeds)


   
