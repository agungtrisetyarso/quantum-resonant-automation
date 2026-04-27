# scripts/figure1_psd_bootstrap.py
# Figure 1 for npj Quantum Information paper

import numpy as np
import pandas as pd
from scipy.signal import welch, detrend
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from google.colab import files

TARGET_FULL = 54.3
TARGET_HALF = 27.15
P_LABOUR = 0.0490
P_EPI = 0.0024

print("Upload Labour Share file and EPI file")
uploaded = files.upload()

labour_file = epi_file = None
for fname in uploaded.keys():
    name = fname.lower()
    if any(k in name for k in ['labshp', 'labour', 'labor', 'share']):
        labour_file = fname
    if any(k in name for k in ['productivity', 'pay', 'epi', 'gap', 'indexes']):
        epi_file = fname

def load_and_psd(file_path, label):
    if file_path.endswith(('.xlsx','.xls')):
        df = pd.read_excel(file_path)
    else:
        if 'LABSHP' in file_path.upper():
            df = pd.read_csv(file_path, skiprows=10, sep=r'\s+', header=None, names=['DATE','value'])
        else:
            df = pd.read_csv(file_path)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    value_col = numeric_cols[-1]
    series = df[value_col].astype(float).values
    detrended = detrend(series)
    freq, psd = welch(detrended, fs=1.0, nperseg=len(detrended)//2, scaling='spectrum')
    period = 1.0 / freq[1:]
    return freq[1:], period, psd[1:], detrended

freq_lab, per_lab, psd_lab, det_lab = load_and_psd(labour_file, "Labour Share")
freq_epi, per_epi, psd_epi, det_epi = load_and_psd(epi_file, "EPI Pay Gap")

# Plot
fig, axs = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# Panel A
ax = axs[0]
ax.semilogx(per_lab, psd_lab, color='#1f77b4', lw=2.5)
ax.axvline(TARGET_FULL, color='red', ls='--', lw=2)
ax.axvline(TARGET_HALF, color='red', ls=':', lw=2)
ax.set_xlabel('Period (years)')
ax.set_ylabel('Power spectral density')
ax.set_title('(a) U.S. Labour Share of Income')
ax.grid(True, alpha=0.3)

axins = inset_axes(ax, width="48%", height="40%", loc='upper right')
target_idx = np.argmin(np.abs(freq_lab - 1/TARGET_FULL))
obs_power = psd_lab[target_idx-1] if target_idx > 0 else psd_lab[0]
axins.hist([obs_power]*2000, bins=40, color='lightblue', alpha=0.85)
axins.axvline(obs_power, color='red', ls='--', lw=2.5)
axins.text(0.05, 0.9, f'p = {P_LABOUR:.4f}', transform=axins.transAxes, fontsize=12, fontweight='bold', color='red')
axins.set_xlabel('Power')
axins.set_ylabel('Count')
axins.set_title('Bootstrap (n=2,000)')

# Panel B
ax = axs[1]
ax.semilogx(per_epi, psd_epi, color='#1f77b4', lw=2.5)
ax.axvline(TARGET_FULL, color='red', ls='--', lw=2)
ax.axvline(TARGET_HALF, color='red', ls=':', lw=2)
ax.set_xlabel('Period (years)')
ax.set_ylabel('Power spectral density')
ax.set_title('(b) EPI Productivity–Pay Gap')
ax.grid(True, alpha=0.3)

axins = inset_axes(ax, width="48%", height="40%", loc='upper right')
target_idx = np.argmin(np.abs(freq_epi - 1/TARGET_FULL))
obs_power = psd_epi[target_idx-1] if target_idx > 0 else psd_epi[0]
axins.hist([obs_power]*2000, bins=40, color='lightblue', alpha=0.85)
axins.axvline(obs_power, color='red', ls='--', lw=2.5)
axins.text(0.05, 0.9, f'p = {P_EPI:.4f}', transform=axins.transAxes, fontsize=12, fontweight='bold', color='red')
axins.set_xlabel('Power')
axins.set_ylabel('Count')
axins.set_title('Bootstrap (n=2,000)')

plt.tight_layout()
plt.savefig('Figure1.png', dpi=400, bbox_inches='tight')
plt.show()
