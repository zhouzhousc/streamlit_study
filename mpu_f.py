#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/6/4

import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import plotly.graph_objects as go


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


base = r"."
file_position = "F:\mpu9250r\猪皮的文件"
f_list = os.listdir(file_position)
st.sidebar.title('mpu test app')

floder = [f for f in os.listdir(file_position) if "." not in f]

selected_floder = st.sidebar.selectbox(
    'Please select your file in ',
    floder)

f_list2 = os.listdir(os.path.join(file_position, selected_floder))
txt_file = [f for f in f_list2 if ".txt" in f]
print(txt_file)
txt_file2 = [
    i + "  (" + str(
        round(os.path.getsize(os.path.join(file_position, selected_floder, i)) / float(1024 * 1024), 2)) + 'MB)'
    for i in txt_file]

option2 = st.sidebar.selectbox(
    'Please select file in {}"'.format(selected_floder),
    txt_file2)

number = st.sidebar.slider("fileter count per ", min_value=2, max_value=14, value=10, step=None, format=None, key=None)

height = st.sidebar.number_input('effective data peaks height', min_value=1020, max_value=1380, value=1160, step=10)
width = st.sidebar.number_input('effective data peaks width', min_value=0.3, max_value=3.0, value=1.3, step=0.2)

st.write('You selected file:', option2)
st.write('filter per:', number)
st.write('effective height:', height)
st.write('effective width:', width)

plt.figure()
st.header("accelerated speed g")
try:
    data = []
    with open(os.path.join(file_position, selected_floder, str(option2).split(" ")[0]), 'r') as f:
        for i, line in enumerate(f):
            # if 0 < i < 2000:
            if i > 0:
                # for line in f:
                d_list = line.split(',')
                g_data = round((pow(float(d_list[0]), 2) + pow(float(d_list[1]), 2) + pow(float(d_list[2]), 2)) ** 0.5,
                               2)
                # g_data = round(float(d_list[0]), 2)
                data.append(g_data)

    data1 = ArithmeticAverage(data, number)
    a = round(sum(data) / len(data), 2)
    print(a)
    b = round((max(data) + min(data)) / 2, 2)
    h = round(((max(data) + min(data)) / 2) * 1.03, 2)
    # 101--1030--1.3  102--1160--1.3  103--1170--1.3  151--1160--1.2  152--1175--1.3
    # 153--1025--1.2  201--1033--1.3  202--1175--1.3  301--1159--1.3  401--1160--1.5
    # 302--1165--1.5
    he = 1028

    peakind = signal.find_peaks(data1, height=height, width=width)  # 找到峰值
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=np.arange(len(data1)), y=data1,
                   mode='lines', name="g")
    )
    fig.add_trace(
        go.Scatter(x=peakind[0], y=peakind[1]["peak_heights"], mode="markers", name="Cycle:" + str(peakind[0].shape[0]))
    )

    st.plotly_chart(fig, use_container_width=True)
    st.header("accelerated speed g")
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(x=np.arange(len(data)), y=data,
                   mode='lines', name="g")
    )

    st.plotly_chart(fig2, use_container_width=True)

except:
    pass
