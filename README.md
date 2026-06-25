# NPL 2025 Match Outcome Predictor

This project analyzes Nepal Premier League match data and provides a simple Streamlit app for predicting match winners from match features.

## Project structure

- `NPL2025/data_loader.py` - loads Cricsheet-style CSV match files into match and delivery tables.
- `NPL2025/model.py` - runs the statistical analysis, trains the logistic regression model, and saves outputs.
- `app.py` - Streamlit app for interactive winner prediction.
- `NPL2025/outputs/` - generated CSV files, plots, and the trained model.
- `*.csv` in the repository root - raw match data.

## What it does

- Loads and cleans match data.
- Performs statistical analysis such as chi-square testing, ANOVA, and logistic regression.
- Saves model artifacts and diagnostic plots.
- Lets you predict whether the batting side or bowling side is more likely to win using Streamlit.

## Requirements

Python 3.11+ and these libraries:

- pandas
- matplotlib
- seaborn
- scipy
- scikit-learn
- statsmodels
- streamlit

## How to run

### 1. Generate the processed data and model

```powershell
python NPL2025\data_loader.py
python NPL2025\model.py
```

### 2. Start the app

```powershell
streamlit run app.py
```

## Notes

- The app expects `NPL2025/outputs/logistic_regression_model.pkl` to exist.
- The raw CSV files in the repository root are used to build the processed datasets in `NPL2025/outputs/`.
# NPL_Predictor
