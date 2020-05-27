# # -*- coding: utf-8 -*-
# """
# Shared Parking Program V1
# Joshua Cayanan
# """

# import os
# import numpy as np
# import pandas as pd

# #Change current working directory, link to folder with input CSVs
# filepath = r"Y:\Shared\R & D\Shared Parking Calculator\Inputs"
# os.chdir(filepath)

# #Import customer/staff and time-of-day data from a CSV into a Pandas dataframe
# split_time_of_day_weekday = pd.read_csv('SplitAndTimeOfDayWeekday.csv')
# split_time_of_day_weekend = pd.read_csv('SplitAndTimeOfDayWeekend.csv')

# #Import noncpative adjustment data from a CSV into a Pandas dataframe
# noncaptive_adjustment = pd.read_csv('NoncaptiveAdjustment.csv')

# #Import monthly adjustment data from a CSV into a Pandas dataframe
# monthly_adjustment = pd.read_csv('MonthlyAdjustment.csv')

# #Import base parking demand from a CSV into a Pandas dataframe
# base_parking_demand = pd.read_csv('BaseParkingDemand.csv')



# #Initialise land use objects 
# Areas = base_parking_demand['Type'].tolist()


# # Generate monthly parking totals:
# months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# for i in range(1,13):
#     for land_use in land_uses.values():
#         land_use.weekday_parking = land_use.compute_parking(base_parking_demand, split_time_of_day_weekday, noncaptive_adjustment, i)
#         land_use.weekend_parking = land_use.compute_parking(base_parking_demand, split_time_of_day_weekend, noncaptive_adjustment, i) 
#     weekday_stack = np.vstack([land_use.weekday_parking for land_use in land_uses.values()])
#     weekend_stack = np.vstack([land_use.weekend_parking for land_use in land_uses.values()])

#     #Turn the vertical stacks into Pandas dataframes
#     row_names = Areas
#     column_names = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00']

#     weekday_df = pd.DataFrame(weekday_stack, columns = column_names, index = row_names)
#     weekday_df.loc['Total'] = weekday_df.apply(lambda x: x.sum())

#     weekend_df = pd.DataFrame(weekend_stack, columns = column_names, index = row_names)
#     weekend_df.loc['Total'] = weekend_df.apply(lambda x: x.sum())

#     #Export dataframes to Excel
#     weekday_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekday\\SharedParkingOutput_Weekday_{}.xlsx'.format(months[i-1])
#     weekend_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekend\\SharedParkingOutput_Weekend_{}.xlsx'.format(months[i-1])
#     weekday_df.to_excel(weekday_filename)
#     weekend_df.to_excel(weekend_filename)