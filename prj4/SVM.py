# -*- coding: utf-8 -*-
"""
Using SVM to classify dataset
| Version | Commit
|   0.1   | Finish first version based on slide

"""

import time
import sys
import argparse
import os
import numpy as np


## Load and  prepare train data
def init(train_txt, tie_limit):
    data = []
    with open(train_txt) as train_data:
         for line in  train_data:
             #print(line)
             data.append([float(l) for l in line.split()])
             #data.append(line)
             print(data[-1])
    x = np.array(data)
    y = (x[:, -1]).astype(int)
    x[:, -1] = 1
    w = np.zeros(len(x[1,:]))
    cycle = 1000
    return x, y, w, cycle
    
def get_loss(xi, yi, w):
    loss = max(0, 1-yi*np.dot(xi, w))
    return loss

## update weight
def cal_sgd(xi, yi, w, ratio, learn_speed):
    # update down hilll speed
    if yi*np.dot(xi,w) < 1:
        w_next = w - ratio*(learn_speed*w - yi*xi)
    else:
        w_next = w - ratio*learn_speed*yi
    return w_next

## Training fucntion
def train(x, y, w, cnt, learn_speed):
    # Repeat cnt time
    log = open("learn_curve.log", "w")
    t = 0
    for epoch in range(cnt):
        randomize =  np.arange(len(x))
        np.random.shuffle(randomize)
        x = x[randomize]
        y = y[randomize]
        loss = 0
        # update ratio of learn_speed each time
        #if epoch < cnt/2:
        #    ratio = 1 / learn_speed
        #else:
        t = t + 1
        ratio = 1/(t*learn_speed)
        # apply gradient down for each random point
        for xi, yi in zip(x, y):
            loss += get_loss(xi, yi, w)
            w = cal_sgd(xi, yi, w, ratio, learn_speed)
       # print train result each time
        print('epoch:{0} loss:{1}'.format(epoch, loss))
        log.write("%d\n"%loss)
    return w

def predict(test_txt, w):
    data = []
    with open(test_txt) as test_data:
         for line in  test_data:
             data.append([float(l) for l in line.split()])
             #data.append(line)
    x_test = np.array(data)
    y_test = (x_test[:, -1]).astype(int)
    x_test[:, -1] = 1
    result = np.sign(np.dot(x_test, w))
    test_log = open("test_result.log", "w")
    for each in result == y_test:
        test_log.write("%d\n"% each)
    print("right predict:", sum(result == y_test), "in", len(result), sum(result==y_test)/len(result))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_data', type=str)
    parser.add_argument('test_data', type=str)
    parser.add_argument('-t', '--time_limit', type=int, default=60)
    args = parser.parse_args()
    train_data = args.train_data
    test_data = args.test_data
    time_limit = args.time_limit
    
    x, y, w, cycle = init(train_data, time_limit)
    
    learn_speed = 0.2
    w = train(x, y, w, cycle, learn_speed)

    result = predict(test_data, w)
    #for each in result:
    #    print(each)

    sys.stdout.flush()
    os._exit(0)
