#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 06 14:54:24 2020

@author: idlirshkurti
"""

import os
import pandas as pd

basepath = os.path.expanduser("~")
os.chdir(basepath + '') # fix to the path of the home directory

from src.pipeline import ABT
from src.dataloader import load_incoming, load_outgoing

# Load the incoming and outgoing data

df_incoming = load_incoming(path_incoming = './', incoming_data = 'data/incoming.csv')
df_outgoing = load_outgoing(path_outgoing = './', outgoing_data = 'data/outgoing.csv')

example = pd.read_csv('./data/example.csv')
example['transaction_timestamp'] = example.transaction_timestamp.astype("datetime64")
example_id = example.loc[0, 'user_id']

# Crate the ABT table
model_building = False

if model_building:
    
    df = ABT()
    df.abt = ABT.add_ratio(df.abt)
    df.abt = ABT.add_prev_trans_time(df.abt)
    df.abt = ABT.add_average_time(df.abt)
    
    '''
    The data scientist could write a few more lines here in order to add 
    more columns/features to the ABT table. These lines should be functions
    defined in the pipeline.py script. 
    
    Also here would be a good place to train a model. Maybe an extra script
    could be used, possibly named 'modelling.py' where machine learning
    model functions are written and implemented here in the run script.
    If this is necessary, the data scientist should change  
    'model_building' in line 28in this script to 'True'.
    
    The model then should be saved in a specific file with the training date
    and the model version. Possibly a separate text file should be saved with
    and explaination of the features necessary for the model to run and the
    necessary format of the input data.
    '''
    
    
    tmp = df.abt.loc[df.abt['user_id'] == example_id]
    example['ratio'] = tmp.incoming_outgoing.sum()/tmp.shape[0]
    example['prev_trans_time'] = example.iloc[0].transaction_timestamp - tmp.iloc[-1].transaction_timestamp
    example['average_time'] = tmp.append(example).reset_index().transaction_timestamp.diff().dropna().mean()
    
    '''
    The data scientist should run the model here with the 'example' data-point and
    make the appropriate Fraud/No Fraud prediction. The command below appends
    the new data with the prediction to the abt table. Ideally this should be
    added to a database. SQL queries could be a lot faster in this scenario
    and improve any bottlenecks in the future once the data grows.

    NOTE:
        - If the data grows significantly and for some reason the ABT table needs
        to be re-run frequently, it wouldnt be smart to re-run the pipeline.py
        script every time. Maybe pyspark could come in handy here in order to speed
        up the process by using a paralellised framework.
        
        - In this example python seems to be satisfactory for ETL purposes, 
        however there are other options. SQL queries could be faster for certain
        pre-processing/loading reasons. Also technologies like NiFi or Informatica
        could be used for data flow automation and easier error diagnosis.
    '''
    
    df.abt = df.abt.append(example).reset_index()
    del tmp, example
    
else:
    '''
    In this scenario the model is already build and we are only 
    interested in making predictions for the new incoming datapoint.
    '''

    df = ABT()    
    tmp = df.abt.loc[df.abt['user_id'] == example_id]
    example['ratio'] = tmp.incoming_outgoing.sum()/tmp.shape[0]
    example['prev_trans_time'] = example.iloc[0].transaction_timestamp - tmp.iloc[-1].transaction_timestamp
    example['average_time'] = tmp.append(example).reset_index().transaction_timestamp.diff().dropna().mean()
    
    df.abt = df.abt.append(example).reset_index()
    del tmp, example
    
    
    
'''
- In order to test if a certain feature is calculated correctly, the 
data scientist could use unit tests on the functions of the pipeline.py script
in order to give a few inputs and check if the output is the one expected.
The 'unittest' library could be used to make this possible.

- It is fair to say that the current method for building the ABT table is not
the most efficient possible since it uses loops. However if the features are 
calculated for every incoming transaction, the rows should be appended to the
ABT table. In order to check where the bottlenecks are in the code, time functions
and breakpoints should be used in order to find which computations are really
the ones taking the longest time. i.e. if the datetime calculations are taking
long to compute, maybe different queries, technologies could be used to speed 
this up when the data grows.



'''
