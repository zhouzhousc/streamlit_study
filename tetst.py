#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/6/5

import os

print(os.listdir("F:\mpu9250r\猪皮的文件"))
wav_path = "F:\mpu9250r\猪皮的文件\move0604\move101.txt"

fsize = os.path.getsize(wav_path)

f_kb = round(fsize / float(1024), 2)
f_mb = round(fsize / float(1024 * 1024), 2)
f_gb = round(fsize / float(1024 * 1024 * 1024), 2)
print(f_mb)

import plotly.graph_objects as go
import numpy as np

fig = go.Figure(data=go.Scatter(
    y = np.random.randn(500),
    mode='markers',
    marker=dict(
        size=16,
        color=np.random.randn(500), #set color equal to a variable
        colorscale='Viridis', # one of plotly colorscales
        showscale=True
    )
))

fig.show()
