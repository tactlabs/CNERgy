#!/usr/bin/env python
# -*- coding: utf-8 -*-
# the above line is to avoid 'SyntaxError: Non-UTF-8 code starting with' error

'''
Created on 

Course work: 

@author: raja

Source:
    https://www.programiz.com/python-programming/datetime/strftime
'''

# Import necessary modules

import datetime
import time

def get_current_time_millis():

    millis = int(round(time.time() * 1000))

    return millis

def get_current_date_str():

    current_date     = datetime.date.today()
    current_date_str = current_date.strftime("%d-%m-%Y") 

    return current_date_str

def get_current_date_with_time_str():

    current_date     = datetime.date.today()
    current_date_str = current_date.strftime("%d-%m-%Y %H:%M:%S") 

    return current_date_str

def get_current_datetime():

    current_datetime = datetime.datetime.now()

    return current_datetime