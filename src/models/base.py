import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error # pyright: ignore[reportMissingModuleSource]

from naive import naive_forecast


DF =pd.read_csv("data/clean/Table_9/combined.csv")
DF['date'] = pd.to_datetime(DF['date'])



heathrow = DF[DF['reporting_airport_name'].str.lower().str.strip(" ")=="heathrow"]


heathrow = heathrow[['date','total_pax_this_period']]
heathrow = heathrow.rename(columns={'total_pax_this_period':'figures'})


def train_test_split(y,data):
    cutoff = pd.Timestamp.today() - pd.DateOffset(years=y)

    train_data = data[data['date'] <cutoff]
    test_data = data[data['date']>=cutoff]

    return train_data, test_data

def plot_against_data(data,prediction):
    fig = plt.plot(data['date'],data['figures'])
    plt.plot(prediction['date'],prediction['figures'], color='red')
    plt.show()

def model_evaluation(pred, test_data):
    print (f"Prediction error: {mean_absolute_percentage_error(test_data['figures'],pred['figures'])}")

train, test = train_test_split(2,heathrow)

model = naive_forecast(train)

pred = model.predict(test['date'].max())


model_evaluation(pred, test)
plot_against_data(heathrow,pred)

