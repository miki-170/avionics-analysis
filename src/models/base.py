import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import root_mean_squared_error

data =pd.read_csv("data/clean/Table_9/combined.csv")
data['date'] = pd.to_datetime(data['date'])


train_data = data[data['date'].dt.year <2024]
test_data = data[data['date'].dt.year>=2024]

def model_evaluation(pred, column):
    return f"Prediction error: {root_mean_squared_error(pred[column],test_data[column])}"
