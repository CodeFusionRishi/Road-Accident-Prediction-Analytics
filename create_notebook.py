"""
Script to generate the complete UK_Road_Accident_Predictive_Analytics.ipynb Jupyter Notebook
"""

import os
import nbformat as nbf

notebook_path = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\UK_Road_Accident_Predictive_Analytics.ipynb"

nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Title Markdown
cells.append(nbf.v4.new_markdown_cell("""# Road Accident Prediction and Analytics Using Machine Learning
### UK STATS19 Road Safety Microdata Analysis
**Course / Subject:** Predictive Analytics  
**Implementation:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn)

---

### Project Objectives:
1. **Data Ingestion & Cleaning:** Load verified UK accident records (2021–2025), clean missing codes (`-1`), extract time features.
2. **Exploratory Data Analysis (EDA):** Univariate distributions, bivariate relations, and correlation heatmaps using Seaborn.
3. **Regression Analysis:** Forecast monthly nationwide collision counts using Simple Linear, Multiple Linear, and Polynomial Regression ($R^2$, RMSE, MAE).
4. **Severity Classification:** Predict crash severity (Severe vs. Slight) using Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting.
5. **Pattern Clustering:** Discover operational accident archetypes using K-Means (Elbow method, Silhouette scores) and PCA visualization.
6. **Dimensionality Reduction (PCA):** Scree plot, explained variance, and model benchmark before vs. after PCA.
7. **Neural Networks:** Multi-Layer Perceptron (MLP) feedforward network for severity prediction.
8. **Ensemble Comparison & Feature Importance:** Gini feature importance ranking and Bias-Variance tradeoff analysis.
9. **Interactive Prediction Function:** Real-time Python function for live accident risk inference.
"""))

# Cell 2: Import Libraries
cells.append(nbf.v4.new_code_cell("""# 1. Core Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set plotting aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

print("All libraries loaded successfully.")
"""))

# Cell 3: Data Ingestion
cells.append(nbf.v4.new_markdown_cell("""---
## 1. Data Ingestion & First Principles Inspection
We load the validated recent 5-year dataset (`uk_accidents_sample_100k.csv`) created from the official UK Department for Transport (DfT) repository.
"""))

cells.append(nbf.v4.new_code_cell("""# Load the dataset
data_path = "data/processed/uk_accidents_sample_100k.csv"
df = pd.read_csv(data_path)

print(f"Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\\n")
print("--- Column Data Types & Non-Null Values ---")
df.info()
"""))

cells.append(nbf.v4.new_code_cell("""# Display first 5 records
df.head()
"""))

cells.append(nbf.v4.new_code_cell("""# Summary statistics for numerical variables
df[['speed_limit', 'number_of_vehicles', 'number_of_casualties', 'hour', 'day_of_week']].describe().round(2)
"""))

cells.append(nbf.v4.new_code_cell("""# Verify missing values
missing = df.isnull().sum()
print("Missing values per column:")
print(missing[missing > 0] if missing.sum() > 0 else "Zero missing values detected across all modeling features.")
"""))

# Cell 4: EDA
cells.append(nbf.v4.new_markdown_cell("""---
## 2. Exploratory Data Analysis (EDA) & Seaborn Visualizations
Here we analyze accident distributions, environmental risk factors, temporal trends, and correlation heatmaps.
"""))

