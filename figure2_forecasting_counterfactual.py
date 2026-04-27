# scripts/figure2_forecasting_counterfactual.py
# Figure 2 for npj Quantum Information paper

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from statsmodels.tsa.filters.hp_filter import hpfilter
import matplotlib.pyplot as plt
from google.colab import files

OMEGA = 0.1158
TRAIN_END_YEAR = 2017
TEST_START_YEAR = 2018
DAMPING_INCREASE = 2.0

print("Upload EPI Productivity-Pay Gap file")
uploaded = files.upload()
epi_file = list(uploaded.keys())[0]

# Load data
if epi_file.endswith(('.xlsx','.xls')):
    df = pd.read_excel(epi_file)
else:
    df = pd.read_csv(epi_file)

# Auto-detect year and value columns
year_col = [col for col in df.columns if str(col).lower() in ['year', 'date', 'time']][0]
df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
df = df.dropna(subset=[year_col]).reset_index(drop=True)

if 'Productivity' in df.columns and 'Hourly Compensation' in df.columns:
    df['pay_gap'] = df['Productivity'] - df['Hourly Compensation']
    value_col = 'pay_gap'
else:
    value_col = df.select_dtypes(include=[np.number]).columns[-1]

years = df[year_col].values
series = df[value_col].astype(float).values

# Train / Test split
train_mask = years <= TRAIN_END_YEAR
years_train = years[train_mask]
series_train = series[train_mask]
years_test = years[~train_mask]
series_test = series[~train_mask]

# Resonant model
def resonant_model(t, A, phi, gamma, trend_slope, trend_intercept):
    return A * np.exp(-gamma * (t - years_train[0])) * np.sin(OMEGA * (t - years_train[0]) + phi) + trend_slope * (t - years_train[0]) + trend_intercept

p0 = [np.std(series_train)*0.8, 0.0, 0.015, 0.0, series_train.mean()]
popt, _ = curve_fit(resonant_model, years_train, series_train, p0=p0, maxfev=20000)

# Baselines
lin_slope, lin_intercept = np.polyfit(years_train, series_train, 1)
def linear_predict(t): 
    return lin_slope * (t - years_train[0]) + lin_intercept

# Forecast
forecast_years = years_test.copy()
resonant_fc = resonant_model(forecast_years, *popt)
linear_fc = linear_predict(forecast_years)

# Counterfactual (2x damping)
popt_cf = popt.copy()
popt_cf[2] *= DAMPING_INCREASE
cf_fc = resonant_model(forecast_years, *popt_cf)

# Plot Figure 2
plt.figure(figsize=(12, 7), dpi=300)
plt.plot(years_train, series_train, 'o-', color='#1f77b4', ms=4, label='Training data (≤2017)')
plt.plot(years_test, series_test, 'o-', color='black', ms=4, label='Actual data (2018–2025)')
plt.plot(forecast_years, resonant_fc, '--', color='red', lw=2.8, label='Resonant model forecast')
plt.plot(forecast_years, linear_fc, '-.', color='gray', lw=1.8, label='Linear baseline')
plt.plot(forecast_years, cf_fc, ':', color='green', lw=2.8, label='Counterfactual (2× reskilling)')
plt.axvline(TRAIN_END_YEAR, color='gray', ls='--', alpha=0.7)
plt.xlabel('Year', fontsize=13)
plt.ylabel('Productivity–Pay Gap (normalised)', fontsize=13)
plt.title('Out-of-Sample Forecasting and Policy Counterfactual', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('Figure2_Forecasting_Counterfactual.png', dpi=400, bbox_inches='tight')
plt.show()

print("✅ Figure 2 saved successfully!")
files.download('Figure2_Forecasting_Counterfactual.png')
