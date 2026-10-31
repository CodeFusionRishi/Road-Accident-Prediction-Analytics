"""
Master ML Orchestration Script
Runs all syllabus experiments across Units II, III, IV, V, VI:
- Regression (SLR, MLR, Poly)
- Classification (LogReg, NaiveBayes, KNN, DecisionTree, SVM, RandomForest, GradientBoosting)
- Clustering (K-Means, Elbow, Silhouette, Hierarchical, Pattern Detection)
- PCA & Neural Networks (PCA explained variance, Scree, MLP)
- Ensemble Learning & Master Leaderboard (Bagging, Forest, Boosting, Bias-Variance)
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from regression import run_regression_analysis
from classification import run_classification_experiments
from clustering import run_clustering_experiments
from pca_neural_network import run_pca_and_nn_experiments
from ensemble import run_ensemble_experiments

def main():
    print("=" * 70)
    print("STARTING ACADEMIC PREDICTIVE ANALYTICS EXPERIMENTS (UNITS II - VI)")
    print("=" * 70)
    start_total = time.time()
    
    # 1. Regression
    print("\n>>> UNIT II: REGRESSION EXPERIMENTS")
    t0 = time.time()
    run_regression_analysis()
    print(f"Unit II finished in {time.time() - t0:.2f}s")
    
    # 2. Classification
    print("\n>>> UNIT III: CLASSIFICATION EXPERIMENTS")
    t0 = time.time()
    run_classification_experiments()
    print(f"Unit III finished in {time.time() - t0:.2f}s")
    
    # 3. Clustering
    print("\n>>> UNIT IV: CLUSTERING & PATTERN DETECTION")
    t0 = time.time()
    run_clustering_experiments()
    print(f"Unit IV finished in {time.time() - t0:.2f}s")
    
    # 4. PCA & Neural Networks
    print("\n>>> UNIT V: PCA & MULTI-LAYER PERCEPTRON (NEURAL NETWORK)")
    t0 = time.time()
    run_pca_and_nn_experiments()
    print(f"Unit V finished in {time.time() - t0:.2f}s")
    
    # 5. Ensemble & Comparison
    print("\n>>> UNIT VI: ENSEMBLE LEARNING & MASTER EVALUATION")
    t0 = time.time()
    run_ensemble_experiments()
    print(f"Unit VI finished in {time.time() - t0:.2f}s")
    
    print("\n" + "=" * 70)
    print(f"ALL EXPERIMENTS COMPLETED SUCCESSFULLY IN {time.time() - start_total:.2f}s")
    print("=" * 70)

if __name__ == "__main__":
    main()
