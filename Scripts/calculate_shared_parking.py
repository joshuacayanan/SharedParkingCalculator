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

# test_landuse = LandUse('Retail')
# test_landuse.compute_parking('Weekday', base_parking_demand, customer_employee_split, tod_weekday, noncaptive_weekday, monthly_factors)

weekday_parking = {}
for land_use in land_uses.values():
    weekday_parking[land_use.name] = land_use.compute_parking('Weekday', base_parking_demand, customer_employee_split, tod_weekday, noncaptive_weekday, monthly_factors)

weekday_parking_list = []
for i in range(0, 12):
    for key, value in weekday_parking.items():
        weekday_parking_list.append([key] + value[i])

col_names = ['Land Use','6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00', 'Month']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
times = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00']


df = pd.DataFrame(weekday_parking_list, columns = col_names)


df = df.melt(['Land Use', 'Month'], value_vars = times, var_name = 'Time', value_name = 'Parking')
df['Month'] = pd.Categorical(df['Month'], categories = months, ordered = True)
df['Time'] = pd.Categorical(df['Time'], categories = times, ordered = True)
df.sort_values(by = ['Month', 'Time'], inplace = True)
df.reset_index(drop = True, inplace = True)


df = df.pivot_table(
    values = 'Parking', index = ['Month', 'Time'], columns = ['Land Use'],
    fill_value = 0, aggfunc = 'first') #this point is good to export to Excel

#Reset index to convert multiindex months into columns so seaborn FacetGrid can be used
df.reset_index(drop = False, inplace = True)
df['Total'] = df.sum(axis = 1, numeric_only = True)

               
graphs = sns.FacetGrid(data = df, col = 'Month', col_wrap = 4)
graphs.map(plt.errorbar, 'Time', 'Total')
graphs.set_titles('{col_name}')
graphs.xticks(rotation = 90)
