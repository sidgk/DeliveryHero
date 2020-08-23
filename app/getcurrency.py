import csv
import logging
import os
import re
import requests
import urllib3
import pandas as pd
import matplotlib.pyplot as plt

logging.getLogger("urllib3").setLevel(logging.WARNING)

class CurrencyDownloader():
    def __init__(self,durl,wurl):
        self.durl = durl
        self.wurl = wurl

    def checkURL(self):
        if self.durl is not None:
            response = requests.get(self.durl)
            logging.info("URL {} to download data from.".format(self.durl))
            logging.info("Checking status of given URL ...")
            if response.status_code == 200:
                logging.info("Success! {}".format( response.status_code))
            elif response.status_code == 404:
                logging.info("Not Found! {}".format(response.status_code))
            else:
                logging.info("Something went wrong URL {} with status ".format(self.durl,response.status_code))

    def downloadJsonData(self):
        response = None
        fpath = './data/downloads/currency_daily_BTC_USD.csv'
        logging.info("Data will be downloaded into {}".format(fpath))
        file_exists = os.path.isfile(fpath)

        try:
            response = requests.get(self.durl).json()
        except requests.exceptions.ConnectionError as err:
            logging.error('Connection failed- {}'.format(str(err)))
        except urllib3.exceptions.MaxRetryError as err:
            logging.error('Connection failed, Maximum retry occured {}'.format(str(err)))

        if response is not None:
            try:
                with open(fpath, 'a') as out:
                    data = response["Time Series (Digital Currency Daily)"]
                    row = dict()

                    fieldnames = ["TimeZone","aopen","bopen","ahigh","bhigh"
                                  ,"alow","blow","aclose","bclose","volume"
                                  ,"marketcap"]
                    logging.info("Columns- {}".format(fieldnames))
                    writer = csv.DictWriter(out, fieldnames=fieldnames)

                    if not file_exists:
                        writer.writeheader()
                    logging.info("{} file exists {}".format(fpath,file_exists))
                    for k,v in data.items():
                        #print(k,v)
                        row.update(TimeZone=k,
                                   aopen=v['1a. open (USD)'],
                                   bopen=v['1b. open (USD)'],
                                   ahigh=v['2a. high (USD)'],
                                   bhigh=v['2b. high (USD)'],
                                   alow=v['3a. low (USD)'],
                                   blow=v['3b. low (USD)'],
                                   aclose=v['4a. close (USD)'],
                                   bclose=v['4b. close (USD)'],
                                   volume=v['5. volume'],
                                   marketcap=v['6. market cap (USD)']
                                   )
                        logging.info("Latest currency {} to be inserted into file {}".format(row,fpath))
                        writer.writerow(row)
                    logging.info("Currency fetch success.")
            except FileNotFoundError as err:
                logging.error('Trying to download file {}'.format(str(err)))
            except Exception as err:
                logging.error('Downloading file failed due to {}'.format(str(err)))

    def downloadCSVData(self):
        response = None
        fpath = './data/downloads'
        logging.info("Data will be downloaded into {}".format(fpath))

        try:
            response = requests.get(self.wurl+"&datatype=csv")
        except requests.exceptions.ConnectionError as err:
            logging.error('Connection failed- {}'.format(str(err)))
        except urllib3.exceptions.MaxRetryError as err:
            logging.error('Connection failed, Maximum retry occured {}'.format(str(err)))

        if response is not None:
            fname = re.search('=(.*?).csv', response.headers['Content-Disposition']).group(1)+'.csv'

            try:
                with open(os.path.join(fpath, fname), 'wb') as f:
                    f.write(response.content)
                logging.info("Currency download success.")
            except FileNotFoundError as err:
                logging.error('Trying to download file {}'.format(str(err)))
            except Exception as err:
                logging.error('Downloading file failed due to {}'.format(str(err)))

    def checkAndDownloadData(self):
        self.checkURL()
        self.downloadCSVData()
        self.downloadJsonData()



class InsightCalculator():
    def __init__(self):
        pass

    def weekly_average(self):
        fname = "data/downloads/currency_daily_BTC_USD.csv"
        result_csv = "data/results/weekly_average.csv"
        result_png = "data/results/weekly_average.png"
        logging.info("Reading data from {}".format(fname))
        df = pd.read_csv(os.path.join(os.getcwd(), fname), parse_dates=['TimeZone'])

        week_df = df.groupby(df['TimeZone'].dt.to_period("W"))
        mdf = week_df['aclose'].mean()
        logging.info("Weekly average is {}".format(mdf))
        mdf.plot(kind='line')
        logging.info("Writing result to {} ".format(result_csv))
        mdf.to_csv(os.path.join(os.getcwd(), result_csv), encoding='utf-8')
        logging.info("Saving plot image result to {} ".format(result_png))
        plt.savefig(os.path.join(os.getcwd(), result_png))
        plt.close()

    def threeDaysRollingMean(self):
        fname = "data/downloads/currency_daily_BTC_USD.csv"
        result_csv = "data/results/3-days-rolling.csv"
        result_png = "data/results/3-days-rolling.png"
        logging.info("Reading data from {}".format(fname))
        df = pd.read_csv(os.path.join(os.getcwd(), fname), parse_dates=['TimeZone'])

        df['aclose'].plot()
        rdf = df['aclose'].rolling(window=3).mean()
        logging.info("Three days rolling average is {}".format(rdf))
        rdf.plot(kind='line')
        logging.info("Writing result to {} ".format(result_csv))
        rdf.to_csv(os.path.join(os.getcwd(), result_csv), encoding='utf-8')
        logging.info("Saving plot image result to {} ".format(result_png))
        plt.savefig(os.path.join(os.getcwd(), result_png))
        plt.close()

    def sevenDaysRollingMean(self):
        fname = "data/downloads/currency_daily_BTC_USD.csv"
        result_csv = "data/results/7-days-rolling.csv"
        result_png = "data/results/7-days-rolling.png"
        logging.info("Reading data from {}".format(fname))
        df = pd.read_csv(os.path.join(os.getcwd(), fname), parse_dates=['TimeZone'])

        df['aclose'].plot()
        rdf = df['aclose'].rolling(window=7).mean()
        logging.info("Seven days rolling average is {}".format(rdf))
        rdf.plot(kind='line')
        logging.info("Writing result to {} ".format(result_csv))
        rdf.to_csv(os.path.join(os.getcwd(), result_csv), encoding='utf-8')
        logging.info("Saving plot image result to {} ".format(result_png))
        plt.savefig(os.path.join(os.getcwd(), result_png))
        plt.close()

    def calculate_insights(self):
        self.weekly_average()
        self.threeDaysRollingMean()
        self.sevenDaysRollingMean()