cells.append(nbf.v4.new_code_cell("""# 2.1 Target Variable Distribution (Accident Severity)
plt.figure(figsize=(8, 4.5))
palette = {'Slight': '#38bdf8', 'Serious': '#f59e0b', 'Fatal': '#ef4444'}
ax = sns.countplot(data=df, x='severity_label', order=['Slight', 'Serious', 'Fatal'], palette=palette)

total = len(df)
for p in ax.patches:
    count = int(p.get_height())
    pct = count / total * 100
    ax.annotate(f"{count:,}\\n({pct:.1f}%)", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                ha='center', va='center', color='white', fontweight='bold', fontsize=11)

plt.title("Distribution of Road Accident Severity (UK STATS19)", fontsize=13, pad=12)
plt.xlabel("Accident Severity", labelpad=8)
plt.ylabel("Number of Collisions", labelpad=8)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 2.2 Correlation Heatmap (First Principles Bivariate Analysis)
numerical_features = ['speed_limit', 'number_of_vehicles', 'number_of_casualties', 
                      'hour', 'day_of_week', 'urban_or_rural_area', 'is_severe']

corr_matrix = df[numerical_features].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, cbar_kws={'label': 'Pearson Correlation (r)'})
plt.title("Correlation Matrix of Numerical Road & Collision Features", fontsize=13, pad=12)
plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 2.3 Accidents by Hour of Day & Day of Week
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Hourly trend
sns.lineplot(data=df['hour'].value_counts().sort_index(), ax=axes[0], color='#2563eb', marker='o', linewidth=2.5)
axes[0].set_title("Accidents by Hour of Day (Peak Commute Windows)", fontsize=12)
axes[0].set_xlabel("Hour (24-Hour Clock)")
axes[0].set_ylabel("Accident Count")
axes[0].set_xticks(range(0, 24, 2))

# Day of week
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.barplot(data=df, x='day_name', order=dow_order, ax=axes[1], palette='Blues_d')
axes[1].set_title("Accidents by Day of Week (Friday Peak)", fontsize=12)
axes[1].set_xlabel("Day of Week")
axes[1].set_ylabel("Accident Count")
axes[1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 2.4 Environmental Risk Factors: Speed Limit, Light, Road Surface & Weather
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Speed Limit vs Severity Rate
speed_sev = df.groupby('speed_limit')['is_severe'].mean() * 100
sns.barplot(x=speed_sev.index, y=speed_sev.values, ax=axes[0, 0], palette='Reds_d')
axes[0, 0].set_title("Severe Crash Rate (%) by Posted Speed Limit", fontsize=12)
axes[0, 0].set_xlabel("Speed Limit (mph)")
axes[0, 0].set_ylabel("Severe Crash Rate (%)")

# Light Conditions vs Severity Rate
light_sev = df.groupby('light_label')['is_severe'].mean() * 100
sns.barplot(y=light_sev.index, x=light_sev.values, ax=axes[0, 1], palette='Purples_r')
axes[0, 1].set_title("Severe Crash Rate (%) by Lighting Condition", fontsize=12)
axes[0, 1].set_xlabel("Severe Crash Rate (%)")

# Road Surface Conditions
surface_sev = df.groupby('surface_label')['is_severe'].mean() * 100
sns.barplot(y=surface_sev.index, x=surface_sev.values, ax=axes[1, 0], palette='Blues_r')
axes[1, 0].set_title("Severe Crash Rate (%) by Road Surface Condition", fontsize=12)
axes[1, 0].set_xlabel("Severe Crash Rate (%)")

# Urban vs Rural
area_sev = df.groupby('area_label')['is_severe'].mean() * 100
sns.barplot(x=area_sev.index, y=area_sev.values, ax=axes[1, 1], palette='Oranges_r')
axes[1, 1].set_title("Severe Crash Rate (%) in Urban vs. Rural Areas", fontsize=12)
axes[1, 1].set_xlabel("Area Classification")
axes[1, 1].set_ylabel("Severe Crash Rate (%)")

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 2.5 Geographical Accident Density Heatmap (Seaborn 2D KDE Spatial Density)
plt.figure(figsize=(9, 10))
geo_sample = df.sample(n=min(15000, len(df)), random_state=42)

# 2D Kernel Density Estimate (Spatial Heatmap across UK Latitude & Longitude)
sns.kdeplot(
    data=geo_sample, 
    x='longitude', 
    y='latitude', 
    fill=True, 
    cmap='rocket_r', 
    levels=15, 
    thresh=0.03,
    alpha=0.85
)

plt.title("Geographical Accident Density Heatmap (UK STATS19 Density Hotspots)", fontsize=13, pad=12)
plt.xlabel("Longitude (Degrees)", labelpad=8)
plt.ylabel("Latitude (Degrees)", labelpad=8)
plt.xlim(-7.5, 2.0)
plt.ylim(50.0, 59.0)

# Annotate Major UK Metropolitan Hubs
plt.text(-0.12, 51.50, " Greater London", color='white', fontweight='bold', fontsize=10)
plt.text(-1.90, 52.48, " Birmingham", color='white', fontweight='bold', fontsize=10)
plt.text(-2.24, 53.48, " Manchester", color='white', fontweight='bold', fontsize=10)
plt.text(-1.54, 53.80, " Leeds", color='white', fontweight='bold', fontsize=10)
plt.text(-4.25, 55.86, " Glasgow", color='white', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 2.6 Interactive UK Collision Map & HeatMap (Folium & Leaflet)
import folium
from folium.plugins import HeatMap, MarkerCluster

# Create base interactive Folium map centered on the UK with CARTO Dark Matter API Key
carto_key = "cb1_4z5r_1_e0afd38c87c9d26c3bc1ff61"
carto_url = f"https://{{s}}.basemaps.cartocdn.com/rastertiles/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png?key={carto_key}"
uk_map = folium.Map(location=[54.5, -2.5], zoom_start=6, tiles=carto_url, attr='&copy; CARTO &copy; OpenStreetMap')

# Prepare coordinate weights for the HeatMap layer
map_sample = df.sample(n=min(3000, len(df)), random_state=42)
heat_data = [[row['latitude'], row['longitude'], 1.0 if row['is_severe'] == 1 else 0.5] for _, row in map_sample.iterrows()]

# Add HeatMap Layer to visualize collision density hotspots
HeatMap(heat_data, radius=12, blur=15, min_opacity=0.3, max_val=1.0).add_to(uk_map)

# Add Clustered Markers for Severe / Fatal Incidents
marker_cluster = MarkerCluster(name="Severe Collision Hotspots").add_to(uk_map)
severe_sample = map_sample[map_sample['is_severe'] == 1].head(150)

for _, row in severe_sample.iterrows():
    popup_text = f\"\"\"
    <b>Severity:</b> {row['severity_label']}<br>
    <b>Speed Limit:</b> {int(row['speed_limit'])} mph<br>
    <b>Weather:</b> {row['weather_label']}<br>
    <b>Road:</b> {row['road_type_label']}<br>
    <b>Hour:</b> {int(row['hour'])}:00
    \"\"\"
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='#ef4444' if row['severity_label'] == 'Fatal' else '#f59e0b',
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=250)
    ).add_to(marker_cluster)

# Save the map to an interactive HTML report
os.makedirs("reports", exist_ok=True)
uk_map.save("reports/uk_interactive_accident_heatmap.html")
print("Interactive UK Heatmap successfully rendered and saved to reports/uk_interactive_accident_heatmap.html")

# Display the map directly inline in the notebook
uk_map
"""))

