# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020

import numpy as np
import pandas as pd

#Create a Class for ULI land use categories
class LandUse:
    def __init__(self, name):
        self.name = name

    def compute_parking(self, context, base_parking_demand, customer_employee_split, tod, noncaptive, monthly):
        #Concatenate user type suffixes to land use name for subsequent dataframe match row to string search
        customer_row_namer = self.name + 'Customer'
        employee_row_namer = self.name + 'Employee'
        
        #Extract appropriate rows based on land use name from common dataframes
        df_1 = base_parking_demand
        daily_demand = df_1.loc[self.name, context]

        df_2 = customer_employee_split
        customer_split = df_2.loc[self.name, 'Customer' + context]
        employee_split = df_2.loc[self.name, 'Employee' + context]
        
        df_3 = tod
        customer_tod = df_3.loc[customer_row_namer, :]
        employee_tod = df_3.loc[employee_row_namer, :]
        
        df_4 = noncaptive
        customer_noncaptive = df_4.loc[customer_row_namer, :]
        employee_noncaptive = df_4.loc[employee_row_namer, :]

        df_5 = monthly
        customer_monthly = df_5.loc[customer_row_namer, :]
        employee_monthly = df_5.loc[employee_row_namer, :]

      
        
        #Calculate the parking demand, adjusted for customer/staff split, time of day profiles, noncaptive, and monthly effects
        parking_demand_yearly = []
        for month in list(monthly.columns):
            parking_demand_customer = daily_demand * customer_split * customer_tod * customer_noncaptive * customer_monthly.loc[month]
            parking_demand_employee = daily_demand * employee_split * employee_tod * employee_noncaptive * employee_monthly.loc[month]
            parking_demand_total = np.rint((parking_demand_customer + parking_demand_employee).astype(int)).values.tolist()
            parking_demand_total.append(month)
            parking_demand_yearly.append(parking_demand_total)

    
        return parking_demand_yearly
