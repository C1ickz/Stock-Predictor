from data_processing import data_loader
from data_processing import train_test_split
from data_processing import data_scaler
from data_processing import generate_sets
from data_processing import build_model

# TODO: Move this to different file
from data_processing import graph_format
from data_processing import graph_data

df, dataset = data_loader('tesla.csv')

train, test = train_test_split(df, dataset)

train_scaled, test_scaled = data_scaler(train, test)

X_train, Y_train, X_test, Y_test = generate_sets(train_scaled, test_scaled)

model = build_model(X_train, Y_train)

train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

train_predict_plot, test_predict_plot = graph_format(dataset, train_predict, test_predict)

graph_data(df, train_predict_plot, test_predict_plot)
