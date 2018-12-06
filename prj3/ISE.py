#!/bin/python3
'''
Description: Return value of the estimated influence spread with given graph
             and seeds
Input : -i <social network> -s <seed set> -m <diffusion model> -t <time budget> 
Output: the value of the estimated influence spread

| Version | Commit
|   0.1   |   

'''
import sys
import os
import argparse
import numpy

time_budget = 0
graph = {} # [node] = outcome out
nodeInfo = {} # [node] = (is active, indegree)

def LT(graph, seeds):
   actived = []
   threshold = {}
   for node in graph:
       threshold[node] = numpy.random() 

   saturation = 0
   
   while(not saturation ): # Todo: add time limit later
       for seed in seeds:
           for neighbour in graph:
               
   return len(actived)

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
   print(input_file, seed_file, model, time_budget)

   
