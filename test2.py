#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/28
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal


def ArithmeticAverage(inputs, per):
    inputs = np.array(inputs)
    if np.shape(inputs)[0] % per != 0:
        lengh = np.shape(inputs)[0] / per
        for x in range(int(np.shape(inputs)[0]), int(lengh + 1) * per):
            inputs = np.append(inputs, inputs[np.shape(inputs)[0] - 1])
    inputs = inputs.reshape((-1, per))
    mean = []
    for tmp in inputs:
        mean.append(tmp.mean())
    return mean


def SlidingAverage(inputs, per):
    inputs = np.array(inputs)
    if np.shape(inputs)[0] % per != 0:
        lengh = np.shape(inputs)[0] / per
        for x in range(int(np.shape(inputs)[0]), int(lengh + 1) * per):
            inputs = np.append(inputs, inputs[np.shape(inputs)[0] - 1])
    inputs = inputs.reshape((-1, per))
    tmpmean = inputs[0].mean()
    mean = []
    for tmp in inputs:
        mean.append((tmpmean + tmp.mean()) / 2)
        tmpmean = tmp.mean()
    return mean


# 遍历文件夹
def walkFile(file):
    f_list = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            # print(os.path.join(root, f))
            f_list.append(str(os.path.join(root, f)))
        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))
    return f_list


plt.figure()
plt.title("accelerated speed g")
plt.subplot(211)
f1 = "move44.txt"
f2 = "junlv2.txt"
# f_list = walkFile("F:\mpu9250r\猪皮的文件\move0604")

# print(f_list)
# for fl in f_list:
data = []
with open('move0604/move401.txt', 'r') as f:
    for i, line in enumerate(f):
        if 0 < i < 2000:
            # for line in f:
            d_list = line.split(',')
            g_data = round((pow(float(d_list[0]), 2) + pow(float(d_list[1]), 2) + pow(float(d_list[2]), 2)) ** 0.5, 2)
            data.append(g_data)

# data1 = SlidingAverage(data, 4)
data1 = ArithmeticAverage(data, 10)
# print(data)
a = round(sum(data) / len(data), 2)
print(a)
b = round((max(data) + min(data)) / 2, 2)
h = round(((max(data) + min(data)) / 2) * 1.03, 2)
# 101--1030--1.3  102--1160--1.3  103--1170--1.3  151--1160--1.2  152--1175--1.3
# 153--1025--1.2  201--1033--1.3  202--1175--1.3  301--1159--1.3  401--1160--1.5
# 302--1165--1.5
he = 1028

peakind = signal.find_peaks(data1, height=a, width=1.5)  # 找到峰值
# print(peakind)
# print(len(peakind[0]))
plt.scatter(peakind[0], peakind[1]["peak_heights"], c="r", marker="d", label="Cycle:" + str(peakind[0].shape[0]))
plt.plot(data1, label="g")
# plt.hlines(h, 0, 200, colors='r', label="h:" + str(h))
plt.hlines(a, 0, 200, colors='r', label="a:" + str(a))
# plt.hlines(b, 0, 200, colors='y', label="b:" + str(b))
# plt.hlines(he, 0, 200, colors='b', label="he:" + str(he))
plt.legend()
plt.subplot(212)
plt.plot(data)

plt.show()
