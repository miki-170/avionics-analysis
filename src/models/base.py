import pandas as pd
import matplotlib.pyplot as plt

data =pd.read_csv("data/clean/Table_9/combined.csv")

heathrow = data[data['reporting_airport_name'].str.strip(" ")=="HEATHROW"]

ax = heathrow.plot(x='date', y='total_pax_this_period')
plt.show()