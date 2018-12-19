# -*- coding: utf-8 -*-

import multiprocessing as mp
import time
import sys
import argparse
import os
import numpy as np


## Load and  prepare train data
def init(train_txt):
    data = []
    with open(train_txt, "r") as train_data:
    for line in  train_data:
        data.append([float(l) for l in line.split()])
    x = np.array(data)
    y = x[:, -1].astype(int)
    x[:, -1] = np.ones(len(data))
    w = np.zeros(len(data)+1)
    cycle = 100
    return x, y, w, cycle
    
def get_loss(xi, yi, w):
    loss = max(0, 1-yi*np.dot(xi, w))
    return loss

## update weight
def cal_sgd(xi, yi, w, ratio, learn_speed):
    # update down hilll speed
    if yi*np.dot(xi,w) < 1:
        w_next = w - ratio*(ratio*w - yi*xi)
    else:
        w_next = w - w*ratio*learn_speed
    return w_next

## Training fucntion
def train(x, y, w, cnt, learn_speed):
    # Repeat cnt time
    t = 0
    for epoch in range(cnt):
        randominze =  np.arange(len(x))
        np.random.shuffle(randomize)
        x = x[randomize]
        y = y[randomize]
        loss = 0
        # update ratio of learn_speed each time
        if epoch < cnt/2:
            ratio = 1 / learn_speed
        else:
            t = t + 1
            ratio = 1/(t*learn_speed)
        # apply gradient down for each random point
        for xi, yi in zip(x, y):
            loss += get_loss(xi, yi)
            w = cal_sgd(xi, yi, w)
       # print train result each time
        print('epoch:{0} loss:{1}'.format(epoch, loss))
    return w

def predict(x, w):
    x_test = np.c_[np.ones((s.shape[0])), x]
    return np.sign(np.dot(x_test, w))

if __name__ == '__main__':
    '''
    从命令行读参数示例
    '''
    print("从命令行读参数示例")
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

    #predict(x, w, test_data)

    sys.stdout.flush()
    os._exit(0)
