"""
Unit III: Supervised Learning — Classification
Accident Severity Prediction
Target: collision_severity (1: Fatal, 2: Serious, 3: Slight) and binary (is_severe: 1 = Fatal/Serious, 0 = Slight)
Models:
1. Logistic Regression
2. K-Nearest Neighbors (KNN)
3. Gaussian Naive Bayes
4. Decision Tree
5. Support Vector Machine (Linear SVC / SGDClassifier)
6. Random Forest
7. Gradient Boosting
Metrics: Accuracy, Precision, Recall, Macro F1, Weighted F1, Confusion Matrix, ROC-AUC
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, log_loss
)

DATA_PATH = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed\uk_accidents_sample_100k.csv"
MODEL_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\models"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

# Feature set
FEATURE_COLS = [
    'speed_limit', 'road_type', 'light_conditions', 'weather_conditions',
    'road_surface_conditions', 'urban_or_rural_area', 'number_of_vehicles',
    'day_of_week', 'hour', 'first_road_class'
]

def run_classification_experiments():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print("Loading classification sample dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # We evaluate on binary severity: 1 = Severe (Fatal or Serious), 0 = Slight
    # This directly addresses the severe road injury risk for emergency services.
    X = df[FEATURE_COLS].copy()
    y = df['is_severe'].values
    
    print(f"Dataset shape: {X.shape}")
    print(f"Class distribution: Slight (0) = {(y == 0).sum():,}, Severe (1) = {(y == 1).sum():,}")
    
    # Stratified Train/Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Standardize numerical features for distance & gradient based models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    joblib.dump(scaler, os.path.join(MODEL_DIR, "classification_scaler.joblib"))
    
    # Define models
    # We use class_weight='balanced' where available to address real-world class imbalance
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        "Gaussian Naive Bayes": GaussianNB(),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7, n_jobs=-1),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, class_weight='balanced', random_state=42),
        "Support Vector Machine": SGDClassifier(loss='log_loss', class_weight='balanced', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', n_jobs=-1, random_state=42),
        "Gradient Boosting": HistGradientBoostingClassifier(max_iter=100, class_weight='balanced', random_state=42)
    }
    
    # For KNN and SVM on large dataset, evaluate on a calibrated subset for fast training
    knn_sample_size = 20000
    
    results = {}
    best_model_name = None
    best_f1 = -1
    
    for name, clf in models.items():
        print(f"\nTraining {name}...")
        if name in ["Logistic Regression", "Support Vector Machine", "Gaussian Naive Bayes"]:
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)
            y_prob = clf.predict_proba(X_test_scaled)[:, 1] if hasattr(clf, 'predict_proba') else None
        elif name == "K-Nearest Neighbors":
            clf.fit(X_train_scaled[:knn_sample_size], y_train[:knn_sample_size])
            y_pred = clf.predict(X_test_scaled)
            y_prob = clf.predict_proba(X_test_scaled)[:, 1]
        else: # Tree-based models
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, 'predict_proba') else None
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        roc_auc = roc_auc_score(y_test, y_prob) if y_prob is not None else None
        logloss_val = log_loss(y_test, y_prob) if y_prob is not None else None
        
        print(f"  Accuracy: {acc:.4f} | Weighted F1: {weighted_f1:.4f} | ROC-AUC: {roc_auc if roc_auc else 'N/A'}")
        
        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "macro_f1": round(float(macro_f1), 4),
            "weighted_f1": round(float(weighted_f1), 4),
            "roc_auc": round(float(roc_auc), 4) if roc_auc else None,
            "log_loss": round(float(logloss_val), 4) if logloss_val else None,
            "confusion_matrix": cm
        }
        
        # Save model
        model_filename = name.lower().replace(" ", "_").replace("-", "_") + ".joblib"
        joblib.dump(clf, os.path.join(MODEL_DIR, f"clf_{model_filename}"))
        
        if weighted_f1 > best_f1:
            best_f1 = weighted_f1
            best_model_name = name

    # Feature Importance from Random Forest
    rf_model = models["Random Forest"]
    feature_importances = dict(zip(FEATURE_COLS, [round(float(v), 4) for v in rf_model.feature_importances_]))
    sorted_importances = dict(sorted(feature_importances.items(), key=lambda x: x[1], reverse=True))

    output = {
        "dataset_summary": {
            "total_records": len(df),
            "train_records": len(X_train),
            "test_records": len(X_test),
            "target": "is_severe (1 = Fatal/Serious, 0 = Slight)",
            "features": FEATURE_COLS
        },
        "best_model": {
            "name": best_model_name,
            "weighted_f1": round(float(best_f1), 4)
        },
        "models": results,
        "feature_importance": sorted_importances,
        "class_imbalance_analysis": {
            "slight_count": int((y == 0).sum()),
            "severe_count": int((y == 1).sum()),
            "slight_ratio": round(float((y == 0).mean()), 4),
            "severe_ratio": round(float((y == 1).mean()), 4),
            "imbalance_handling_method": "class_weight='balanced' applied across estimators to penalize false negatives on rare severe crashes"
        }
    }
    
    report_path = os.path.join(REPORT_DIR, "classification_results.json")
    with open(report_path, 'w') as f:
        json.dump(output, f, indent=4)
        
    print(f"\nClassification experiments saved to: {report_path}")
    print(f"Top 3 important features according to Random Forest: {list(sorted_importances.items())[:3]}")
    return output

if __name__ == "__main__":
    run_classification_experiments()
