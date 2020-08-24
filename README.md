# DeliveryHero


## Prerequisites

```
pip install requests
pip install responses
pip install urllib3
pip install configparser
pip install pandas
pip install unittest
pip install matplotlib

OR 

pip install -r requirements.txt --> Because i have added all the required packages in requirements.txt.

```
# Summary
1. Initialy download the data from the AlphaVintage API's for daily and weekly data and saving it to currency_daily_BTC_USD.csv and currency_weekly_BTC_USD.csv files respectively.
2. Perform calculations (average price of each week, 3-day and 7-day rolling average) on the data saved in currency_daily_BTC_USD.csv file and store the visulizations and reports under **results folder**. 
3. Logic to perform actions in first two steps are written in **getcurrency.py file** .
4. In **main.py** file Airflow DAG is created and all the functions created to perform the relevant actions in gutcurrency.py file are called in the main.py file. 
5. A logger is written in main.py file with the appropriate log messsage and current time of execution to log/track every line of execution of the program and all the logs are stored in myapp.log file under logs folder. Reviewing logs regularly could help identify program execution flow and failuers with appropriate messages.
6. The average price of each week, 3-day and 7-day rolling average calculations are carried out and written saperately in 3_day_rolling_insights.py, 7_day_rolling_insights.py, weekely_insights.py files in **app folder**.
7. **config.ini** --> This file contains all the confidential details about the application, and it can be accessed by referencing to this file by using _ConfigParser_ module.
8. Entire application is containerized using docker-compose and the same is written in **docker-compose.yml** file.

# How to run the application 
You can run the entire application using one command i.e. **docker-compose up** 

