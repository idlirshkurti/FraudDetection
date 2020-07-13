#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 18:07:49 2019

@author: idlirshkurti
"""

import pandas as pd

def load_incoming(path_incoming, incoming_data):
        
        '''
        Function to load the incoming transaction data
        '''
        
        df_incoming = pd.read_csv(path_incoming + incoming_data, sep = ',')
        df_incoming['transaction_timestamp'] = df_incoming.transaction_timestamp.astype("datetime64")
        
        return df_incoming
    
    
def load_outgoing(path_outgoing, outgoing_data):
    
    '''
    Function to load the outgoing transaction data
    '''
    
    df_outgoing = pd.read_csv(path_outgoing + outgoing_data, sep = ',')
    df_outgoing['transaction_timestamp'] = df_outgoing.transaction_timestamp.astype("datetime64")
    
    return df_outgoing
    
    
    