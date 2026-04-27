# Observation of Multi-Decadal Resonant Oscillations in Automation-Driven Labour–Capital Substitution

**Quantum-Inspired Resonant Dynamics**  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains all code, data analysis scripts, and notebooks for the paper:

**Trisetyarso et al.** — *Observation of Multi-Decadal Resonant Oscillations in Automation-Driven Labour–Capital Substitution*  
Submitted to *npj Quantum Information*

## Key Results
- First rigorous statistical demonstration of **multi-decadal resonant isoquant oscillations** in real macroeconomic data.
- Phase-randomized Fourier surrogate tests (10,000 realisations):  
  **p = 0.0490** (U.S. labour share) and **p = 0.0024** (EPI Productivity–Pay Gap).
- Superior out-of-sample forecasting (2018–2025): RMSE = 72.36 (vs. ~4,911 for linear trend).
- Policy counterfactual: Doubling reskilling intensity substantially damps future inequality waves.

## Repository Structure
- `notebooks/` — Google Colab notebooks for full reproduction
- `scripts/` — Python scripts to generate Figure 1 and Figure 2
- `data/` — Raw time series (FRED labour share + EPI Productivity–Pay Gap)

## How to Reproduce
```bash
pip install -r requirements.txt
