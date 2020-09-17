#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/6/3

import time
import streamlit as st
import numpy
import pandas


def show_s():
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i + 1}')
        bar.progress(i + 1)
        time.sleep(0.01)


def cacur():
    x = st.slider('x')
    st.write(x, 'squared is', x * x)


def title():
    st.title('My first app')


def writet():
    st.write("Here's our first attempt at using data to create a table:")
    st.write(pandas.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    }))


def writed():
    df = pandas.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

    df


def map_test():
    map_data = pandas.DataFrame(
        numpy.random.randn(1000, 2) / [10, 10] + [37.76, -122.4],
        columns=['lat', 'lon'])

    st.map(map_data)


def check_box():
    if st.checkbox('Show dataframe'):
        chart_data = pandas.DataFrame(
            numpy.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.line_chart(chart_data)


def list_box():
    df = pandas.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
    option = st.selectbox(
        'Which number do you like best?',
        df['first column'])

    'You selected: ', option


def cebian():
    df = pandas.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        df['first column'])

    'You selected:', option


# title()
# # map_test()
# cacur()
# show_s()
# writet()
# writed()
# check_box()
# # list_box()
# cebian()

option = st.selectbox(
'How would you like to be contacted?',
('Email', 'Home phone', 'Mobile phone'))
st.write('You selected:', option)
