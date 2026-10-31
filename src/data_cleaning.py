"""
Data Inspection & Cleaning Pipeline
Filters UK STATS19 Road Safety dataset for recent 5 years (2021-2025),
handles missing values and special -1 codes, extracts time features,
and generates clean datasets for analysis and ML modeling.
"""

import os
import json
import pandas as pd
import numpy as np

RAW_DATA_PATH = r"D:\predictive analytics project\dft-road-casualty-statistics-collision-1979-latest-published-year.csv"
OUTPUT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\data\processed"
REPORT_DIR = r"C:\Users\RISHIKESH\.gemini\antigravity\scratch\road-accident-project\reports"

# DfT STATS19 Human Readable Mappings
SEVERITY_MAP = {1: "Fatal", 2: "Serious", 3: "Slight"}
WEATHER_MAP = {
    1: "Fine no high winds",
    2: "Raining no high winds",
    3: "Snowing no high winds",
    4: "Fine + high winds",
    5: "Raining + high winds",
    6: "Snowing + high winds",
    7: "Fog or mist",
    8: "Other",
    9: "Unknown",
    -1: "Unknown"
}
LIGHT_MAP = {
    1: "Daylight",
    4: "Darkness - lights lit",
    5: "Darkness - lights unlit",
    6: "Darkness - no lighting",
    7: "Darkness - lighting unknown",
    -1: "Unknown"
}
SURFACE_MAP = {
    1: "Dry",
    2: "Wet or damp",
    3: "Snow",
    4: "Frost or ice",
    5: "Flood over 3cm",
    -1: "Unknown"
}
ROAD_TYPE_MAP = {
    1: "Roundabout",
    2: "One way street",
    3: "Dual carriageway",
    6: "Single carriageway",
    7: "Slip road",
    9: "Unknown",
    -1: "Unknown"
}
AREA_MAP = {
    1: "Urban",
    2: "Rural",
    -1: "Unknown"
}
DAY_MAP = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

