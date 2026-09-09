import pandas as pd

class naive_forecast:
    def __init__(self,train):
        self.training_data = train
        self.final_date = self.training_data.date.max()


        self.window = None
        self.prediction = self.training_data[self.training_data['date']>= self.final_date-pd.DateOffset(years=1)]

    def predict(self, window):
        date = self.final_date +pd.DateOffset(months=1)
        while date<=window:
            pred = self.prediction[self.prediction['date']== date -pd.DateOffset(years=1)]['figures']
            self.prediction = pd.concat([self.prediction,pd.DataFrame({'date':date,'figures':pred})])
            date += pd.DateOffset(months=1)

        return self.prediction[self.prediction['date'] > self.final_date]