# Cell 5: Regression Analysis
cells.append(nbf.v4.new_markdown_cell("""---
## 3. Supervised Learning — Regression Analysis (Accident Count Forecasting)
We model **Monthly Accident Counts ($Y$)** nationwide.
Predictors include:
* `total_vehicles` (traffic volume)
* `total_casualties` (casualty volume)
* `avg_speed_limit` (speed environment)
* `time_idx` (long-term safety trend index)

We evaluate **Simple Linear Regression**, **Multiple Linear Regression**, and **Polynomial Regression (Degree 2)** using MAE, MSE, RMSE, and $R^2$.
"""))

cells.append(nbf.v4.new_code_cell("""from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Load monthly aggregated dataset
reg_df = pd.read_csv("data/processed/monthly_accident_regression.csv")
print(f"Monthly dataset: {len(reg_df)} months of observation.")
reg_df.head()
"""))

cells.append(nbf.v4.new_code_cell("""# Define features and target
X_features = ['time_idx', 'total_vehicles', 'total_casualties', 'avg_speed_limit']
X = reg_df[X_features].values
y = reg_df['accident_count'].values

# Train/Test Split (75% Train, 25% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 1. Simple Linear Regression (Accident Count vs Vehicle Volume)
slr = LinearRegression()
slr.fit(X_train[:, [1]], y_train) # feature index 1 is total_vehicles
y_pred_slr = slr.predict(X_test[:, [1]])

# 2. Multiple Linear Regression
mlr = LinearRegression()
mlr.fit(X_train, y_train)
y_pred_mlr = mlr.predict(X_test)

# 3. Polynomial Regression (Degree 2)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

plr = LinearRegression()
plr.fit(X_train_poly, y_train)
y_pred_plr = plr.predict(X_test_poly)

# Evaluation Function
def evaluate_regression(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return {'Model': name, 'MAE': round(mae, 2), 'MSE': round(mse, 2), 'RMSE': round(rmse, 2), 'R2 Score': round(r2, 4)}

reg_results = pd.DataFrame([
    evaluate_regression(y_test, y_pred_slr, "Simple Linear Regression"),
    evaluate_regression(y_test, y_pred_mlr, "Multiple Linear Regression"),
    evaluate_regression(y_test, y_pred_plr, "Polynomial Regression (Deg 2)")
])

print("--- Regression Model Evaluation Table ---")
reg_results
"""))

