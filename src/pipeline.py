#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:09:02 2019

@author: idlirshkurti
"""

# =============================================================================
# Pipeline script
# =============================================================================

import pandas as pd
from src.dataloader import load_incoming, load_outgoing
from tqdm import tqdm


'''
The following scripts builds a data pipeline which adds features to an
analytical base table (ABT). Use the run.py script to run the pipeline
and create the ABT table.
'''


class ABT:
    """Analytical Base Table for building analytical models and predicting
    the future behavior of a subject.
    """
    def __init__(self):
        """Constructor to set-up analytical base table.

        Returns:
            abt (pd.DataFrame): DataFrame acting as analytical base table
                                   with numerical index and sorted by
                                   time column 'transaction_timestamp' column.
        """

        self.df_incoming = load_incoming(path_incoming = './', incoming_data = 'data/incoming.csv')
        self.df_incoming['incoming_outgoing'] = 0
        self.df_outgoing = load_outgoing(path_outgoing = './', outgoing_data = 'data/outgoing.csv')
        self.df_outgoing['incoming_outgoing'] = 1
        self.abt = self.df_incoming.append(self.df_outgoing)
        self.abt = self.abt.sort_values(by='transaction_timestamp')
        self.abt.index = range(self.abt.shape[0])
    

    def add_ratio(abt, column_name = 'ratio'):
        
        abt[column_name] = None
        for i in tqdm(range(abt.shape[0])):
            date = abt.loc[i, 'transaction_timestamp']
            
            assert type(date) is pd._libs.tslibs.timestamps.Timestamp, \
            "Date is not the correct format for row: {} in ABT table!".format(i)
            
            user = abt.loc[i, 'user_id']
            assert type(user) is str, \
            "User not identified: {} ".format(user)

            tmp = abt[(abt['user_id'] == user) & (abt['transaction_timestamp'] <= date)]
            
            assert (tmp.shape[0] > 0), \
            "No rows selected for tmp DataFrame in 'ratio' column!"
            
            abt.loc[i, column_name] = tmp.incoming_outgoing.sum()/tmp.shape[0]
            
        return(abt)
        
        
    def add_prev_trans_time(abt, column_name = 'prev_trans_time'):
        
        abt[column_name] = None
        for i in tqdm(range(abt.shape[0])):
            date = abt.loc[i, 'transaction_timestamp']
            
            assert type(date) is pd._libs.tslibs.timestamps.Timestamp, \
            "Date is not the correct format for row: {} in ABT table!".format(i)
            
            user = abt.loc[i, 'user_id']
            assert type(user) is str, \
            "User not identified: {} ".format(user)

            tmp = abt[(abt['user_id'] == user) & (abt['transaction_timestamp'] <= date)]
            
            assert (tmp.shape[0] > 0), \
            "No rows selected for tmp DataFrame in 'prev_trans_time' column!"
            abt.loc[i, column_name] = date - tmp.iloc[-1].transaction_timestamp

        return(abt)
    
        
    def add_average_time(abt, column_name = 'average_time'):
        
        abt[column_name] = None
        for i in tqdm(range(abt.shape[0])):
            
            date = abt.loc[i, 'transaction_timestamp']
            assert type(date) is pd._libs.tslibs.timestamps.Timestamp, \
            "Date is not the correct format for row: {} in ABT table!".format(i)
            
            user = abt.loc[i, 'user_id']
            assert type(user) is str, \
            "User not identified: {} ".format(user)

            tmp = abt[(abt['user_id'] == user) & (abt['transaction_timestamp'] <= date)]
            assert (tmp.shape[0] > 0), \
            "No rows selected for tmp DataFrame in 'average_time' column!"
            
            abt.loc[i, column_name] = tmp.transaction_timestamp.append(pd.core.series.Series([date])).diff().dropna().mean()
            assert type(abt.loc[i, column_name]) is pd._libs.tslibs.timedeltas.Timedelta, \
            "Not the correct format for the i={} row in 'average_time' column!".format(i)
            
        return(abt)
        
'''
If the data scientist decided to add more features to the model, 
they could use a similar format/function as the ones writen 
above to add columns to the 'abt' table
'''

     
