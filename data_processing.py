from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import EarlyStopping

# This python file will process the data and train it.
# No prediction will be done in here

df = pd.read_csv('tesla.csv')  # TODO make so user can choose csv
df = df.set_index(df['Date'])
most_recent = pd.Timestamp(df['Date'].max())
trainingRange = str(most_recent - dt.timedelta(days=7))
train = df.loc[:trainingRange, ['Adj Close']]
test = df.loc[trainingRange:, ['Adj Close']]
scaler = MinMaxScaler(feature_range=(0, 1))  # set values between 0 and 1
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)

X_train = train_scaled[:-1]
Y_train = train_scaled[1:]
X_test = test_scaled[:-1]
Y_test = test_scaled[1:]
print(X_train.shape, Y_train.shape)
model = Sequential()
model.add(Dense(12, input_dim=1, activation='relu'))  # tanh also works but relu provides best results
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
monitor = EarlyStopping(monitor='loss', min_delta=1e-3, patience=10,
                        verbose=1, mode='auto', restore_best_weights=True)
model.fit(X_train, Y_train, callbacks=[monitor], verbose=2, epochs=200)

# TODO Move code for predictions somewhere else
prediction = model.predict(X_test)
plt.plot(Y_test)
plt.plot(prediction)
plt.show()
