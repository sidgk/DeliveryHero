import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

logging.getLogger("urllib3").setLevel(logging.WARNING)

def weekly_average():
    fname = "data/downloads/currency_daily_BTC_USD.csv"
    result_csv = "data/results/weekly_average.csv"
    result_png = "data/results/weekly_average.png"
    logging.info("Reading data from {}".format(fname))
    df = pd.read_csv(os.path.join(os.pardir,fname),parse_dates=['TimeZone'])

    week_df = df.groupby(df['TimeZone'].dt.to_period("W"))
    mdf = week_df['aclose'].mean()
    logging.info("Weekly average is {}".format(mdf))
    mdf.plot(kind='line')
    logging.info("Writing result to {} ".format(result_csv))
    mdf.to_csv(os.path.join(os.pardir,result_csv), encoding='utf-8')
    logging.info("Saving plot image result to {} ".format(result_png))
    plt.savefig(os.path.join(os.pardir,result_png))
