# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020

import numpy as np
import pandas as pd
from get_inputs import get_inputs

#Call the get_inputs function
base_parking_demand, customer_employee_split, tod_weekday, tod_weekend, \
noncaptive_weekday, noncaptive_weekend, monthly_factors = get_inputs()

#Create a Class for ULI land use categories
class LandUse():
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
        for month in months:
            parking_demand_customer = daily_demand * customer_split * customer_tod * customer_noncaptive * customer_monthly.loc[month]
            parking_demand_employee = daily_demand * employee_split * employee_tod * employee_noncaptive * employee_monthly.loc[month]
            parking_demand_total = np.rint((parking_demand_customer + parking_demand_employee).astype(int)).values.tolist()
            parking_demand_total.append(month)
            parking_demand_yearly.append(parking_demand_total)
                
        return parking_demand_yearly

    def reshape_data(data_dictionary):

        data_list = []
        for i in range(0, 12):
            for key, value in data_dictionary.items():
                data_list.append([key] + value[i])
        
        #Convert to pandas df and apply transformations to reshape the data
        df = pd.DataFrame(data_list, columns = col_names)
        df = df.melt(['Land Use', 'Month'], value_vars = times, var_name = 'Time', value_name = 'Parking')
        df['Month'] = pd.Categorical(df['Month'], categories = months, ordered = True)
        df['Time'] = pd.Categorical(df['Time'], categories = times, ordered = True)
        df.sort_values(by = ['Month', 'Time'], inplace = True)
        df.reset_index(drop = True, inplace = True)
       
        df = df.pivot_table(values = 'Parking', index = ['Month', 'Time'], columns = ['Land Use'], \
                            fill_value = 0, aggfunc = 'first') 

        #Create a new total column
        df['Total'] =df.sum(axis = 1)

        return df

#Dataframe columns in list format
times = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', \
        '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00']
col_names = ['Land Use'] + times + ['Month']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#Initialise land use objects 
areas = base_parking_demand.index
land_uses = {name: LandUse(name) for name in areas}

#Create function for weekday and weekend parking demand
def parking_demand(context):
    if context == 'Weekday':
        tod, noncaptive = tod_weekday, noncaptive_weekday
    else:
        tod, noncaptive = tod_weekend, noncaptive_weekend
    parking_demand = {}
    for land_use in land_uses.values():
        parking_demand[land_use.name] = land_use.compute_parking(context, base_parking_demand, customer_employee_split, \
                                        tod, noncaptive, monthly_factors)
    return LandUse.reshape_data(parking_demand)


   