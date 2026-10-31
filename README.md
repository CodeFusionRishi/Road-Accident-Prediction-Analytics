# Road Accident Prediction and Analytics Dashboard Using Machine Learning

An academic and production-grade predictive analytics platform engineered on **513,801 official collision records (2021–2025)** from the UK Department for Transport (DfT) STATS19 database.

This project was developed for a BTech Computer Science curriculum under the **Predictive Analytics** course, fulfilling all practical and experimental requirements across all **six units of the syllabus**.

---

## 🚀 Key Highlights & Features

1. **Empirical Open Government Data**:
   * Extracted from the 1.46 GB UK Government STATS19 microdata repository (1979–2025).
   * Filtered to recent 5 years (**2021–2025**) to ensure modern vehicular safety relevance and 99.9% complete GPS coordinates.
   * Total validated records: **513,801 collisions**.

2. **Full Curriculum Syllabus Mapping (Units I – VI)**:
   * **Unit I (Data Preparation & EDA)**: Special missing code (`-1`) handling, temporal feature engineering, class imbalance analysis, and environmental distributions.
   * **Unit II (Regression)**: Monthly nationwide collision count prediction using Simple Linear Regression, Multiple Linear Regression, and Polynomial Regression ($R^2 = 0.9889$, $\text{RMSE} = 94.65$).
   * **Unit III (Classification)**: Binary severity prediction (Severe [Fatal/Serious] vs Slight) benchmarking Logistic Regression, Gaussian Naive Bayes, KNN, Decision Tree, Support Vector Machine (SGD), Random Forest, and Gradient Boosting.
   * **Unit IV (Unsupervised Clustering & Patterns)**: K-Means with Elbow Method ($k=2..6$) and Silhouette analysis, Hierarchical Agglomerative Clustering (Ward linkage), 2D PCA cluster projection, and frequent condition association rules.
   * **Unit V (PCA & Neural Networks)**: Principal Component Analysis (scree plot, explained variance, loadings, before vs after PCA model comparison), and Feedforward Neural Network (Multi-Layer Perceptron / MLPClassifier with ReLU and Adam).
   * **Unit VI (Ensembles & Model Performance)**: Bagging vs. Random Forest vs. Boosting, Gini feature importance analysis, master leaderboard of all 9 algorithms, and academic bias-variance tradeoff matrix.

3. **Interactive Web Dashboard**:
   * **Frontend**: HTML5, CSS3, JavaScript, Chart.js 4, Leaflet.js (dark tile mapping), responsive layout.
   * **Backend**: Python 3, Flask 3.1 REST API, Scikit-Learn pipelines, Joblib model serialization.
   * **Live Severity Risk Predictor**: Form allowing examiners or users to enter customized road conditions, generating real-time predictions and severity probabilities.

---

## 📂 Project Directory Structure

```text
road-accident-project/
│
├── app.py                      # Flask Application & REST API
├── requirements.txt            # Python Dependencies
├── README.md                   # Comprehensive Project Documentation
│
├── data/
│   ├── raw/                    # Raw source pointers
│   └── processed/              # Cleaned microdata, stratified samples, KPIs, geo points
│       ├── dashboard_kpis.json
│       ├── map_sample_points.json
│       ├── monthly_accident_regression.csv
│       └── uk_accidents_sample_100k.csv
│
├── models/                     # Trained Serialized Scikit-Learn Models (.joblib)
│   ├── clf_random_forest.joblib
│   ├── clf_gradient_boosting.joblib
│   ├── clf_logistic_regression.joblib
│   ├── clf_neural_network_mlp.joblib
│   ├── clf_bagging.joblib
│   ├── regression_mlr.joblib
│   ├── regression_plr.joblib
│   ├── kmeans_optimal.joblib
│   ├── pca_3comp.joblib
│   └── classification_scaler.joblib
│
├── reports/                    # Generated Metrics & Academic JSON Artifacts
│   ├── data_preprocessing_report.json
│   ├── regression_results.json
│   ├── classification_results.json
│   ├── clustering_results.json
│   ├── pca_nn_results.json
│   └── ensemble_comparison_results.json
│
├── src/                        # Machine Learning Pipeline Source Code
│   ├── data_cleaning.py        # Chunk-based ingestion, imputation, feature engineering
│   ├── regression.py           # Unit II Regression experiments
│   ├── classification.py       # Unit III Classification experiments
│   ├── clustering.py           # Unit IV Clustering experiments
│   ├── pca_neural_network.py   # Unit V PCA & MLP Neural Network experiments
│   ├── ensemble.py             # Unit VI Ensemble learning & Master Leaderboard
│   └── train_all.py            # Master orchestration script
│
├── static/
│   ├── css/style.css           # Premium Dark Navy Theme CSS
│   └── js/main.js
│
└── templates/                  # Jinja2 Modular Web Templates
    ├── base.html               # Master layout with sidebar navigation
    ├── index.html              # Executive Dashboard Overview (KPIs, Leaflet map)
    ├── dataset.html            # Unit I: Dataset Analysis & EDA
    ├── regression.html         # Unit II: Regression Analysis
    ├── classification.html     # Unit III: Classification Analysis
    ├── clustering.html         # Unit IV: Clustering & Pattern Detection
    ├── pca.html                # Unit V: PCA & Neural Networks
    ├── model_comparison.html   # Unit VI: Ensembles & Master Evaluation
    ├── predict.html            # Interactive Live Severity Predictor
    └── about.html              # Syllabus Mapping & Academic Viva Guide
```

