import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

data = pd.read_csv('final_dataset.csv')

data['Issue Date'] = pd.to_datetime(data['Issue Date'], format='%Y-%m-%d')
data.set_index('Issue Date', inplace=True)
data = data.loc['2014':]
data = data.loc[:'2017']

precinct_data = data[['Violation Precinct', 'count']]

precinct_data = precinct_data.groupby(['Violation Precinct', pd.Grouper(freq='M')]).sum()
precinct_data = precinct_data.loc[:123]
precinct_data.to_csv("aggregated_dataset.csv")

precinct_matrix = precinct_data.unstack(level=0)

pred_df = pd.DataFrame()

for precinct in precinct_matrix.columns:
    ts = precinct_matrix[precinct].dropna()
    if len(ts) > 9:
        model = ARIMA(ts, order=(1, 1, 1))
        results = model.fit()

        forecast = results.predict(steps=12)
        
        pred_df = pd.merge(pred_df, forecast[1:], how = 'outer', left_index=True, right_index=True)
        pred_df = pred_df.rename(columns={"predicted_mean": precinct[1]})

#         plt.plot(forecast[1:], label='Predicted')
#         plt.plot(ts[:-12], label='Actual')

#         plt.title(f'Precinct {precinct[1]} Parking Ticket Counts')
#         plt.xlabel('Date')
#         plt.ylabel('Ticket Count')

#         plt.legend()
#         plt.show()

pred_df = pred_df.rename(columns={"Issue Date": "Date"})
pred_df.to_csv("arima.csv")