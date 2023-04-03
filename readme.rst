Revenue Forecast
==========

# About the Project

This project will process the datasets available in data--> input--> data.xlsx, will do the following:
* convert_xlsx_csv will convert data.xlsx to sheet1.csv(dataset A), sheet2.csv(dataset B), sheet3.csv(dataset C) 
* TaskA will forecast the subscription growth and generates csv files in data --> output folder. 
    * taskA_subcription_growth.csv  will provide insight subscription growth during the year 2023
    * TaskA_ARR_per_month will provide summarized revenue per TaskA_ARR_per_month
    
* TaskB will process sheet1.csv(dataset A), sheet2.csv(dataset B), sheet3.csv(dataset C) and generates csv files in data --> output folder
    * TaskB_sheet(1/2/3).csv will provide cash in bank per day
    * TaskB_cummulative_sum.csv will provide total cash in bank combining all datasets

* helper python file is a placeholder to hold all utility functions. It holds write_to_csv function to write data to csv files
Libraries
------------

This project uses Python standard library

Assumptions
-----------

* This project was intended to run Windows machine. To make the code in unix machine, pathlib.PureWindowsPath in all files needs to be updated
* This code is intended to process small amount of dataset, therefore the processed rows are stored in memory and later written to csv files. In case, larger datasets to be processed then code needs to be improvised.
* The revenue generated across all tasks is in USD. As per Google, used 1 GBP = 1.23 USD as conversion rate

Next Steps
---------

Unit tests



