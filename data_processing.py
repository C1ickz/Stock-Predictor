from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


# This python file will process the data and train it.
# No prediction will be done in here

df = pd.read_csv('tesla.csv') #TODO make so user can choose csv
df = df.set_index(df['Date'])
most_recent = pd.Timestamp(df['Date'].max())
trainingRange = str(most_recent - dt.timedelta(days= 2))
train = df.loc[:trainingRange, ['Adj Close']]
test = df.loc[trainingRange:, ['Adj Close']]
scaler = MinMaxScaler()
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)

