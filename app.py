"""
Flask Web Application & REST API
Road Accident Prediction and Analytics Dashboard Using Machine Learning
UK STATS19 Road Safety Dataset (2021-2025)
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# Helper to load JSON safely
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

# Load Cached Reports
KPIS = load_json(os.path.join(DATA_DIR, "dashboard_kpis.json"))
PREPROC_REPORT = load_json(os.path.join(REPORT_DIR, "data_preprocessing_report.json"))
REG_RESULTS = load_json(os.path.join(REPORT_DIR, "regression_results.json"))
CLF_RESULTS = load_json(os.path.join(REPORT_DIR, "classification_results.json"))
CLUSTER_RESULTS = load_json(os.path.join(REPORT_DIR, "clustering_results.json"))
PCA_NN_RESULTS = load_json(os.path.join(REPORT_DIR, "pca_nn_results.json"))
ENSEMBLE_RESULTS = load_json(os.path.join(REPORT_DIR, "ensemble_comparison_results.json"))
MAP_POINTS = load_json(os.path.join(DATA_DIR, "map_sample_points.json"))
MATRIX_HEATMAPS = load_json(os.path.join(DATA_DIR, "matrix_heatmaps.json"))

# Load Prediction Model & Scaler (Random Forest & Scaler)
try:
    PRED_MODEL = joblib.load(os.path.join(MODEL_DIR, "clf_random_forest.joblib"))
    PRED_SCALER = joblib.load(os.path.join(MODEL_DIR, "classification_scaler.joblib"))
except Exception as e:
    print(f"Warning: Could not load default prediction model: {e}")
    PRED_MODEL = None
    PRED_SCALER = None

FEATURE_ORDER = [
    'speed_limit', 'road_type', 'light_conditions', 'weather_conditions',
    'road_surface_conditions', 'urban_or_rural_area', 'number_of_vehicles',
    'day_of_week', 'hour', 'first_road_class'
]

# -------------------------------------------------------------
# Frontend Page Routes
# -------------------------------------------------------------

@app.route('/')
def page_dashboard():
    return render_template('index.html', kpis=KPIS, active_page='dashboard')

@app.route('/heatmap')
def page_heatmap():
    return render_template('heatmap.html', matrix_data=MATRIX_HEATMAPS, active_page='heatmap')

@app.route('/dataset')
def page_dataset():
    return render_template('dataset.html', report=PREPROC_REPORT, kpis=KPIS, active_page='dataset')

@app.route('/regression')
def page_regression():
    return render_template('regression.html', data=REG_RESULTS, active_page='regression')

@app.route('/classification')
def page_classification():
    return render_template('classification.html', data=CLF_RESULTS, active_page='classification')

@app.route('/clustering')
def page_clustering():
    return render_template('clustering.html', data=CLUSTER_RESULTS, active_page='clustering')

@app.route('/pca-nn')
def page_pca_nn():
    return render_template('pca.html', data=PCA_NN_RESULTS, active_page='pca-nn')

@app.route('/model-comparison')
def page_model_comparison():
    return render_template('model_comparison.html', data=ENSEMBLE_RESULTS, active_page='model-comparison')

@app.route('/predict')
def page_predict():
    return render_template('predict.html', active_page='predict')

# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "healthy",
        "dataset_records": KPIS.get("total_accidents", 0),
        "model_loaded": PRED_MODEL is not None
    })

@app.route('/api/dashboard')
def api_dashboard():
    return jsonify(KPIS)

@app.route('/api/dataset')
def api_dataset():
    return jsonify(PREPROC_REPORT)

@app.route('/api/regression')
def api_regression():
    return jsonify(REG_RESULTS)

@app.route('/api/classification')
def api_classification():
    return jsonify(CLF_RESULTS)

@app.route('/api/clustering')
def api_clustering():
    return jsonify(CLUSTER_RESULTS)

@app.route('/api/pca')
def api_pca():
    return jsonify(PCA_NN_RESULTS)

@app.route('/api/model-comparison')
def api_model_comparison():
    return jsonify(ENSEMBLE_RESULTS)

@app.route('/api/map-points')
def api_map_points():
    return jsonify(MAP_POINTS)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if PRED_MODEL is None:
        return jsonify({"error": "Prediction model not loaded"}), 500
        
    try:
        data = request.get_json(force=True)
        
        # Extract features with defaults
        speed_limit = float(data.get('speed_limit', 30))
        road_type = int(data.get('road_type', 6)) # 6: Single carriageway
        light_conditions = int(data.get('light_conditions', 1)) # 1: Daylight
        weather_conditions = int(data.get('weather_conditions', 1)) # 1: Fine
        road_surface_conditions = int(data.get('road_surface_conditions', 1)) # 1: Dry
        urban_or_rural_area = int(data.get('urban_or_rural_area', 1)) # 1: Urban
        number_of_vehicles = int(data.get('number_of_vehicles', 2))
        day_of_week = int(data.get('day_of_week', 4)) # 4: Wednesday
        hour = int(data.get('hour', 14)) # 14: 2 PM
        first_road_class = int(data.get('first_road_class', 3)) # 3: A-road
        
        input_row = pd.DataFrame([[
            speed_limit, road_type, light_conditions, weather_conditions,
            road_surface_conditions, urban_or_rural_area, number_of_vehicles,
            day_of_week, hour, first_road_class
        ]], columns=FEATURE_ORDER)
        
        # Predict using Random Forest
        prediction = int(PRED_MODEL.predict(input_row)[0])
        probabilities = PRED_MODEL.predict_proba(input_row)[0].tolist()
        
        severe_prob = round(float(probabilities[1] * 100), 2)
        slight_prob = round(float(probabilities[0] * 100), 2)
        
        # Risk assessment level
        if severe_prob >= 40:
            risk_level = "HIGH RISK"
            badge_class = "danger"
            advice = "High risk of fatal or serious injury. Rural high-speed conditions, unlit roads, or adverse surface conditions detected."
        elif severe_prob >= 25:
            risk_level = "MODERATE RISK"
            badge_class = "warning"
            advice = "Elevated risk of injury. Exercise caution at junctions and maintain safe following distances."
        else:
            risk_level = "LOW RISK"
            badge_class = "success"
            advice = "Statistically lower probability of severe injury, typical of low-speed daylight urban driving."
            
        return jsonify({
            "success": True,
            "prediction": prediction,
            "prediction_label": "Severe (Fatal or Serious)" if prediction == 1 else "Slight (Minor Injury)",
            "severe_probability": severe_prob,
            "slight_probability": slight_prob,
            "risk_level": risk_level,
            "badge_class": badge_class,
            "advice": advice,
            "model_used": "Balanced Random Forest Classifier (Trained on UK STATS19 microdata)",
            "features_received": {
                "Speed Limit": f"{int(speed_limit)} mph",
                "Environment": "Rural" if urban_or_rural_area == 2 else "Urban",
                "Light": "Darkness" if light_conditions > 1 else "Daylight",
                "Surface": "Wet/Adverse" if road_surface_conditions > 1 else "Dry",
                "Hour": f"{hour:02d}:00"
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Road Accident Analytics Dashboard on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
