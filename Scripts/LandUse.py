# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020

import numpy as np
import pandas as pd

col_names = ['Land Use','6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00', 'Month']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
times = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00']

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
                            fill_value = 0, aggfunc = 'first') #this point is good to export to Excel
        return df