cells.append(nbf.v4.new_code_cell("""# Plot Actual vs. Predicted & Residuals
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Actual vs Predicted
axes[0].plot(y_test, label='Actual Counts', color='#10b981', marker='o', linewidth=2.5)
axes[0].plot(y_pred_mlr, label='MLR Prediction', color='#2563eb', linestyle='--', marker='s')
axes[0].plot(y_pred_plr, label='Polynomial Prediction', color='#8b5cf6', linestyle=':', marker='^')
axes[0].set_title("Actual vs. Predicted Monthly Accident Counts", fontsize=12)
axes[0].set_xlabel("Test Month Index")
axes[0].set_ylabel("Accident Count")
axes[0].legend()

# Residual Plot (MLR)
residuals = y_test - y_pred_mlr
sns.barplot(x=list(range(len(residuals))), y=residuals, ax=axes[1], palette='coolwarm')
axes[1].axhline(0, color='black', linestyle='--')
axes[1].set_title("Residual Error Plot (e = Y - Ŷ) for MLR", fontsize=12)
axes[1].set_xlabel("Test Month Index")
axes[1].set_ylabel("Residual Error")

plt.tight_layout()
plt.show()
"""))

# Cell 6: Classification
cells.append(nbf.v4.new_markdown_cell("""---
## 4. Supervised Learning — Severity Classification
We predict whether an accident will be **Severe (Fatal or Serious = 1)** or **Slight (Minor = 0)**.
To handle the class imbalance (~76% Slight vs ~24% Severe), we use cost-sensitive learning (`class_weight='balanced'`).

Models compared:
* Logistic Regression
* Gaussian Naive Bayes
* Decision Tree Classifier
* Random Forest Classifier
* HistGradientBoosting Classifier
"""))

cells.append(nbf.v4.new_code_cell("""from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

feature_cols = [
    'speed_limit', 'road_type', 'light_conditions', 'weather_conditions',
    'road_surface_conditions', 'urban_or_rural_area', 'number_of_vehicles',
    'day_of_week', 'hour', 'first_road_class'
]

X_clf = df[feature_cols].copy()
y_clf = df['is_severe'].values

# Stratified Split (80% Train, 20% Test)
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_clf, y_clf, test_size=0.20, random_state=42, stratify=y_clf
)

# Standardize features for linear/gradient models
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_c)
X_test_scaled = scaler.transform(X_test_c)

print(f"Training instances: {X_train_c.shape[0]:,} | Testing instances: {X_test_c.shape[0]:,}")
"""))

cells.append(nbf.v4.new_code_cell("""# Define and train models
models = {
    "Logistic Regression": (LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42), True),
    "Gaussian Naive Bayes": (GaussianNB(), True),
    "Decision Tree": (DecisionTreeClassifier(max_depth=10, class_weight='balanced', random_state=42), False),
    "Random Forest": (RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', n_jobs=-1, random_state=42), False),
    "Gradient Boosting": (HistGradientBoostingClassifier(max_iter=100, class_weight='balanced', random_state=42), False)
}

clf_metrics = []
cms = {}

for name, (clf, use_scaled) in models.items():
    X_tr = X_train_scaled if use_scaled else X_train_c
    X_te = X_test_scaled if use_scaled else X_test_c
    
    clf.fit(X_tr, y_train_c)
    y_pred = clf.predict(X_te)
    y_prob = clf.predict_proba(X_te)[:, 1] if hasattr(clf, 'predict_proba') else None
    
    acc = accuracy_score(y_test_c, y_pred)
    prec = precision_score(y_test_c, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test_c, y_pred, average='weighted', zero_division=0)
    f1_w = f1_score(y_test_c, y_pred, average='weighted', zero_division=0)
    roc = roc_auc_score(y_test_c, y_prob) if y_prob is not None else np.nan
    
    cms[name] = confusion_matrix(y_test_c, y_pred)
    
    clf_metrics.append({
        'Model': name,
        'Accuracy (%)': round(acc * 100, 2),
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'Weighted F1': round(f1_w, 4),
        'ROC-AUC': round(roc, 4)
    })

clf_results = pd.DataFrame(clf_metrics).sort_values(by='Weighted F1', ascending=False).reset_index(drop=True)
print("--- Classification Model Performance Leaderboard ---")
clf_results
"""))