---

## 🛠️ Installation & Setup Instructions

### 1. Prerequisites
* Python 3.10+ installed
* pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Experiments & Train Models (Optional - Already Pre-trained)
If you wish to re-execute the entire machine learning pipeline:
```bash
python src/train_all.py
```

### 4. Launch the Web Dashboard
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📊 Summary of Model Results

### Unit II: Regression (Monthly Accident Count Prediction)
| Model | MAE | RMSE | $R^2$ Score | Key Takeaway |
| :--- | :---: | :---: | :---: | :--- |
| **Simple Linear Regression** | 98.41 | 118.77 | 0.9825 | Strong linear relationship with vehicle volume. |
| **Multiple Linear Regression** | 79.82 | 98.25 | 0.9880 | Incorporates casualty severity and time index. |
| **Polynomial Regression (Deg 2)** | **75.40** | **94.65** | **0.9889** | **Best Fit:** Models non-linear congestion interactions. |

### Unit III, V, VI: Classification Master Leaderboard
| Rank | Algorithm | Category | Accuracy | Weighted F1 | ROC-AUC | Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **#1** | **Gaussian Naive Bayes** | Probabilistic | 72.25% | **0.6866** | 0.6043 | Top Baseline |
| **#2** | **K-Nearest Neighbors** | Non-parametric | 72.82% | **0.6765** | 0.5499 | Distance Metric |
| **#3** | **Random Forest** | Ensemble (Bagging) | 63.67% | **0.6575** | **0.6254** | **Production Model** |
| **#4** | **Multi-Layer Perceptron (MLP)** | Neural Network | **75.72%** | **0.6559** | 0.6271 | Deep Architecture |
| **#5** | **Decision Tree** | Tree | 62.91% | **0.6512** | 0.6121 | White-box baseline |
| **#6** | **Gradient Boosting** | Ensemble (Boosting) | 61.48% | **0.6406** | **0.6280** | Residual correction |
| **#7** | **Bagging (Decision Trees)** | Ensemble (Bagging) | 63.15% | **0.6380** | 0.6185 | Variance reduction |
| **#8** | **Support Vector Machine (SGD)** | Linear / Margin | 58.64% | **0.6151** | 0.5909 | Maximum margin |
| **#9** | **Logistic Regression** | Linear | 57.96% | **0.6094** | 0.5977 | Balanced baseline |

---

## 🎓 Academic Viva Defense Guide

1. **Why aggregate accident counts for Regression instead of regression on raw rows?**
   * *Answer*: On raw rows, severity is ordinal and discrete (1, 2, 3). Running OLS regression on discrete codes violates homoscedasticity and normality of residuals. Monthly counts form a continuous dependent variable ($Y \in \mathbb{R}^+$) suitable for linear and polynomial regression.
2. **How was the severe class imbalance handled?**
   * *Answer*: Slight collisions account for ~76% while severe collisions account for ~24%. We applied `class_weight='balanced'` to penalize false negatives on rare severe crashes and benchmarked algorithms using Weighted/Macro F1-scores and ROC-AUC rather than misleading raw Accuracy.
3. **What is the mathematical difference between Bagging and Boosting?**
   * *Answer*: Bagging trains independent base estimators in parallel on bootstrap samples to reduce model variance. Gradient Boosting trains base estimators sequentially, where each new tree fits the pseudo-residuals of the previous ensemble to reduce bias.
4. **How does PCA help?**
   * *Answer*: PCA projects correlated road features onto orthogonal principal axes. 3 principal components preserved ~40% of variance while retaining ~98% of the classification F1-score, proving significant dimensionality compression with minimal loss in discriminatory power.
