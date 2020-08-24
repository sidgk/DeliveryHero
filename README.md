# DeliveryHero

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  
* [Getting Started](#getting-started)
  * [Prerequisites](#Prerequisites)
* [Summary](#Summary)
* [Running the Application](#Running-the-Application)

<!-- ABOUT THE PROJECT -->
## About The Project

* Collect the cryptocurrency data by accessing the API provided by Alpha Vantage.
* We are collecting data from two sources. Refer congig.ini file under config folder to access the URL's.
    1) DURL - Provides the daily data
    2) WURL - Provides the weekely data
*  I am performing all the calculations (average price of each week, 3-day and 7-day rolling average) and referig to only daily cryptocurrency data that is saved as       currency_daily_BTC_USD.csv file under data/downloads folder. 
* Collect the data and store it in CSV format.
* Perform calculations suggested in case study.
* Schedule and Author it using Apache Airflow.
* Containerize the application.
* Run the container.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

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
## Summary

1. Initialy download the data from the AlphaVintage API's for daily and weekly data and saving it to currency_daily_BTC_USD.csv and currency_weekly_BTC_USD.csv files respectively.
2. Perform calculations (average price of each week, 3-day and 7-day rolling average) on the data saved in currency_daily_BTC_USD.csv file and store the visulizations and reports under **results folder**. 
3. Logic to perform actions in first two steps are written in **getcurrency.py file** .
4. In **main.py** file Airflow DAG is created and scheduled to run the program for every one hour and all the functions defined to perform the relevant actions in gutcurrency.py file are called in the main.py file. 
5. A logger is written in main.py file with the appropriate log messsage and current time of execution to log/track every line of execution of the program and all the logs are stored in myapp.log file under logs folder. Reviewing logs regularly could help identify program execution flow and failuers with appropriate messages.
6. The average price of each week, 3-day and 7-day rolling average calculations are carried out and written saperately in 3_day_rolling_insights.py, 7_day_rolling_insights.py, weekely_insights.py files in **app folder**.
7. **config.ini** --> This file contains all the confidential details about the application, and it can be accessed by referencing to this file by using _ConfigParser_ module.
8. The unittest to check the status of the URL's (durl and wurl) provided is written in **getcurrency_test.py**. 
9. Entire application is containerized using docker-compose and the same is written in **docker-compose.yml** file.
10. I have used the puckel docker image to run my airflow 

<!-- Running the Application -->
## Running the Application
You can run the entire application using one command i.e. **docker-compose up** 

