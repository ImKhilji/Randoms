import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller


def is_stationary(ts, test_window):
	"""
	This function checks whether the given TS is stationary. Can make it boolean, but lets just leave it
	for visualisation purposes. Not to be run once the numbers have been fixed.
	"""

	# Determine the rolling statistics (places like these compelled me to use Pandas and not numpy here)
	rol_mean = pd.rolling_mean(ts, window=test_window)
	rol_std = pd.rolling_std(ts, window=test_window)

	#Plot rolling statistics:
	orig = plt.plot(ts, color='blue',label='Original')
	mean = plt.plot(rol_mean, color='red', label='Rolling Mean')
	std = plt.plot(rol_std, color='black', label = 'Rolling Std')
	plt.legend(loc='best')
	plt.title('Rolling Mean & Standard Deviation')
	plt.show()

	# Perform the  Dickey-Fuller test: (Check documentation of fn for return params)
	print 'Results of Dickey-Fuller Test:'
	dftest = adfuller(timeseries, autolag='AIC')
	dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
	for key,value in dftest[4].items():
		dfoutput['Critical Value (%s)'%key] = value
	print dfoutput



#if __name__ == '__main__':
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
# The above is a function!

data = pd.read_csv('AirPassengers.csv', parse_dates='Month', index_col='Month',date_parser=dateparse)
# print and check the format. Unlike numpy, the entries can now be called by dates,
# which is the first column.
timeseries = data['#Passengers'] # Note that this is the head of the CSV
# plt.plot(timeseries)
# plt.show()
# is_stationary(timeseries, 12)
# is_stationary(np.log(timeseries), 12)

ts_log = np.log(timeseries)
moving_avg = pd.rolling_mean(ts_log,12)
# plt.plot(ts_log)
# plt.plot(moving_avg, color='red')
#plt.show()
ts_log_moving_avg_diff = ts_log - moving_avg
ts_log_moving_avg_diff.dropna(inplace=True) # Pandas in action :p
# after the above, make sure that the test_statistic is lesser than the critical value.
# For this you can run is_stationary again.
# is_stationary(ts_log_moving_avg_diff, 12)

expwighted_avg = pd.ewma(ts_log, halflife=12)
# Exponential weights make sure that recent observations have more importance

ts_log_ewma_diff = ts_log - expwighted_avg
# test_stationarity(ts_log_ewma_diff)
# On testing, apparently this has a lower test statistic value and hence
# better as a stationary series

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts_log)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# Sorry for the inconvenience, this code is incomplete