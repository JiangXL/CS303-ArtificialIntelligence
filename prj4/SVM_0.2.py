# -*- coding: utf-8 -*-
"""
Using SVM to classify dataset
| Version | Commit
|   0.1   | Finish first version based on slide
|   0.2   | Add time control
"""

import time
import sys
import argparse
import os
import numpy as np

time_limit = 0
time0 = time.time()
isDebug = 0
## Load and  prepare train data
def init(train_txt):
    data = []
    with open(train_txt) as train_data:
         for line in  train_data:
             #print(line)
             data.append([float(l) for l in line.split()])
             #data.append(line)
             #print(data[-1])
    x = np.array(data)
    y = (x[:, -1]).astype(int)
    x[:, -1] = 1
    w = np.zeros(len(x[1,:]))
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
def train(x, y, w, learn_speed):
    # Repeat cnt time
    if isDebug: log = open("learn_curve.log", "w")
    t = 0
    while(time.time()-time0 < time_limit-2):
    #for epoch in range(100):
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
        #print('epoch:{0} loss:{1}'.format(t, loss))
        if isDebug: log.write("%d\n"%loss)
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
    if isDebug:
        test_log = open("test_result.log", "w")
        for each in result == y_test:
            test_log.write("%d\n"% each)
        print("right predict:", sum(result == y_test), "in", len(result), sum(result==y_test)/len(result))
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
    
    learn_speed = 0.2
    w = train(x, y, w, learn_speed)

    result = predict(test_data, w)
    if not isDebug:
        for each in result:
            print(each)

    sys.stdout.flush()
    os._exit(0)
