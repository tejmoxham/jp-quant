
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import date, timedelta

# Load data into pandas dataframe
start_date = date(2020,10,31)
end_date = date(2024,9,30)
extrap_data = date(2025,9,30)
date_time = ["10-2020", "11-2020", "12-2020"]
date_time = pd.to_datetime(date_time)
data = [1, 2, 3]
df = pd.read_csv('./data/nat_gas.csv', parse_dates=['Dates'])
prices = df['Prices'].values
dates = df['Dates'].values

# Convert dates into days from the start
months = []
year = start_date.year
month = start_date.month + 1
while True:
    current = date(year, month, 1) + timedelta(days=-1)
    months.append(current)
    if current.month == end_date.month and current.year == end_date.year:
        break
    else:
        month = ((month + 1) % 12) or 12
        if month == 1:
            year += 1        
days_from_start = [(day - start_date ).days for day in months]

# Linear regression fitting
def simple_regression(x, y):
    xbar = np.mean(x)
    ybar = np.mean(y)
    slope = np.sum((x - xbar) * (y - ybar))/ np.sum((x - xbar)**2)
    intercept = ybar - slope*xbar
    return slope, intercept

time = np.array(days_from_start)
slope, intercept = simple_regression(time, prices)

# Use bilinear regression, with no intercept, to solve for u = Acos(z), w = Asin(z)
sin_prices = prices - (time * slope + intercept)
sin_time = np.sin(time * 2 * np.pi / (365))
cos_time = np.cos(time * 2 * np.pi / (365))

def bilinear_regression(y, x1, x2):
    # Bilinear regression without an intercept amounts to projection onto the x-vectors
    slope1 = np.sum(y * x1) / np.sum(x1 ** 2)
    slope2 = np.sum(y * x2) / np.sum(x2 ** 2)
    return(slope1, slope2)

slope1, slope2 = bilinear_regression(sin_prices, sin_time, cos_time)
amplitude = np.sqrt(slope1 ** 2 + slope2 ** 2)
shift = np.arctan2(slope2, slope1)

# Define the interpolation/extrapolation function
def interpolate(date):
    days = (date - pd.Timestamp(start_date)).days
    if days in days_from_start:
        # Exact match found in the data
        return prices[days_from_start.index(days)]
    else:
        # Interpolate/extrapolate using the sin/cos model
        return amplitude * np.sin(days * 2 * np.pi / 365 + shift) + days * slope + intercept

def future_price_function(start_date, extrap_data):
    x = np.array(days_from_start)
    y = np.array(prices)
    fit_amplitude = np.sqrt(slope1 ** 2 + slope2 ** 2)
    fit_shift = np.arctan2(slope2, slope1)
    fit_slope, fit_intercept = simple_regression(x, y - fit_amplitude * np.sin(x * 2 * np.pi / 365 + fit_shift))
    continuous_dates = pd.date_range(start=pd.Timestamp(start_date), end=pd.Timestamp(extrap_data), freq='D')
    fit_prices = fit_amplitude * np.sin((continuous_dates - pd.Timestamp(start_date)).days * 2 * np.pi / 365 + fit_shift) + (continuous_dates - pd.Timestamp(start_date)).days * fit_slope + fit_intercept
    return continuous_dates, fit_prices