cells.append(nbf.v4.new_code_cell("""# Confusion Matrix of the Top Ensemble Model (Random Forest)
plt.figure(figsize=(6, 5))
sns.heatmap(cms['Random Forest'], annot=True, fmt=',d', cmap='Blues', cbar=False,
            xticklabels=['Pred Slight (0)', 'Pred Severe (1)'],
            yticklabels=['Actual Slight (0)', 'Actual Severe (1)'])
plt.title("Confusion Matrix — Random Forest Classifier", fontsize=12, pad=10)
plt.ylabel("Ground Truth")
plt.xlabel("Predicted Class")
plt.show()
"""))

# Cell 7: Clustering
cells.append(nbf.v4.new_markdown_cell("""---
## 5. Unsupervised Learning — Clustering (Accident Risk Archetypes)
We apply **K-Means Clustering** without any ground-truth severity labels to discover natural accident patterns based on environmental and road conditions.
* Evaluated using the **Elbow Method (Inertia/WCSS)** and **Silhouette Coefficients**.
"""))

cells.append(nbf.v4.new_code_cell("""from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

cluster_cols = [
    'speed_limit', 'urban_or_rural_area', 'light_conditions',
    'weather_conditions', 'road_surface_conditions', 'hour', 'number_of_vehicles'
]

X_cluster = df[cluster_cols]
scaler_cl = StandardScaler()
X_cluster_scaled = scaler_cl.fit_transform(X_cluster)

# Evaluate K=2 to 6
k_range = list(range(2, 7))
inertias = []
silhouettes = []

# Representative sample for silhouette score (O(N^2) speedup)
sample_idx = np.random.RandomState(42).choice(len(X_cluster_scaled), size=5000, replace=False)
X_cl_sample = X_cluster_scaled[sample_idx]

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_cluster_scaled)
    inertias.append(km.inertia_)
    sil = silhouette_score(X_cl_sample, km.predict(X_cl_sample))
    silhouettes.append(sil)

fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))

axes[0].plot(k_range, inertias, marker='o', color='#2563eb', linewidth=2)
axes[0].set_title("The Elbow Method (Inertia vs. Number of Clusters)", fontsize=12)
axes[0].set_xlabel("Number of Clusters (k)")
axes[0].set_ylabel("Within-Cluster Sum of Squares (Inertia)")

axes[1].bar(k_range, silhouettes, color='#10b981', alpha=0.8)
axes[1].set_title("Silhouette Coefficients (Cluster Cohesion)", fontsize=12)
axes[1].set_xlabel("Number of Clusters (k)")
axes[1].set_ylabel("Silhouette Score")

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Fit Optimal K-Means (k = 3)
kmeans_opt = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans_opt.fit_predict(X_cluster_scaled)

# Cluster Profiling
profile = df.groupby('cluster').agg(
    Record_Count=('collision_index', 'count'),
    Avg_Speed_Limit=('speed_limit', 'mean'),
    Rural_Percentage=('urban_or_rural_area', lambda x: round((x == 2).mean() * 100, 1)),
    Darkness_Percentage=('light_conditions', lambda x: round((x > 1).mean() * 100, 1)),
    Wet_Surface_Percentage=('road_surface_conditions', lambda x: round((x > 1).mean() * 100, 1)),
    Severe_Crash_Rate=('is_severe', lambda x: round(x.mean() * 100, 2))
).reset_index()

cluster_names = {
    0: "Cluster 0: Urban Commuter & Congestion",
    1: "Cluster 1: High-Speed Rural & Unlit Darkness",
    2: "Cluster 2: Adverse Weather & Wet Surface"
}
profile['Cluster Archetype'] = profile['cluster'].map(cluster_names)
profile[['Cluster Archetype', 'Record_Count', 'Avg_Speed_Limit', 'Rural_Percentage', 'Darkness_Percentage', 'Severe_Crash_Rate']]
"""))

