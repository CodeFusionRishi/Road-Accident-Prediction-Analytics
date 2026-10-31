"""
Unit V: Dimensionality Reduction and Neural Networks
1. Principal Component Analysis (PCA):
   - Scree plot & Explained Variance Ratio
   - Principal Component Loadings
   - Model Performance Before vs After PCA
2. Multi-Layer Perceptron (MLP) Neural Network:
   - Feedforward architecture (Input -> Hidden1(64) -> Hidden2(32) -> Output)
   - ReLU activation, Adam optimizer, early stopping
   - Comparison with traditional ML models
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

DATA_PATH = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed\uk_accidents_sample_100k.csv"
MODEL_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\models"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

FEATURE_COLS = [
    'speed_limit', 'road_type', 'light_conditions', 'weather_conditions',
    'road_surface_conditions', 'urban_or_rural_area', 'number_of_vehicles',
    'day_of_week', 'hour', 'first_road_class'
]

def run_pca_and_nn_experiments():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print("Loading data for PCA and Neural Networks (Unit V)...")
    df = pd.read_csv(DATA_PATH)
    
    X = df[FEATURE_COLS].copy()
    y = df['is_severe'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # -------------------------------------------------------------
    # PART 1: Principal Component Analysis (PCA)
    # -------------------------------------------------------------
    print("Running Full PCA...")
    pca_full = PCA(random_state=42)
    pca_full.fit(X_train_scaled)
    
    explained_var = [round(float(v), 4) for v in pca_full.explained_variance_ratio_]
    cum_explained_var = [round(float(v), 4) for v in np.cumsum(pca_full.explained_variance_ratio_)]
    
    # PCA Loadings for top 3 components
    loadings = pd.DataFrame(
        pca_full.components_[:3].T,
        columns=['PC1', 'PC2', 'PC3'],
        index=FEATURE_COLS
    ).round(4).to_dict()
    
    # Evaluate Baseline Model (Logistic Regression) with All 10 Features
    lr_full = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    lr_full.fit(X_train_scaled, y_train)
    y_pred_full = lr_full.predict(X_test_scaled)
    acc_full = accuracy_score(y_test, y_pred_full)
    f1_full = f1_score(y_test, y_pred_full, average='weighted')
    
    # Evaluate Model with Top 3 Principal Components (Dimensionality Reduction: 10 -> 3)
    pca_3 = PCA(n_components=3, random_state=42)
    X_train_pca3 = pca_3.fit_transform(X_train_scaled)
    X_test_pca3 = pca_3.transform(X_test_scaled)
    
    lr_pca = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    lr_pca.fit(X_train_pca3, y_train)
    y_pred_pca = lr_pca.predict(X_test_pca3)
    acc_pca = accuracy_score(y_test, y_pred_pca)
    f1_pca = f1_score(y_test, y_pred_pca, average='weighted')
    
    # Save PCA model
    joblib.dump(pca_3, os.path.join(MODEL_DIR, "pca_3comp.joblib"))
    
    # -------------------------------------------------------------
    # PART 2: Multi-Layer Perceptron (MLP) Neural Network
    # -------------------------------------------------------------
    print("Training Multi-Layer Perceptron (MLP) Neural Network...")
    mlp = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        solver='adam',
        max_iter=150,
        early_stopping=True,
        validation_fraction=0.1,
        random_state=42
    )
    
    mlp.fit(X_train_scaled, y_train)
    y_pred_mlp = mlp.predict(X_test_scaled)
    y_prob_mlp = mlp.predict_proba(X_test_scaled)[:, 1]
    
    acc_mlp = accuracy_score(y_test, y_pred_mlp)
    prec_mlp = precision_score(y_test, y_pred_mlp, average='weighted', zero_division=0)
    rec_mlp = recall_score(y_test, y_pred_mlp, average='weighted', zero_division=0)
    f1_macro_mlp = f1_score(y_test, y_pred_mlp, average='macro', zero_division=0)
    f1_weighted_mlp = f1_score(y_test, y_pred_mlp, average='weighted', zero_division=0)
    cm_mlp = confusion_matrix(y_test, y_pred_mlp).tolist()
    auc_mlp = roc_auc_score(y_test, y_prob_mlp)
    
    # Save MLP model
    joblib.dump(mlp, os.path.join(MODEL_DIR, "clf_neural_network_mlp.joblib"))
    
    output = {
        "pca_results": {
            "n_features_original": len(FEATURE_COLS),
            "n_components_reduced": 3,
            "explained_variance_ratio": explained_var,
            "cumulative_explained_variance": cum_explained_var,
            "scree_labels": [f"PC{i+1}" for i in range(len(FEATURE_COLS))],
            "loadings": loadings,
            "comparison_before_after": {
                "before_pca_all_features": {
                    "accuracy": round(float(acc_full), 4),
                    "weighted_f1": round(float(f1_full), 4),
                    "features_count": len(FEATURE_COLS)
                },
                "after_pca_3_components": {
                    "accuracy": round(float(acc_pca), 4),
                    "weighted_f1": round(float(f1_pca), 4),
                    "features_count": 3,
                    "retained_variance_pct": round(float(cum_explained_var[2] * 100), 2)
                }
            }
        },
        "neural_network_mlp": {
            "architecture": {
                "input_layer": len(FEATURE_COLS),
                "hidden_layers": [64, 32],
                "activation": "ReLU",
                "output_layer": 2,
                "optimizer": "Adam",
                "iterations_completed": int(mlp.n_iter_),
                "loss_curve": [round(float(v), 4) for v in mlp.loss_curve_]
            },
            "metrics": {
                "accuracy": round(float(acc_mlp), 4),
                "precision": round(float(prec_mlp), 4),
                "recall": round(float(rec_mlp), 4),
                "macro_f1": round(float(f1_macro_mlp), 4),
                "weighted_f1": round(float(f1_weighted_mlp), 4),
                "roc_auc": round(float(auc_mlp), 4),
                "confusion_matrix": cm_mlp
            }
        }
    }
    
    report_path = os.path.join(REPORT_DIR, "pca_nn_results.json")
    with open(report_path, 'w') as f:
        json.dump(output, f, indent=4)
        
    print(f"PCA and Neural Network results saved to: {report_path}")
    print(f"  MLP Accuracy: {acc_mlp:.4f} | Weighted F1: {f1_weighted_mlp:.4f} | ROC-AUC: {auc_mlp:.4f}")
    return output

if __name__ == "__main__":
    run_pca_and_nn_experiments()
