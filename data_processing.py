from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import EarlyStopping

# This python file will process the data and train it.
# No prediction will be done in here
df = pd.read_csv('tesla.csv')  # TODO make so user can choose csv
df['Date'] = pd.to_datetime(df['Date'])
dataset = list(zip(df['Date'], df['Adj Close'].values))
most_recent = pd.Timestamp(df['Date'].max())
print(most_recent)
trainingRange = str(most_recent -  dt.timedelta(days=20))
print(f"Train is using the data between {df['Date'].min()} and {(most_recent - dt.timedelta(days=20))}")
print(f"Test is using the data between {most_recent - dt.timedelta(days=20)} and {most_recent}")
trainingRange = str(trainingRange.split(" ", 1)[0])
print("Training range =", trainingRange)
train = df.loc[:'2019-10-17', 'Adj Close']
#test = df.loc[trainingRange:, df['Adj Close']]
print(len(train))
scaler = MinMaxScaler(feature_range=(0, 1))  # set values between 0 and 1
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)


def to_sequences(data, window_size):
    x = []
    y = []

    for i in range(len(data) - window_size - 1):
        window = data[i:(i + window_size), 0]
        x.append(window)
        y.append(data[i + window_size, 0])
    return np.array(x), np.array(y)


WINDOW_SIZE = 10
X_train, Y_train = to_sequences(train_scaled, WINDOW_SIZE)
X_test, Y_test = to_sequences(test_scaled, WINDOW_SIZE)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
print(X_test)
print("=============================================================")
print(f"tests shape is {test.shape}; X_trains shape is {X_train.shape} ; X_Tests shape is {X_test.shape}")
print("================================================================================")
print(X_train.shape, Y_train.shape)
model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1], 1), return_sequences=True, activation='relu'))
model.add(Dropout(.2))
model.add(LSTM(32))
model.add(Dropout(.2))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])  # adagrad?
monitor = EarlyStopping(monitor='loss', patience=10, verbose=1, restore_best_weights=True)
model.fit(X_train, Y_train, callbacks=[monitor], epochs=200)

# TODO Move code for predictions somewhere else
original = pd.DataFrame(dataset, columns=['Date', 'Adj Close'])
original = original.set_index('Date')
print(original)
print(f"{len(train)} {len(test)}")
print(f"{X_train.shape} {X_test.shape}")
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
train_predict_plot = np.empty_like(dataset)
train_predict_plot[:, :] = np.nan
train_predict_plot[WINDOW_SIZE:len(train_predict) + WINDOW_SIZE, :] = train_predict

test_predict_plot = np.empty_like(dataset)
test_predict_plot[:, :] = np.nan
test_predict_plot[len(train_predict) + (WINDOW_SIZE * 2) + 1: len(dataset) - 1, :] = test_predict
plt.title("Stocks for TSLA")

print(f"Test predict plots shape is {test_predict_plot.shape}")
plt.plot(df['Date'], train_predict_plot)
plt.plot(df['Date'], test_predict_plot)
plt.plot(df['Date'], df['Adj Close'])
plt.xlabel('Date')
plt.ylabel('Adj Close Price')
plt.tight_layout()
plt.gcf().autofmt_xdate()

plt.show()
