from sklearn.preprocessing import MinMaxScaler
from SimpleStocksAndGraph import gatherData

scaler = MinMaxScaler(feature_range = (0,1)) #put all data between 0 and 1
