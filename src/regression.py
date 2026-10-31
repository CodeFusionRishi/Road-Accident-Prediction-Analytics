"""
Unit II: Supervised Learning — Regression
Models:
1. Simple Linear Regression (Accident Count vs Vehicle Volume)
2. Multiple Linear Regression (Accident Count vs Vehicles, Casualties, Speed Limit, Time Trend)
3. Polynomial Regression (Degree 2)
Metrics: MAE, MSE, RMSE, R-squared
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_PATH = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed\monthly_accident_regression.csv"
MODEL_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\models"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

def run_regression_analysis():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded monthly regression data: {len(df)} records (months).")
    
    # 1. Simple Linear Regression: accident_count vs total_vehicles
    X_simple = df[['total_vehicles']].values
    y = df['accident_count'].values
    
    X_train_s, X_test_s, y_train, y_test = train_test_split(X_simple, y, test_size=0.25, random_state=42)
    
    slr = LinearRegression()
    slr.fit(X_train_s, y_train)
    y_pred_slr = slr.predict(X_test_s)
    
    mae_slr = mean_absolute_error(y_test, y_pred_slr)
    mse_slr = mean_squared_error(y_test, y_pred_slr)
    rmse_slr = np.sqrt(mse_slr)
    r2_slr = r2_score(y_test, y_pred_slr)
    
    # 2. Multiple Linear Regression: features = [time_idx, total_vehicles, total_casualties, avg_speed_limit]
    feature_cols = ['time_idx', 'total_vehicles', 'total_casualties', 'avg_speed_limit']
    X_multi = df[feature_cols].values
    
    X_train_m, X_test_m, _, _ = train_test_split(X_multi, y, test_size=0.25, random_state=42)
    
    mlr = LinearRegression()
    mlr.fit(X_train_m, y_train)
    y_pred_mlr = mlr.predict(X_test_m)
    
    mae_mlr = mean_absolute_error(y_test, y_pred_mlr)
    mse_mlr = mean_squared_error(y_test, y_pred_mlr)
    rmse_mlr = np.sqrt(mse_mlr)
    r2_mlr = r2_score(y_test, y_pred_mlr)
    
    # 3. Polynomial Regression (Degree 2) on Multiple Features
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_p = poly.fit_transform(X_train_m)
    X_test_p = poly.transform(X_test_m)
    
    plr = LinearRegression()
    plr.fit(X_train_p, y_train)
    y_pred_plr = plr.predict(X_test_p)
    
    mae_plr = mean_absolute_error(y_test, y_pred_plr)
    mse_plr = mean_squared_error(y_test, y_pred_plr)
    rmse_plr = np.sqrt(mse_plr)
    r2_plr = r2_score(y_test, y_pred_plr)
    
    # Residual analysis for best model (MLR)
    residuals_mlr = (y_test - y_pred_mlr).tolist()
    
    # Correlation matrix of regression features
    corr_matrix = df[feature_cols + ['accident_count']].corr().round(3).to_dict()
    
    # Prepare comparison results
    results = {
        "dataset_summary": {
            "total_months": len(df),
            "features_used": feature_cols,
            "target": "accident_count"
        },
        "correlation_matrix": corr_matrix,
        "models": {
            "Simple Linear Regression": {
                "equation": f"Accident Count = {slr.intercept_:.2f} + ({slr.coef_[0]:.4f} * total_vehicles)",
                "mae": round(float(mae_slr), 2),
                "mse": round(float(mse_slr), 2),
                "rmse": round(float(rmse_slr), 2),
                "r2": round(float(r2_slr), 4)
            },
            "Multiple Linear Regression": {
                "coefficients": {col: round(float(coef), 4) for col, coef in zip(feature_cols, mlr.coef_)},
                "intercept": round(float(mlr.intercept_), 2),
                "mae": round(float(mae_mlr), 2),
                "mse": round(float(mse_mlr), 2),
                "rmse": round(float(rmse_mlr), 2),
                "r2": round(float(r2_mlr), 4)
            },
            "Polynomial Regression (Degree 2)": {
                "poly_degree": 2,
                "mae": round(float(mae_plr), 2),
                "mse": round(float(mse_plr), 2),
                "rmse": round(float(rmse_plr), 2),
                "r2": round(float(r2_plr), 4)
            }
        },
        "actual_vs_predicted": {
            "actual": [int(val) for val in y_test],
            "pred_slr": [round(float(val), 1) for val in y_pred_slr],
            "pred_mlr": [round(float(val), 1) for val in y_pred_mlr],
            "pred_plr": [round(float(val), 1) for val in y_pred_plr],
            "residuals_mlr": [round(float(val), 1) for val in residuals_mlr]
        },
        "monthly_series": {
            "labels": [f"{row['collision_year']}-{int(row['month']):02d}" for _, row in df.iterrows()],
            "counts": df['accident_count'].tolist()
        }
    }
    
    # Save models
    joblib.dump(slr, os.path.join(MODEL_DIR, "regression_slr.joblib"))
    joblib.dump(mlr, os.path.join(MODEL_DIR, "regression_mlr.joblib"))
    joblib.dump(plr, os.path.join(MODEL_DIR, "regression_plr.joblib"))
    joblib.dump(poly, os.path.join(MODEL_DIR, "poly_transformer.joblib"))
    
    # Save results json
    report_path = os.path.join(REPORT_DIR, "regression_results.json")
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Regression experiments completed successfully. Results saved to: {report_path}")
    print(f"  SLR R2: {r2_slr:.4f} | RMSE: {rmse_slr:.2f}")
    print(f"  MLR R2: {r2_mlr:.4f} | RMSE: {rmse_mlr:.2f}")
    print(f"  PLR R2: {r2_plr:.4f} | RMSE: {rmse_plr:.2f}")
    return results

if __name__ == "__main__":
    run_regression_analysis()
