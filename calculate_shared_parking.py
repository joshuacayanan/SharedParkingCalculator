# PROGRAMMER: Joshua Cayanan
# DATE CREATED: May 25, 2020
# PURPSOSE: Create a function that calculates shared parking demand for different land uses at a mixed-use site
#           on an hourly basis within a day, for each month of the year. Plot the results in a seaborn facet grid
#           object to show seasonal trends. Command line arguments:
#               1. Working directory where scripts and inputs are stored as --dir 


from LandUse import parking_demand
from get_inputs import get_working_directory

#Get working directory from command line input
# get_working_directory()

#Calculate weekday parking tables and export to Excel
weekday_parking_demand = parking_demand('Weekday')
weekday_filepath = r'C:\Users\joshu\Projects\SharedParkingCalculator\Outputs\WeekdayParking.xlsx'
weekday_parking_demand.to_excel(weekday_filepath)

#Calculate weekend parking tables and export to Excel
weekend_parking_demand = parking_demand('Weekend')
weekend_filepath = r'C:\Users\joshu\Projects\SharedParkingCalculator\Outputs\WeekendParking.xlsx'
weekend_parking_demand.to_excel(weekend_filepath)



