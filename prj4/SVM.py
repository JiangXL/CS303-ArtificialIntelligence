# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14

import multiprocessing as mp
import time
import sys
import argparse
import os
import numpy as np




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

    sys.stdout.flush()
    os._exit(0)
