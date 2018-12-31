import numpy as np

predict = open("test_data_res.txt","r")
label = open("test_data_y.txt","r")

predict = []
with open("test_data_res.txt") as test_res:
    for line in  test_res:
        predict.append([float(l) for l in line.split()])
predcit = np.array(predict)

real = []
with open("test_data_y.txt") as r:
    for line in  r:
        real.append([float(l) for l in line.split()])
real = np.array(real)

right = 0
print(sum(real == predict)/len(real))

