<p float="left">
  <img src="https://github.com/joshuacayanan/SharedParkingCalculator/blob/master/Assets/calculator.png" width="70" align="right"/>
  <img src="https://github.com/joshuacayanan/SharedParkingCalculator/blob/master/Assets/car-parking.png" width="70" align="right"/> 
</p>



# Shared Parking Calculator
This repository contains a calculator that forecasts shared parking demand for mixed-use sites. Parking demand for each land use is calculated on an hourly basis from 6:00 - 0:00 within a typical weekday or weekend day for each month of the year. The calculator also plots the following graphs:

- Maximum hourly parking demand for each month, line graph with 85th percentile demand
- Hourly parking demand for busiest month, stacked bar graph
- Hourly parking demand for 85th percentile month, stacked bar graph

## Workflow Example
<p float="left">
  <img src="https://github.com/joshuacayanan/SharedParkingCalculator/blob/master/Assets/Workflow.jpg" width="1000" align="center"/>
</p>

The above flowchart and accompanying instrucitons are for an example mixed-use site with retail, food services, entertainment, fitness, office, hotel, and child care uses. Base parking demand is calculated using appropriate parking generation ratios (bylaw, demand, or supply) with respect to variables such as gross floor area, number of hotel rooms, or number of children in care.

1. Categorise individual land uses (cyan) into land use classes (navy blue) with common parking behaviours. For example, _Gym_ and _Yoga Studio_ have similar patron parking patterns so they are modeled as a __Health Club__. Create as many land use classes as required to capture different parking behaviours, ensure that name and factors defined as per below instructions. Unused land use classes may be retained in the input files.

#### The following steps refer to files in the `Inputs` folder

2. Compile the base parking demand for each land use class into the `BaseParkingDemand.csv` file, typically analyze weekday and weekend scenarios because certain uses such as office are not as active on weekends while shopping and restaurant uses might be busier. 

3. Decide on the staff/visitor split as staff and visitors (employees and customers) are suject to separate adjustment factors. The staff/visitor splits are stored in the `CustomerEmployeeSplit.csv` file. 

4. Decide on the time of day factors for each  land use class, there will be one set of hourly factors (6:00 - 0:00) for employees and one set for customers for each class. The time of day adjustment factors are stored in the `TimeOfDayWeekday.csv` and `TimeofDayWeekend.csv` files. 

5. Decide on the non-captive market adjustment factors for each land use class, there will be one set of hourly factors (6:00 - 0:00) for employees and one set for customers for each class. The time of day adjustment factors are stored in the `NoncaptiveAdjustmentWeekday.csv` and `NoncaptiveAdjustmentWeekend.csv` files.

6. Decide on the monthly adjustment factors for each land use class, there will be one set of monthly factors for each class, common to both employees and customers. The monthly adjustment factors are stored in the `MonthlyAdjustment.csv` file. 

Values for the above input files are usually based on industry guidance and/or engineering judgement, make sure to document your assumptions.

#### Once the input file values have been finalised, call the program from the terminal `python calculate_shared_parking.py --dir [insert filepath here]` where the filepath is where the `Inputs` and `Outputs` folders are stored. Once called, the program will perform the following steps:

1. Read base parking demand for each land use class

2. Split the base parking demand into customer parking demand and employee parking demand which are subject to their own set of adjustments.

3. Multiply the base parking demand by the time of day factors to generate an hourly demand vector for each land use. Each land use class will calculate one hourly demand vector for customers and one hourly demand vector for employees to arrive at unadjusted shared parking demand. 

4. Apply non-captive market adjustments for each land use, varying by the hour, to account for the interactions between land uses within the site. For example, an office worker going to a fast-food restaurant for lunch on the site is already counted as being parked for the day and would not generate addditional parking demand for the fast-food land use.

5. Apply monthly adjustments for each land use to generate parking demand profiles from January to December.

6. Add the adjusted employee and customer hourly parking demands for each land use class together. The hourly parking demand for the weekday and weekend scenarios are generated in the `Output` folder and are named `WeekdayParking.xslx` and `WeekendParking.xlsx` respectively. 


## Dependencies
- All code is written in Python 3
- Numpy
- Pandas

## File Descriptions
**Python files:**
|filename     |description      |
|---          |---              |
|calculate_shared_parking.py| Calls functions to calculate weekday and weekend parking demand|
|get_inputs.py| Two functions, one to get directory containing input and output folders from user terminal input and one function to read the input files|
|LandUse.py| Contains LandUse Class and associated calculations, dataframe manipulations, and output formatting|

<br>

**Input files:**
|filename     |description      |
|---          |---              |
|BaseParkingDemand.csv| Unadjusted parking demand for each land use class|
|CustomerEmployeeSplit.csv| Proportions of customers to employees for each land use class, weekday and weekend values|
|MonthlyAdjustment.csv| Adjustment factors for Jan to Dec for each land use class, one set of factors for both customers and employees, no weekday/weekend distinction|
|NoncaptiveAdjustmentWeekday.csv| Adjustment factors for non-captive market effects for each land use class, one set of factors each for customers and employees, weekday values only|
|NoncaptiveAdjustmentWeekend.csv| Adjustment factors for non-captive market effects for each land use class, one set of factors each for customers and employees, weekend values only|
|TimeOfDayWeekday.csv| Adjustment factors for temporal demand variation for each land use class, one set of factors each for customers and employees, weekday values only|
|TimeOfDayWeekend.csv| Adjustment factors for temporal demand variation for each land use class, one set of factors each for customers and employees, weekend values only|

<br>

**Output files:**
|filename     |description      |
|---          |---              |
|WeekdayParking.xlsx| Spreadsheet grouped by month, contains weekday hourly parking demand broken down by land use class, contains total column |
|WeekdendParking.xlsx| Spreadsheet grouped by month, contains weekend hourly parking demand broken down by land use class, contains total column |


## Credits
Author: Joshua Cayanan

The methodology is adapted from [Shared Parking (Third Edition)](https://uli.bookstore.ipgbook.com/shared-parking-products-9780874204278.php) by Mary Smith, published by the Urban Land Institute. 

_Car Parking_ icon made by [monkik](https://www.flaticon.com/free-icon/parking_2503520) from [www.flaticon.com](www.flaticon.com)
<br>
_Calculator_ icon made by [srip](https://www.flaticon.com/free-icon/calculator_2344291) from [www.flaticon.com](www.flaticon.com)

## To-Do List
- [x] Complete description of files section in README
- [x] Add flowchart of calculation process
- [ ] Add feature that plots maximum total parking demand per month as a line graph
- [ ] Add feature that identifies 85th percentile total parking demand
- [ ] Add graphing feature that plots stacked bar chart of the 85th percentile month and the busiest month
- [ ] Add feature that asks the user for the current working directory
- [ ] Add GUI

## License
This project is licensed under the terms of the [MIT License](https://github.com/joshuacayanan/SharedParkingCalculator/blob/master/LICENSE).
