import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

logging.getLogger("urllib3").setLevel(logging.WARNING)

df = pd.read_csv(os.path.join(os.pardir,"data/downloads/currency_daily_BTC_USD.csv"),parse_dates=['TimeZone'])

df['aclose'].plot()
rdf = df['aclose'].rolling(window=7).mean()
rdf.plot(kind='line')
rdf.to_csv(os.path.join(os.pardir,"data/results/7-days-rolling.csv"), encoding='utf-8')
plt.savefig(os.path.join(os.pardir,"data/results/7-days-rolling.png"))

print(rdf.head())