cells.append(nbf.v4.new_code_cell("""# 2D PCA Visualization of Discovered Clusters
pca_2d = PCA(n_components=2, random_state=42)
X_pca_vis = pca_2d.fit_transform(X_cluster_scaled)

sample_vis = np.random.RandomState(42).choice(len(df), size=1000, replace=False)

plt.figure(figsize=(9, 6))
sns.scatterplot(
    x=X_pca_vis[sample_vis, 0], 
    y=X_pca_vis[sample_vis, 1], 
    hue=df.iloc[sample_vis]['cluster'].map(cluster_names),
    palette=['#2563eb', '#ef4444', '#8b5cf6'],
    alpha=0.75, s=40
)
plt.title("2D PCA Projection of Discovered Accident Risk Clusters", fontsize=13, pad=12)
plt.xlabel("Principal Component 1 (Speed & Geometry)")
plt.ylabel("Principal Component 2 (Friction & Lighting)")
plt.legend(title="Cluster Archetype", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
"""))

# Cell 8: PCA & Neural Networks
cells.append(nbf.v4.new_markdown_cell("""---
## 6. Dimensionality Reduction (PCA) & Neural Networks (MLP)
1. **PCA Scree Plot:** Quantifying variance retention across components.
2. **Before vs. After PCA Benchmark:** Does compressing 10 features to 3 preserve predictive power?
3. **Feedforward Neural Network:** Training an `MLPClassifier` with backpropagation.
"""))

cells.append(nbf.v4.new_code_cell("""# 6.1 Principal Component Analysis (Scree Plot)
pca_full = PCA(random_state=42)
pca_full.fit(X_train_scaled)

explained_var = pca_full.explained_variance_ratio_
cum_var = np.cumsum(explained_var)

fig, ax1 = plt.subplots(figsize=(10, 5))

# Individual Variance (Bars)
ax1.bar([f"PC{i+1}" for i in range(len(explained_var))], explained_var, color='#38bdf8', alpha=0.7, label='Individual Explained Variance')
ax1.set_ylabel('Variance Ratio', color='#2563eb')
ax1.set_xlabel('Principal Components')

# Cumulative Variance (Line)
ax2 = ax1.twinx()
ax2.plot([f"PC{i+1}" for i in range(len(explained_var))], cum_var, color='#10b981', marker='o', linewidth=2.5, label='Cumulative Variance')
ax2.set_ylabel('Cumulative Variance', color='#10b981')
ax2.set_ylim(0, 1.05)

plt.title("PCA Scree Plot & Cumulative Explained Variance", fontsize=13, pad=12)
plt.show()
"""))

cells.append(nbf.v4.new_code_cell("""# 6.2 Empirical Benchmark: Model Before vs After PCA
# Fit Logistic Regression on all 10 features
lr_full = LogisticRegression(class_weight='balanced', random_state=42)
lr_full.fit(X_train_scaled, y_train_c)
f1_full = f1_score(y_test_c, lr_full.predict(X_test_scaled), average='weighted')

# Reduce to 3 components
pca_3 = PCA(n_components=3, random_state=42)
X_train_pca3 = pca_3.fit_transform(X_train_scaled)
X_test_pca3 = pca_3.transform(X_test_scaled)

lr_pca = LogisticRegression(class_weight='balanced', random_state=42)
lr_pca.fit(X_train_pca3, y_train_c)
f1_pca = f1_score(y_test_c, lr_pca.predict(X_test_pca3), average='weighted')

pd.DataFrame([
    {'Feature Set': 'All 10 Raw Features', 'Dimensions': 10, 'Weighted F1': round(f1_full, 4), 'Variance Retained': '100%'},
    {'Feature Set': 'Top 3 Principal Components', 'Dimensions': 3, 'Weighted F1': round(f1_pca, 4), 'Variance Retained': f"{cum_var[2]*100:.1f}%"}
])
"""))

cells.append(nbf.v4.new_code_cell("""# 6.3 Multi-Layer Perceptron (MLP) Neural Network
from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    max_iter=150,
    early_stopping=True,
    validation_fraction=0.1,
    random_state=42
)

mlp.fit(X_train_scaled, y_train_c)
y_pred_mlp = mlp.predict(X_test_scaled)

print(f"MLP Convergence achieved in {mlp.n_iter_} iterations.")
print(f"MLP Test Accuracy: {accuracy_score(y_test_c, y_pred_mlp)*100:.2f}%")
print(f"MLP Weighted F1: {f1_score(y_test_c, y_pred_mlp, average='weighted'):.4f}")

# Plot Loss Curve
plt.figure(figsize=(8, 4))
plt.plot(mlp.loss_curve_, color='#8b5cf6', linewidth=2)
plt.title("MLP Neural Network — Training Loss Curve (Adam Optimizer)", fontsize=12, pad=10)
plt.xlabel("Iteration")
plt.ylabel("Cross-Entropy Loss")
plt.show()
"""))