def clean_and_prepare(start_year=2021, end_year=2025):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    print(f"Reading raw data for years {start_year} to {end_year}...")
    chunks = []
    total_scanned_rows = 0
    selected_rows = 0
    
    # Selected columns
    cols_to_use = [
        'collision_index', 'collision_year', 'date', 'day_of_week', 'time',
        'latitude', 'longitude', 'collision_severity', 'number_of_vehicles',
        'number_of_casualties', 'speed_limit', 'road_type', 'light_conditions',
        'weather_conditions', 'road_surface_conditions', 'urban_or_rural_area',
        'junction_detail', 'first_road_class', 'local_authority_ons_district'
    ]
    
    chunk_size = 300000
    for chunk in pd.read_csv(RAW_DATA_PATH, usecols=cols_to_use, chunksize=chunk_size, low_memory=False):
        total_scanned_rows += len(chunk)
        subset = chunk[(chunk['collision_year'] >= start_year) & (chunk['collision_year'] <= end_year)].copy()
        if not subset.empty:
            selected_rows += len(subset)
            chunks.append(subset)
            print(f"  Collected {len(subset):,} records (Total so far: {selected_rows:,})")
            
    df = pd.concat(chunks, ignore_index=True)
    print(f"Total extracted records for {start_year}-{end_year}: {len(df):,}")
    
    # Duplicate check
    duplicates = df.duplicated(subset=['collision_index']).sum()
    if duplicates > 0:
        df = df.drop_duplicates(subset=['collision_index'])
        print(f"Removed {duplicates} duplicate records.")
        
    # Missing coordinates check
    missing_coords = df['latitude'].isna().sum()
    print(f"Missing coordinates: {missing_coords:,} ({missing_coords/len(df)*100:.2f}%)")
    # Impute missing coordinates with median or drop for geo maps
    df = df.dropna(subset=['latitude', 'longitude']).copy()
    
    # Filter valid coordinates for UK (approx lat 49 to 61, lon -8 to 2)
    df = df[(df['latitude'] >= 49.0) & (df['latitude'] <= 61.0) & 
            (df['longitude'] >= -8.5) & (df['longitude'] <= 2.5)].copy()
            
    # Parse Date & Time
    print("Parsing dates and extracting temporal features...")
    df['date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    df['month'] = df['date_dt'].dt.month
    
    # Extract hour from time string HH:MM
    def extract_hour(val):
        try:
            if pd.isna(val):
                return 12
            parts = str(val).split(':')
            return int(parts[0])
        except:
            return 12
            
    df['hour'] = df['time'].apply(extract_hour)
    
    # Map human-readable categories
    df['severity_label'] = df['collision_severity'].map(SEVERITY_MAP).fillna("Unknown")
    df['weather_label'] = df['weather_conditions'].map(WEATHER_MAP).fillna("Unknown")
    df['light_label'] = df['light_conditions'].map(LIGHT_MAP).fillna("Unknown")
    df['surface_label'] = df['road_surface_conditions'].map(SURFACE_MAP).fillna("Unknown")
    df['road_type_label'] = df['road_type'].map(ROAD_TYPE_MAP).fillna("Unknown")
    df['area_label'] = df['urban_or_rural_area'].map(AREA_MAP).fillna("Unknown")
    df['day_name'] = df['day_of_week'].map(DAY_MAP).fillna("Unknown")
    
    # Binary Severity Target for clear academic ML benchmarking:
    # 1: Severe (Fatal or Serious), 0: Slight
    df['is_severe'] = df['collision_severity'].apply(lambda x: 1 if x in [1, 2] else 0)
    
    # Save cleaned full dataset summary and report
    report = {
        "raw_dataset_path": RAW_DATA_PATH,
        "selected_years": f"{start_year} - {end_year}",
        "total_scanned_rows": int(total_scanned_rows),
        "total_extracted_rows": int(selected_rows),
        "cleaned_rows": int(len(df)),
        "removed_duplicates": int(duplicates),
        "missing_coordinates_dropped": int(missing_coords),
        "columns_count": len(df.columns),
        "features": list(df.columns),
        "severity_distribution": df['severity_label'].value_counts().to_dict(),
        "severe_binary_distribution": {
            "Slight (0)": int((df['is_severe'] == 0).sum()),
            "Severe (Fatal/Serious, 1)": int((df['is_severe'] == 1).sum())
        },
        "yearly_distribution": df['collision_year'].value_counts().sort_index().to_dict()
    }
    
    report_file = os.path.join(REPORT_DIR, "data_preprocessing_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"Preprocessing report saved to: {report_file}")
    
    # Save a 100k stratified sample for ultra-fast ML modeling and reproducible college viva demonstration
    print("Creating stratified 100,000-row sample for model training...")
    sample_df = df.groupby('collision_severity', group_keys=False).apply(
        lambda x: x.sample(n=int(100000 * len(x) / len(df)), random_state=42)
    )
    
    sample_path = os.path.join(OUTPUT_DIR, "uk_accidents_sample_100k.csv")
    sample_df.to_csv(sample_path, index=False)
    print(f"Stratified sample saved: {sample_path} ({len(sample_df):,} rows)")
    
    # Also save an aggregated monthly counts dataset for Unit II: Regression Analysis
    print("Generating monthly aggregated accident counts for Regression (Unit II)...")
    monthly_counts = df.groupby(['collision_year', 'month']).agg(
        accident_count=('collision_index', 'count'),
        total_casualties=('number_of_casualties', 'sum'),
        total_vehicles=('number_of_vehicles', 'sum'),
        avg_speed_limit=('speed_limit', 'mean'),
        severe_count=('is_severe', 'sum')
    ).reset_index()
    
    # Create time trend index: 1, 2, 3...
    monthly_counts['time_idx'] = np.arange(1, len(monthly_counts) + 1)
    
    monthly_path = os.path.join(OUTPUT_DIR, "monthly_accident_regression.csv")
    monthly_counts.to_csv(monthly_path, index=False)
    print(f"Monthly regression dataset saved: {monthly_path} ({len(monthly_counts)} months)")

    # Save summary stats JSON for quick web dashboard loading
    dashboard_kpis = {
        "total_accidents": int(len(df)),
        "total_casualties": int(df['number_of_casualties'].sum()),
        "total_vehicles": int(df['number_of_vehicles'].sum()),
        "fatal_count": int((df['collision_severity'] == 1).sum()),
        "serious_count": int((df['collision_severity'] == 2).sum()),
        "slight_count": int((df['collision_severity'] == 3).sum()),
        "fatal_pct": round(float((df['collision_severity'] == 1).mean() * 100), 2),
        "serious_pct": round(float((df['collision_severity'] == 2).mean() * 100), 2),
        "slight_pct": round(float((df['collision_severity'] == 3).mean() * 100), 2),
        "start_year": start_year,
        "end_year": end_year,
        "yearly_trend": df['collision_year'].value_counts().sort_index().to_dict(),
        "by_day_of_week": df['day_name'].value_counts().to_dict(),
        "by_hour": df['hour'].value_counts().sort_index().to_dict(),
        "by_weather": df['weather_label'].value_counts().head(6).to_dict(),
        "by_light": df['light_label'].value_counts().to_dict(),
        "by_road_surface": df['surface_label'].value_counts().head(5).to_dict(),
        "by_road_type": df['road_type_label'].value_counts().head(5).to_dict(),
        "by_area": df['area_label'].value_counts().to_dict(),
        "speed_distribution": df['speed_limit'].value_counts().sort_index().to_dict()
    }
    
    kpi_file = os.path.join(OUTPUT_DIR, "dashboard_kpis.json")
    with open(kpi_file, 'w') as f:
        json.dump(dashboard_kpis, f, indent=4)
    print(f"Dashboard KPIs saved: {kpi_file}")
    
    # Save a small geo sample (1,500 points) for fast interactive Leaflet Map in the dashboard
    geo_sample = df[['latitude', 'longitude', 'severity_label', 'collision_year', 'speed_limit', 'weather_label']].sample(n=min(2000, len(df)), random_state=42)
    geo_path = os.path.join(OUTPUT_DIR, "map_sample_points.json")
    geo_sample.to_json(geo_path, orient='records')
    print(f"Map sample points saved: {geo_path}")
    
    print("\nData preprocessing finished successfully!")

if __name__ == "__main__":
    clean_and_prepare()
