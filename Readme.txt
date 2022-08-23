Please read this before executing the assignment:-

Plugins-
Software: python3(.sh files run python3 files)

Dependencies-
Python Libraries: pandas, numpy, json, datetime,

Programs-

.sh files:

assign1.sh 
  Top level script that runs the entire assignment

neighbor-modifier.sh(No naming convention was given for Question1)
  Runs Question1.py python file
  Generates neighbor-districts-modified.json 

edge-generator.sh
  Runs Question2.py python file
  Generates edge-graph.csv

case-generator.sh
  Runs Question3.py python file
  Generates week-cases-time.csv,month-case-time.csv,overall-case-time.csv

peaks-generator.sh
  Runs Question4.py python file
  Generates district-peaks.csv, state-peaks.csv

vaccinated-count-generator.sh
  Runs Question5.py python file
  Generates district-weekly-vaccinated-count-time.csv, district-monthly-vaccinated-count-time.csv,
            district-overall-vaccinated-count-time.csv, state-weekly-vaccinated-count-time.csv,
            state-monthly-vaccinated-count-time.csv, state-overall-vaccinated-count-time.csv

vaccination-population-ratio-generator.sh
  Runs Question6.py python file
  Generates district-vaccination-population-ratio.csv,state-vaccination-population-ratio.csv,
            india-vaccination-population-ratio.csv

vaccine-type-ratio-generator.sh
  Runs Question7.py python file
  Generates district-vaccine-type-ratio.csv, state-vaccine-type-ratio.csv,
            india-vaccine-type-ratio.csv

vaccinated-ratio-generator.sh
  Runs Question8.py python file
  Generates district-vaccinated-dose-ratio.csv, state-vaccinated-dose-ratio.csv,
            india-vaccinated-dose-ratio.csv

complete-vaccination-generator.sh
  Runs Question9.py python file
  Generates complete-vaccination.csv

How to use:
To run the whole assignment at once run the following command from the terminal-
bash assign1.sh 

To run each code seperately run the following command from the terminal-
bash FILE_NAME.sh
where FILE_NAME is the name of the .sh file you want to run

Output-
All the output files generated are stored in the 'Outputs' folder.


In question 4, for some districts and states there were not enough cases to cause a peak in either wave1 or wave2 or both. For such cases I have used -1 to represent that there
is no wave.

In question 7, for some districts and states no covaxin doses were administered so the ratio for those districts and state is shown as 'inf'.

In question 9, for some states the number of vaccinated people already crossed the total population before 14/08/2021 thus, for those states the populationleft column shows negative values.
The date column shows the date in "dd-mm-yy" pattern.

For each question whose output required seperate csv file for district, state and overall, week, month data, I have added district, state and overall, week, month to the name of 
those output files.


Some points to keep in mind:

If any sh file does not execute please change permissions for the file and try again.

All the python programs and the datasets are provided in the same folder. Python program are named q1,q2,q3, and so on for each question repectively

Along with all the datasets provided for this assignment I have created a dataset vaccine_data_new.csv to correct the irregularaties cumulation of vaccination dataset.
   
Please keep all the python programs, the datasets and the CSV files folder within the same directory otherwise, there will be execution errors.

Please do not use any dataset other than those provided by me as I have removed some Null values from the dataset manually and the programming is done with these datasets in
consideration.

As I have done complete assignment on Jupyter Notebook so I have also added a Jupyte notebooks folder to notebooks in case you want to run code in notebook format.

I have tried to explain everything in my code using comments, if still in case you face any problem feel free to contact me.
