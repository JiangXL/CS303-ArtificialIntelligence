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
from random import *
np.set_printoptions(threshold=np.nan)
time_budget = 0
node_num = 0
graph_cp = {} # graph[child] = parent
graph_pc = {} # graph[parent] = child
seeds = [] 
incoming = {} # incoming[node] = incoming degree
debug = 0

def genSeeds(size):
    seeds = []
    cnt = 1
    for i in graph_cp.keys():
        seeds.append(i)
        cnt += 1 
        if cnt > size:
            break
    return seeds

def hill_greedy(size, model):
    ans_seed = []
    cnt = 0
    while not(cnt ==  size):
        cur_seed = ans_seed.copy()
        high = 0
        cur_point = 1
        #point = 1 # initial point
        for node in graph_cp.keys():
            if not (node in ans_seed):
                cur_seed.append(node)
                if model == "IC":
                    new_high = IC(graph_pc, cur_seed, incoming)
                else:
                    new_high = LT(graph_cp, cur_seed, incoming)
                if high < new_high :
                    high = new_high
                    cur_point = node
        ans_seed.append(cur_point)
        cnt += 1
        #print(high)
        #print(cnt, ans_seed)
    return ans_seed

## Generate graph matrix and incoming degree from input txt file
def genGraph(source_file):
    graph_txt = open(source_file, "r")
    header = graph_txt.readline().split()
    global node_num
    node_num = int(header[0])
    #graph_matrix = np.zeros([node_num, node_num])
    node_incoming = {}
    cp_graph = {}
    pc_graph = {}
    edge_num = int(header[1])
    for v in range(1, node_num+1):
        cp_graph[v]=[]
        pc_graph[v]=[]
    for e in range(edge_num):
        edge = graph_txt.readline().split()
        #print(edge[0], int(edge[1]), float(edge[2]))
        (pc_graph[int(edge[0])]).append(int(edge[1]))
        (cp_graph[int(edge[1])]).append(int(edge[0]))
        node_incoming[int(edge[1])] = float(edge[2])
    return cp_graph, pc_graph, node_incoming

def calSpread(model, in_seeds):
    t_start = time.time()
    spread = 0
    cnt = 0
    if model == "LT":
        spread += (LT(graph_cp, in_seeds, incoming))
        t_cost = time.time() - t_start
        #print(t_cost)
        #t_limit = time_budget - 1000*t_cost
        t_limit = time_budget-3
        cnt  += 1
        while (time.time() - t_start) < t_limit:
            #print(t_limit, time.time() - t_start, spread)
            spread += (LT(graph_cp, in_seeds, incoming))
            cnt += 1
    else:
        spread += (IC(graph_pc, in_seeds, incoming))
        t_cost = time.time() - t_start
        #t_limit = time_budget - 10000*t_cost
        t_limit = time_budget-3
        cnt += 1
        while (time.time() - t_start) < t_limit:
            #print(t_limit, time.time() - t_start, spread)
            spread += (IC(graph_pc, in_seeds, incoming))
            cnt += 1
            #spread = IC(graph, seeds, incoming)
    return spread/cnt

## Use Linear Threshold Model
def LT(cp_graph, seeds, node_incoming):
    isActivated = seeds.copy()
    saturation = 0
    # use seeds activate all seed's nodes
    # generate threshold
    #threshold = np.random.rand(node_num) 
    threshold = []
    for i in range(node_num):
        threshold.append( random())
        if threshold[i]==0:
            isActivated.append(i+1)
    lastlen = len(isActivated)
    while (not saturation):
        for node in cp_graph.keys():
            if not(node in isActivated):  # For each node was inactivated do:
                pulse = 0
                for parent in cp_graph[node]:
                    if parent in isActivated:
                        pulse += node_incoming[node]
                if pulse > threshold[node-1]:
                    isActivated.append(node)
        if (lastlen == len(isActivated)):
            saturation = 1
        lastlen= len(isActivated)
    return len(isActivated)

## Using IC Model: the random value larget than incoming
def IC(pc_graph, seeds, node_incoming):
    #print("Cal IC model ")
    spread = 0
    isActivated = seeds.copy()
    lastActivated = seeds.copy()
    equal = 0
    while(not equal):
        newActivated = []
        if debug: print('Lst',lastActivated)
        for node in lastActivated :
            for child in pc_graph[node]: # For each child was inactivated 
                if not (child in isActivated):
                    if node_incoming[child] > random(): 
                        newActivated.append(child)
                        isActivated.append(child) # avoid add element repeatly
        if debug: print("New",newActivated)
        if len(newActivated) == 0 : # No new activated child
            equal = 1
        #isActivated = isActivated + newActivated
        if len(isActivated) == node_num : # All node are activated
            equal = 1
        lastActivated = newActivated.copy()
        if debug: input()
    return len(isActivated)


if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input_file', type=str, default='network.txt')
   parser.add_argument('-k', '--k', type=int)
   parser.add_argument('-m', '--model', type=str, default='IC')
   parser.add_argument('-t', '--time', type=int, default=60)
   args = parser.parse_args()
   input_file = args.input_file
   size = args.k
   model = args.model

   #global time_budget
   time_budget = args.time
   #print(seeds)
   graph_cp, graph_pc, incoming = genGraph(input_file)
   #print(input_file, seed_file, model, time_budget)
   seeds = genSeeds(size)
   seeds = hill_greedy(size, model)
   for seed in seeds:
       print(seed)
   #spread = calSpread(model) 
   #spread = IC(graph_pc, seeds, incoming)
   #spread = LT(graph_cp, seeds, incoming)
   #print(spread)
   #print(graph_cp)
