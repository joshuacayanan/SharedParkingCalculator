#Collapse the 12 spreadsheets into one Excel file for ease of viewing, use append method

import os
import pandas as pd

weekday_path = r'Y:\Shared\R & D\Shared Parking Calculator\Outputs\Weekday'
weekend_path = r'Y:\Shared\R & D\Shared Parking Calculator\Outputs\Weekend'

#Define function to list files in directory
def file_lister(directory_path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directory_path):
        for file in f:
            if '.xlsx' in file:
                files.append(os.path.join(r, file))
    return files

weekday_files = file_lister(weekday_path)
weekend_files = file_lister(weekend_path)

#Read spreadsheets into pandas dataframes, combine
def combiner(file_list):
    list_of_dfs = [pd.read_excel(filename, index_col= 0) for filename in file_list]
    for dataframe, filename in zip(list_of_dfs, file_list):
        dataframe['Month'] = filename[-8:-5]
    combined_df = pd.concat(list_of_dfs)
    return combined_df

weekday_dfs = combiner(weekday_files)
weekend_dfs = combiner(weekend_files)

#Export combined dataframes to Excel
weekday_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekday\\SharedParkingOutput_Weekday_Combined.xlsx'
weekend_filename = 'Y:\\Shared\\R & D\\Shared Parking Calculator\\Outputs\\Weekend\\SharedParkingOutput_Weekend_Combined.xlsx'
weekday_dfs.to_excel(weekday_filename)
weekend_dfs.to_excel(weekend_filename)
