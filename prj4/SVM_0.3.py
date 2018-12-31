# -*- coding: utf-8 -*-
"""
Using SVM to classify dataset
| Version | Commit
|   0.1   | Finish first version based on slide
|   0.2   | Add time control
|   0.3   | Add 10-fold cross validation and init $w$ with random 
"""

import time
import sys
import argparse
import os
import numpy as np
import math

time_limit = 0
isDebug = 0
## Load and  prepare train data
def init(train_txt):
    data = []
    with open(train_txt) as train_data:
         for line in  train_data:
             data.append([float(l) for l in line.split()])
    x = np.array(data)
    y = (x[:, -1]).astype(int)
    x[:, -1] = 1
    w = np.random.uniform(size=np.shape(x)[1],)
    return x, y, w
    
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
def train(x, y, w, learn_speed, time0, time_lim):
    if isDebug: log = open("learn_curve.log", "w")
    t = 0
    while(time.time()-time0 < time_lim):
        randomize =  np.arange(len(x))
        np.random.shuffle(randomize)
        x = x[randomize]
        y = y[randomize]
        loss = 0
        t = t + 1
        ratio = 1/(t*learn_speed)
        # apply gradient down for each random point
        for xi, yi in zip(x, y):
            loss += get_loss(xi, yi, w)
            w = cal_sgd(xi, yi, w, ratio, learn_speed)
       # print train result each time
        if isDebug: log.write("%d\n"%(loss))
    return w

def predict(test_txt, w):
    data = []
    with open(test_txt) as test_data:
         for line in  test_data:
             data.append([float(l) for l in line.split()])
    x_test = np.array(data)
    x_test = np.c_[x_test, np.ones((x.shape[0]))]
    result = np.sign(np.dot(x_test, w))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_data', type=str)
    parser.add_argument('test_data', type=str)
    parser.add_argument('-t', '--time_limit', type=int, default=10)
    args = parser.parse_args()
    train_data = args.train_data
    test_data = args.test_data
    time_limit = args.time_limit
    
    x, y, w = init(train_data)
    
    learn_speed = 0.3
    #learn_speed = 0.2

    #w = train(x, y, w, learn_speed, time.time(), time_limit-1)
    # 10-hold cross validation
    randomize =  np.arange(len(x))
    np.random.shuffle(randomize)
    x = x[randomize]
    y = y[randomize]
    train_sroce = [] 
    train_w = []
    step = len(x)//10
    time_lim = (time_limit-1.5)/10
    for i in range(10):
        w = np.random.uniform(size=np.shape(x)[1],)
        if not(i==9):
            test_x = x[i*step:i*step+step]
            test_y = y[i*step:i*step+step]
            train_x = np.concatenate((x[0:i*step],x[i*step+step::]),axis=0)
            train_y = np.concatenate((y[0:i*step],y[i*step+step::]),axis=0)
        else:
            test_x = x[9*step: :]
            test_y = y[9*step: :]
            train_x = x[0:9*step]
            train_y = y[0:9*step]
        w= train(train_x, train_y, w, learn_speed, time.time(), time_lim)
        train_w.append(w)
        acc = 0
        for xi, yi in zip(test_x, test_y):
            predict_res = np.sign(np.dot(test_x, w))
            acc = sum(test_y==predict_res)/len(test_x)
        train_sroce.append(acc)

    #if isDebug: print(sum(train_sroce)/len(train_sroce))
    w = sum(train_w)/len(train_w)

    result = predict(test_data, w)
    if isDebug: output = open("test_data_res.txt","w")
    for each in result:
        if isDebug:
            display= "%.1f\n"%each
            output.write(display)
        else:
            print(each)
    if isDebug: output.close()
    sys.stdout.flush()
    os._exit(0)
