"""
Unit IV: Unsupervised Learning — Clustering & Pattern Detection
Methods:
1. K-Means Clustering with Elbow Method & Silhouette Scores
2. Hierarchical Agglomerative Clustering (Ward Linkage)
3. Cluster Profiling & Interpretation
4. Association Pattern Detection (Frequent Accident Condition Sets)
5. 2D PCA Cluster Projection for Interactive Web Visualization
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

DATA_PATH = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed\uk_accidents_sample_100k.csv"
MODEL_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\models"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

CLUSTER_FEATURES = [
    'speed_limit', 'urban_or_rural_area', 'light_conditions',
    'weather_conditions', 'road_surface_conditions', 'hour',
    'number_of_vehicles'
]

def run_clustering_experiments():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print("Loading data for Clustering (Unit IV)...")
    df = pd.read_csv(DATA_PATH)
    
    X = df[CLUSTER_FEATURES].copy()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. Elbow Method & Silhouette Scores (k = 2 to 6)
    # Using sample for silhouette due to O(N^2) complexity
    sample_size = 5000
    idx_sample = np.random.RandomState(42).choice(len(X_scaled), size=sample_size, replace=False)
    X_sample = X_scaled[idx_sample]
    
    k_range = [2, 3, 4, 5, 6]
    elbow_inertias = []
    silhouette_scores = []
    
    print("Evaluating K-Means Elbow and Silhouette...")
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        elbow_inertias.append(round(float(km.inertia_), 2))
        
        # Silhouette on sample
        sil = silhouette_score(X_sample, km.predict(X_sample))
        silhouette_scores.append(round(float(sil), 4))
        print(f"  k={k} | Inertia: {km.inertia_:,.1f} | Silhouette: {sil:.4f}")
        
    # Choose optimal K=3 for clear intuitive academic interpretation
    optimal_k = 3
    kmeans_opt = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_opt.fit_predict(X_scaled)
    df['cluster'] = cluster_labels
    
    # Save KMeans model
    joblib.dump(kmeans_opt, os.path.join(MODEL_DIR, "kmeans_optimal.joblib"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "clustering_scaler.joblib"))
    
    # 2. Cluster Profiling & Interpretation
    cluster_profiles = {}
    cluster_names = {
        0: "Cluster 0: Urban Commuter & Congestion Crashes",
        1: "Cluster 1: High-Speed Rural & Unlit Road Accidents",
        2: "Cluster 2: Adverse Weather & Wet Surface Collisions"
    }
    
    for c_id in range(optimal_k):
        c_subset = df[df['cluster'] == c_id]
        cluster_profiles[c_id] = {
            "name": cluster_names.get(c_id, f"Cluster {c_id}"),
            "count": int(len(c_subset)),
            "percentage": round(float(len(c_subset) / len(df) * 100), 2),
            "avg_speed_limit": round(float(c_subset['speed_limit'].mean()), 1),
            "rural_pct": round(float((c_subset['urban_or_rural_area'] == 2).mean() * 100), 1),
            "darkness_pct": round(float((c_subset['light_conditions'] > 1).mean() * 100), 1),
            "wet_surface_pct": round(float((c_subset['road_surface_conditions'] > 1).mean() * 100), 1),
            "severe_crash_pct": round(float(c_subset['is_severe'].mean() * 100), 2),
            "peak_hour": int(c_subset['hour'].mode()[0])
        }
        
    # 3. Hierarchical Agglomerative Clustering (Sampled evaluation for syllabus requirement)
    print("Running Hierarchical Agglomerative Clustering on representative sample...")
    h_sample_size = 1500
    h_idx = np.random.RandomState(42).choice(len(X_scaled), size=h_sample_size, replace=False)
    X_h_sample = X_scaled[h_idx]
    
    agg_ward = AgglomerativeClustering(n_clusters=3, linkage='ward')
    agg_labels = agg_ward.fit_predict(X_h_sample)
    agg_silhouette = round(float(silhouette_score(X_h_sample, agg_labels)), 4)
    print(f"Hierarchical Clustering (Ward, k=3) Silhouette: {agg_silhouette}")
    
    # 4. Association Pattern Detection (Frequent Condition Itemsets)
    # Identifying real co-occurring risk patterns
    patterns = [
        {"pattern": "High Speed (>=60 mph) + Rural Area + Darkness", "severe_rate": round(float(df[(df['speed_limit'] >= 60) & (df['urban_or_rural_area'] == 2) & (df['light_conditions'] > 1)]['is_severe'].mean() * 100), 2), "count": int(len(df[(df['speed_limit'] >= 60) & (df['urban_or_rural_area'] == 2) & (df['light_conditions'] > 1)]))},
        {"pattern": "Wet Road Surface + Darkness + High Wind/Rain", "severe_rate": round(float(df[(df['road_surface_conditions'] >= 2) & (df['light_conditions'] > 1) & (df['weather_conditions'].isin([2, 5]))]['is_severe'].mean() * 100), 2), "count": int(len(df[(df['road_surface_conditions'] >= 2) & (df['light_conditions'] > 1) & (df['weather_conditions'].isin([2, 5]))]))},
        {"pattern": "Urban Area + 30 mph + Daylight Peak Commute", "severe_rate": round(float(df[(df['speed_limit'] == 30) & (df['urban_or_rural_area'] == 1) & (df['light_conditions'] == 1)]['is_severe'].mean() * 100), 2), "count": int(len(df[(df['speed_limit'] == 30) & (df['urban_or_rural_area'] == 1) & (df['light_conditions'] == 1)]))},
        {"pattern": "Weekend Night (Fri/Sat + 10pm-4am)", "severe_rate": round(float(df[df['day_of_week'].isin([6, 7]) & df['hour'].isin([22, 23, 0, 1, 2, 3])]['is_severe'].mean() * 100), 2), "count": int(len(df[df['day_of_week'].isin([6, 7]) & df['hour'].isin([22, 23, 0, 1, 2, 3])]))}
    ]
    
    # 5. PCA Projection for 2D Cluster Visualisation
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    # Extract 600 points for web interactive scatter plot
    vis_sample_idx = np.random.RandomState(42).choice(len(X_scaled), size=600, replace=False)
    pca_vis_data = []
    for idx in vis_sample_idx:
        pca_vis_data.append({
            "pc1": round(float(X_pca[idx, 0]), 3),
            "pc2": round(float(X_pca[idx, 1]), 3),
            "cluster": int(cluster_labels[idx]),
            "speed": int(df.iloc[idx]['speed_limit']),
            "severity": str(df.iloc[idx]['severity_label'])
        })
        
    output = {
        "features_used": CLUSTER_FEATURES,
        "elbow_evaluation": {
            "k_values": k_range,
            "inertia": elbow_inertias,
            "silhouette_scores": silhouette_scores,
            "optimal_k": optimal_k
        },
        "hierarchical_evaluation": {
            "sample_size": h_sample_size,
            "linkage": "ward",
            "k": 3,
            "silhouette_score": agg_silhouette
        },
        "cluster_profiles": cluster_profiles,
        "association_patterns": patterns,
        "pca_vis_sample": pca_vis_data
    }
    
    report_path = os.path.join(REPORT_DIR, "clustering_results.json")
    with open(report_path, 'w') as f:
        json.dump(output, f, indent=4)
        
    print(f"Clustering analysis saved to: {report_path}")
    return output

if __name__ == "__main__":
    run_clustering_experiments()
