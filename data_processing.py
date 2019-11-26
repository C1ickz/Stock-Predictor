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
df = pd.read_csv('datasets/tesla.csv')  # TODO make so user can choose csv
df = df.set_index(df['Date'])
dataset = df['Adj Close'].values
most_recent = pd.Timestamp(df['Date'].max())
trainingRange = str(most_recent - dt.timedelta(days=40))
train = df.loc[:trainingRange, ['Adj Close']]
test = df.loc[trainingRange:, ['Adj Close']]
scaler = MinMaxScaler(feature_range=(0, 1))  # set values between 0 and 1
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)


def to_sequences(obs, window_size):
    x = []
    y = []

    for i in range(len(obs) - window_size ): # -1
        window = obs[i:(i + window_size)]
        x.append(window)
        y.append(obs[i + window_size])
    return np.array(x), np.array(y)


X_train, Y_train = to_sequences(train_scaled, 5)
X_test, Y_test = to_sequences(test_scaled, 5)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
print(X_test)
print("=============================================================")
print(f"tests shape is {test.shape}; X_trains shape is {X_train.shape} ; X_Tests shape is {X_test.shape}")
print("================================================================================")
print(X_train.shape, Y_train.shape)
model = Sequential()
model.add(LSTM(16, input_shape=(X_train.shape[1], 1), activation='relu'))
model.add(Dropout(.2))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy']) # adagrad?
monitor = EarlyStopping(monitor='loss', min_delta=1e-3, patience=10,
                        verbose=1, mode='auto', restore_best_weights=True)

model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
          callbacks=[monitor], verbose=1, epochs=200)
print("Shape of X_test", X_test.shape)


# TODO Move code for predictions somewhere else


dataset = dataset.reshape(len(dataset), 1)
print(f"{len(train)} {len(test)}")
print(f"{X_train.shape} {X_test.shape}")
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
train_predict_plot = np.empty_like(dataset)
print(f"{train_predict.shape} to {test_predict.shape} to {len(dataset)}")
train_predict_plot[:, :] = np.nan
train_predict_plot[5:len(train_predict) + 5, :] = train_predict

test_predict_plot = np.empty_like(dataset)
test_predict_plot[:, :] = np.nan
test_predict_plot[len(train_predict) + (5 * 2) : len(dataset) , :] = test_predict

plt.title("Stocks for TSLA")

print(f"Test predict plots shape is {test_predict_plot.shape}")
plt.plot(df['Date'], train_predict_plot)
plt.plot(df['Date'], test_predict_plot)
plt.tight_layout()
plt.gcf().autofmt_xdate()

plt.show()
