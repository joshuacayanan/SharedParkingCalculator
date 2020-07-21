# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020

import os
import argparse
import pandas as pd

def get_working_directory():
    '''
    Inputs working directory from user to direct terminal to location of inputs, scripts, and where to save outputs

    Parameters:
      None - simply uses argparse module to craete and store command line arguments

    Returns:
      parse_args() - data structure that stores the command line arguments object
    '''

    #Create parser object
    parser = argparse.ArgumentParser()

    #Create 1 command line argument for working directory
    parser.add_argument('--dir', type = str, help = 'path to shared parking program in your project folder')

    #Return the given working directory
    return parser.parse_args()

def get_inputs():
    #Get working directory from command line input
    in_arg = get_working_directory()
    input_directory = in_arg.dir + '\Inputs'
    os.chdir(input_directory)
    
    #Import base parking demand from a CSV into a Pandas dataframe
    base_parking_demand = pd.read_csv('BaseParkingDemand.csv', index_col = 0)

    #Import customer vs employee split CSV into a Pandas dataframe
    customer_employee_split = pd.read_csv('CustomerEmployeeSplit.csv', index_col = 0)

    #Import customer/staff and time-of-day data from a CSV into a Pandas dataframe
    tod_weekday = pd.read_csv('TimeOfDayWeekday.csv', index_col = 0)
    tod_weekend = pd.read_csv('TimeOfDayWeekend.csv', index_col = 0)

    #Import noncpative adjustment data from a CSV into a Pandas dataframe
    noncaptive_weekday = pd.read_csv('NoncaptiveAdjustmentWeekday.csv', index_col = 0)
    noncaptive_weekend = pd.read_csv('NoncaptiveAdjustmentWeekend.csv', index_col = 0)

    #Import monthly adjustment data from a CSV into a Pandas dataframe
    monthly_factors = pd.read_csv('MonthlyAdjustment.csv', index_col = 0)

    return base_parking_demand, customer_employee_split, tod_weekday, tod_weekend, \
           noncaptive_weekday, noncaptive_weekend, monthly_factors

