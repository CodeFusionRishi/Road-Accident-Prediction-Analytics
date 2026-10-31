"""
Unit VI: Model Performance & Ensemble Learning
1. Ensemble Models:
   - Bagging (Bootstrap Aggregation)
   - Random Forest (Bagging + Random Subspace)
   - Gradient Boosting (Sequential error reduction)
2. Bias-Variance Tradeoff Analysis
3. Comprehensive Master Leaderboard (All 9 Models from Units III, V, VI)
4. Academic Viva Discussion on Ensembles vs Traditional Models
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

DATA_PATH = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed\uk_accidents_sample_100k.csv"
MODEL_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\models"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

FEATURE_COLS = [
    'speed_limit', 'road_type', 'light_conditions', 'weather_conditions',
    'road_surface_conditions', 'urban_or_rural_area', 'number_of_vehicles',
    'day_of_week', 'hour', 'first_road_class'
]

def run_ensemble_experiments():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print("Loading data for Ensemble Learning (Unit VI)...")
    df = pd.read_csv(DATA_PATH)
    
    X = df[FEATURE_COLS].copy()
    y = df['is_severe'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # 1. Bagging Classifier
    print("Training Bagging Classifier...")
    bagging = BaggingClassifier(
        estimator=DecisionTreeClassifier(max_depth=10, class_weight='balanced'),
        n_estimators=30,
        random_state=42,
        n_jobs=-1
    )
    bagging.fit(X_train, y_train)
    y_pred_bag = bagging.predict(X_test)
    y_prob_bag = bagging.predict_proba(X_test)[:, 1]
    
    acc_bag = accuracy_score(y_test, y_pred_bag)
    prec_bag = precision_score(y_test, y_pred_bag, average='weighted', zero_division=0)
    rec_bag = recall_score(y_test, y_pred_bag, average='weighted', zero_division=0)
    f1_bag = f1_score(y_test, y_pred_bag, average='weighted', zero_division=0)
    auc_bag = roc_auc_score(y_test, y_prob_bag)
    
    # Save bagging model
    joblib.dump(bagging, os.path.join(MODEL_DIR, "clf_bagging.joblib"))
    
    # Load previously trained classification & NN metrics to compile Master Leaderboard
    clf_report_path = os.path.join(REPORT_DIR, "classification_results.json")
    pca_nn_report_path = os.path.join(REPORT_DIR, "pca_nn_results.json")
    
    clf_models = {}
    if os.path.exists(clf_report_path):
        with open(clf_report_path, 'r') as f:
            clf_models = json.load(f).get("models", {})
            
    nn_metrics = {}
    if os.path.exists(pca_nn_report_path):
        with open(pca_nn_report_path, 'r') as f:
            nn_metrics = json.load(f).get("neural_network_mlp", {}).get("metrics", {})
            
    # Add Bagging to results
    clf_models["Bagging (Decision Trees)"] = {
        "accuracy": round(float(acc_bag), 4),
        "precision": round(float(prec_bag), 4),
        "recall": round(float(rec_bag), 4),
        "macro_f1": round(float(f1_score(y_test, y_pred_bag, average='macro', zero_division=0)), 4),
        "weighted_f1": round(float(f1_bag), 4),
        "roc_auc": round(float(auc_bag), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred_bag).tolist()
    }
    
    if nn_metrics:
        clf_models["Multi-Layer Perceptron (MLP)"] = nn_metrics

    # Create Master Leaderboard comparing all models
    leaderboard = []
    for model_name, metrics in clf_models.items():
        leaderboard.append({
            "model_name": model_name,
            "accuracy": metrics.get("accuracy", 0),
            "precision": metrics.get("precision", 0),
            "recall": metrics.get("recall", 0),
            "weighted_f1": metrics.get("weighted_f1", 0),
            "roc_auc": metrics.get("roc_auc", 0),
            "category": "Ensemble" if any(x in model_name for x in ["Forest", "Boosting", "Bagging"]) else ("Neural Network" if "Perceptron" in model_name else "Traditional")
        })
        
    leaderboard = sorted(leaderboard, key=lambda x: x["weighted_f1"], reverse=True)
    best_overall = leaderboard[0]
    
    # Bias-Variance Analysis Discussion
    bias_variance_table = [
        {"model": "Logistic Regression", "bias": "High", "variance": "Low", "risk": "Underfitting nonlinear road interactions", "viva_note": "Linear decision boundary cannot capture speed x darkness interaction."},
        {"model": "Decision Tree (Unpruned)", "bias": "Low", "variance": "High", "risk": "Overfitting noise and single accidents", "viva_note": "High variance mitigated by ensemble bagging."},
        {"model": "Random Forest", "bias": "Low", "variance": "Medium-Low", "risk": "Balanced", "viva_note": "Averages many decorrelated trees; reduces variance substantially."},
        {"model": "Gradient Boosting", "bias": "Low", "variance": "Low-Medium", "risk": "Balanced / Overfitting if too many iterations", "viva_note": "Sequential boosting reduces bias by focusing on hard-to-classify crashes."},
        {"model": "Multi-Layer Perceptron (NN)", "bias": "Low", "variance": "Medium", "risk": "Requires extensive parameter tuning", "viva_note": "Approximates complex nonlinear surfaces through ReLU hidden layers."}
    ]
    
    output = {
        "master_leaderboard": leaderboard,
        "best_model": best_overall,
        "bias_variance_analysis": bias_variance_table,
        "ensemble_comparison": {
            "bagging_vs_random_forest": "Random Forest improves on standard Bagging by introducing feature bagging (random subspace), which decorrelates individual decision trees and achieves higher generalization.",
            "boosting_vs_bagging": "Bagging builds independent models in parallel to cut variance, while Boosting builds models sequentially to minimize residual bias."
        }
    }
    
    report_path = os.path.join(REPORT_DIR, "ensemble_comparison_results.json")
    with open(report_path, 'w') as f:
        json.dump(output, f, indent=4)
        
    print(f"Ensemble and master evaluation saved to: {report_path}")
    print(f"Top performing model overall: {best_overall['model_name']} with Weighted F1: {best_overall['weighted_f1']}")
    return output

if __name__ == "__main__":
    run_ensemble_experiments()