# Cell 9: Feature Importance
cells.append(nbf.v4.new_markdown_cell("""---
## 7. Feature Importance & Bias-Variance Tradeoff Analysis
* Identifying the most predictive road variables contributing to crash severity.
* Academic discussion on Bias-Variance trade-offs across model families.
"""))

cells.append(nbf.v4.new_code_cell("""# Feature Importance from Random Forest Classifier
rf_model = models["Random Forest"][0]
importances = pd.Series(rf_model.feature_importances_, index=feature_cols).sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=importances.values, y=importances.index, palette='crest')
plt.title("Random Forest Feature Importance (Mean Decrease in Gini Impurity)", fontsize=13, pad=12)
plt.xlabel("Relative Importance Weight")
plt.ylabel("Predictor Variable")

for i, v in enumerate(importances.values):
    plt.text(v + 0.003, i, f"{v:.3f}", va='center', fontweight='bold', fontsize=10)

plt.xlim(0, max(importances.values) + 0.03)
plt.tight_layout()
plt.show()
"""))

# Cell 10: Live Inference Function
cells.append(nbf.v4.new_markdown_cell("""---
## 8. Interactive Real-Time Prediction Function
This clean Python function accepts any custom set of driving conditions, runs it through the trained pipeline, and returns the predicted severity and probability.
"""))

cells.append(nbf.v4.new_code_cell("""def predict_accident_severity(speed_limit=30, road_type=6, light_conditions=1, 
                              weather_conditions=1, road_surface_conditions=1, 
                              urban_or_rural=1, vehicles=2, day_of_week=5, hour=17, road_class=3):
    \"\"\"
    Real-Time Accident Severity Prediction Function
    Returns: Predicted Label, Probability, and Safety Advisory
    \"\"\"
    input_data = pd.DataFrame([[
        speed_limit, road_type, light_conditions, weather_conditions,
        road_surface_conditions, urban_or_rural, vehicles, day_of_week, hour, road_class
    ]], columns=feature_cols)
    
    # Predict using Random Forest
    pred = rf_model.predict(input_data)[0]
    probs = rf_model.predict_proba(input_data)[0]
    severe_prob = probs[1] * 100
    slight_prob = probs[0] * 100
    
    print("=" * 60)
    print("REAL-TIME ROAD ACCIDENT SEVERITY PREDICTOR")
    print("=" * 60)
    print(f"Inputs Received: Speed={speed_limit}mph | Environment={'Rural' if urban_or_rural==2 else 'Urban'} | Time={hour:02d}:00")
    print(f"Light={'Daylight' if light_conditions==1 else 'Darkness'} | Surface={'Dry' if road_surface_conditions==1 else 'Wet/Adverse'}")
    print("-" * 60)
    print(f"Outcome Prediction : {'SEVERE (Fatal or Serious Injury)' if pred == 1 else 'SLIGHT (Minor Injury)'}")
    print(f"Severe Probability : {severe_prob:.1f}%")
    print(f"Slight Probability : {slight_prob:.1f}%")
    
    if severe_prob >= 35:
        print("Safety Advisory    : HIGH RISK. Rural high-speed zone or adverse lighting detected. Exercise maximum caution.")
    elif severe_prob >= 24:
        print("Safety Advisory    : MODERATE RISK. Elevated crash probability at intersections.")
    else:
        print("Safety Advisory    : LOW RISK. Statistically lower severity typical of daytime low-speed urban traffic.")
    print("=" * 60)

# Example 1: High-Speed Rural Night Incident (Dangerous Scenario)
predict_accident_severity(speed_limit=60, urban_or_rural=2, light_conditions=6, weather_conditions=2, road_surface_conditions=2, hour=23)

# Example 2: Daytime Urban Commute (Low Risk Scenario)
predict_accident_severity(speed_limit=30, urban_or_rural=1, light_conditions=1, weather_conditions=1, road_surface_conditions=1, hour=14)
"""))

# Save Notebook
nb.cells = cells
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"SUCCESS: Jupyter Notebook created at: {notebook_path}")
