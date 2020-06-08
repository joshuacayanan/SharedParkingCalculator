# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020
# PURPSOSE: Create a function that calculates shared parking demand for different land uses at a mixed-use site
#           on an hourly basis within a day, for each month of the year. Plot the results in a seaborn facet grid
#           object to show seasonal trends. Command line arguments:
#               1. Working directory where scripts and inputs are stored as --dir 

import os
import numpy as np
import pandas as pd
from get_working_directory import get_working_directory
from LandUse import LandUse

import matplotlib.pyplot as plt
import seaborn as sns

#Navigate to working directory where program and inputs are stored
#in_arg = get_working_directory()
os.chdir(r'C:\Users\joshu\Projects\SharedParkingCalculator\Inputs') #temporarily hard coded to current directory for testing 

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

#Initialise land use objects 
areas = base_parking_demand.index
land_uses = {name: LandUse(name) for name in areas}

#Calculate weekday parking tables and export to Excel
weekday_parking = {}
for land_use in land_uses.values():
    weekday_parking[land_use.name] = land_use.compute_parking('Weekday', base_parking_demand, customer_employee_split, tod_weekday, noncaptive_weekday, monthly_factors)
weekday_parking_table = LandUse.reshape_data(weekday_parking)

# weekday_parking_list = []
# for i in range(0, 12):
#     for key, value in weekday_parking.items():
#         weekday_parking_list.append([key] + value[i])




# #Reset index to convert multiindex months into columns so seaborn FacetGrid can be used
# df.reset_index(drop = False, inplace = True)
# df['Total'] = df.sum(axis = 1, numeric_only = True)

