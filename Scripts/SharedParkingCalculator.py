# -*- coding: utf-8 -*-
"""
Shared Parking Program V1
Joshua Cayanan
"""

import os
import numpy as np
import pandas as pd

#Change current working directory, link to folder with input CSVs
filepath = r"Y:\Shared\R & D\Shared Parking Calculator\Inputs"
os.chdir(filepath)

#Import customer/staff and time-of-day data from a CSV into a Pandas dataframe
split_time_of_day_weekday = pd.read_csv('SplitAndTimeOfDayWeekday.csv')
split_time_of_day_weekend = pd.read_csv('SplitAndTimeOfDayWeekend.csv')

#Import noncpative adjustment data from a CSV into a Pandas dataframe
noncaptive_adjustment = pd.read_csv('NoncaptiveAdjustment.csv')

#Import monthly adjustment data from a CSV into a Pandas dataframe
monthly_adjustment = pd.read_csv('MonthlyAdjustment.csv')

#Import base parking demand from a CSV into a Pandas dataframe
base_parking_demand = pd.read_csv('BaseParkingDemand.csv')

#Create a Class for ULI land use categories
class LandUse:
    def __init__(self, name):
        self.name = name

    def compute_parking(self, base_parking_demand, split_time_of_day_distribution, noncaptive_distribution, month):
        #Concatenate user type suffixes to land use name for subsequent dataframe match row to string search
        customer_row_namer = self.name + 'Customer'
        employee_row_namer = self.name + 'Employee'
        
        #Extract appropriate rows based on land use name from common dataframes
        df_1 = split_time_of_day_distribution
        df_2 = noncaptive_distribution
        df_3 = monthly_adjustment
        customer_row_1 = df_1[df_1['Type'].str.match(customer_row_namer)].values
        employee_row_1 = df_1[df_1['Type'].str.match(employee_row_namer)].values
        customer_row_2 = df_2[df_2['Type'].str.match(customer_row_namer)].values
        employee_row_2 = df_2[df_2['Type'].str.match(employee_row_namer)].values
        customer_row_3 = df_3[df_3['Type'].str.match(customer_row_namer)].values
        employee_row_3 = df_3[df_3['Type'].str.match(employee_row_namer)].values
            
        #Extract base parking demand based on land use name from common dataframe       
        df_4 = base_parking_demand
        base_row = df_4[df_4['Type'].str.match(self.name)].values
        base_demand = base_row[0,1]
        
        #Obtain single value for split of base parking demand that is from customers, 
        #Obtain time of day profile, noncaptive adjustment
        customer_split = customer_row_1[0,1]
        customer_time_of_day = customer_row_1[0,2:]
        customer_noncaptive = customer_row_2[0,1:]
        customer_monthly = customer_row_3[0, month]

        #Obtain single value for split of base parking demand that is from employees, 
        #Obtain time of day profile, noncaptive adjustment
        employee_split = employee_row_1[0,1]
        employee_time_of_day = employee_row_1[0,2:]
        employee_noncaptive = employee_row_2[0,1:]
        employee_monthly = employee_row_3[0, month]
        
        #Calculate the parking demand, adjusted for customer/staff split, time of day profiles, noncaptive, and monthly effects
        parking_demand_customer = base_demand * customer_split * customer_time_of_day * customer_noncaptive * customer_monthly
        parking_demand_employee = base_demand * employee_split * employee_time_of_day * employee_noncaptive * employee_monthly
        parking_demand_total = np.rint((parking_demand_customer + parking_demand_employee).astype(float))
        parking_demand_total = np.reshape(parking_demand_total, (1,19))
        
        return parking_demand_total

#Initialise land use objects 
Areas = base_parking_demand['Type'].tolist()
land_uses = {name: LandUse(name) for name in Areas}

# Generate monthly parking totals:
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    for land_use in land_uses.values():
        land_use.weekday_parking = land_use.compute_parking(base_parking_demand, split_time_of_day_weekday, noncaptive_adjustment, i)
        land_use.weekend_parking = land_use.compute_parking(base_parking_demand, split_time_of_day_weekend, noncaptive_adjustment, i) 
    weekday_stack = np.vstack([land_use.weekday_parking for land_use in land_uses.values()])
    weekend_stack = np.vstack([land_use.weekend_parking for land_use in land_uses.values()])

    #Turn the vertical stacks into Pandas dataframes
    row_names = Areas
    column_names = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00']

    weekday_df = pd.DataFrame(weekday_stack, columns = column_names, index = row_names)
    weekday_df.loc['Total'] = weekday_df.apply(lambda x: x.sum())

    weekend_df = pd.DataFrame(weekend_stack, columns = column_names, index = row_names)
    weekend_df.loc['Total'] = weekend_df.apply(lambda x: x.sum())

    #Export dataframes to Excel
    weekday_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekday\\SharedParkingOutput_Weekday_{}.xlsx'.format(months[i-1])
    weekend_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekend\\SharedParkingOutput_Weekend_{}.xlsx'.format(months[i-1])
    weekday_df.to_excel(weekday_filename)
    weekend_df.to_excel(weekend_filename)