import pytest
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import clean_data, get_user_aggregation
from src.feature_store import save_features, load_features
from src.engagement import get_top10_per_metric, normalize_and_cluster
from src.experience import get_experience_metrics, cluster_experience
from src.satisfaction import compute_satisfaction_score, cluster_satisfaction

def create_sample_data():
    data = {
        'Bearer Id': [1, 2, 3, 4, 5],
        'MSISDN/Number': [111, 222, 111, 333, 222],
        'Dur. (ms)': [1000, 2000, None, 3000, 4000],
        'Total DL (Bytes)': [500, 600, 700, None, 900],
        'Total UL (Bytes)': [100, 200, 300, 400, None],
        'Social Media DL (Bytes)': [10, 20, 30, 40, 50],
        'Social Media UL (Bytes)': [5, 10, 15, 20, 25],
        'Youtube DL (Bytes)': [100, 200, 300, 400, 500],
        'Youtube UL (Bytes)': [50, 100, 150, 200, 250],
        'Netflix DL (Bytes)': [10, 20, 30, 40, 50],
        'Netflix UL (Bytes)': [5, 10, 15, 20, 25],
        'Google DL (Bytes)': [10, 20, 30, 40, 50],
        'Google UL (Bytes)': [5, 10, 15, 20, 25],
        'Email DL (Bytes)': [10, 20, 30, 40, 50],
        'Email UL (Bytes)': [5, 10, 15, 20, 25],
        'Gaming DL (Bytes)': [10, 20, 30, 40, 50],
        'Gaming UL (Bytes)': [5, 10, 15, 20, 25],
        'Other DL (Bytes)': [10, 20, 30, 40, 50],
        'Other UL (Bytes)': [5, 10, 15, 20, 25],
        'Handset Type': ['iPhone', 'Samsung', 'iPhone', 'Huawei', 'Samsung'],
        'Handset Manufacturer': ['Apple', 'Samsung', 'Apple', 'Huawei', 'Samsung'],
    }
    return pd.DataFrame(data)

def create_experience_sample():
    data = {
        'MSISDN/Number': [111, 222, 111, 333, 222],
        'TCP DL Retrans. Vol (Bytes)': [100, 200, 150, 300, 250],
        'TCP UL Retrans. Vol (Bytes)': [50, 100, 75, 150, 125],
        'Avg RTT DL (ms)': [10, 20, 15, 30, 25],
        'Avg RTT UL (ms)': [5, 10, 8, 15, 12],
        'Avg Bearer TP DL (kbps)': [1000, 2000, 1500, 3000, 2500],
        'Avg Bearer TP UL (kbps)': [500, 1000, 750, 1500, 1250],
        'Handset Type': ['iPhone', 'Samsung', 'iPhone', 'Huawei', 'Samsung'],
    }
    return pd.DataFrame(data)

def test_clean_data_removes_nulls():
    df = create_sample_data()
    cleaned = clean_data(df)
    assert cleaned.isnull().sum().sum() == 0

def test_clean_data_returns_dataframe():
    df = create_sample_data()
    cleaned = clean_data(df)
    assert isinstance(cleaned, pd.DataFrame)

def test_clean_data_keeps_shape():
    df = create_sample_data()
    cleaned = clean_data(df)
    assert cleaned.shape[0] == df.shape[0]

def test_user_aggregation_returns_dataframe():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    assert isinstance(user_agg, pd.DataFrame)

def test_user_aggregation_unique_users():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    assert len(user_agg) == 3

def test_user_aggregation_has_total_traffic():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    assert 'total_traffic' in user_agg.columns

def test_user_aggregation_sessions_count():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    user_111 = user_agg[user_agg['MSISDN/Number'] == 111]
    assert user_111['sessions'].values[0] == 2

def test_save_and_load_features():
    df = create_sample_data()
    save_features(df, 'test_features')
    loaded = load_features('test_features')
    assert loaded is not None
    assert len(loaded) == len(df)

def test_load_nonexistent_file():
    result = load_features('nonexistent_file_xyz')
    assert result is None

def test_get_top10_per_metric():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    get_top10_per_metric(user_agg)

def test_normalize_and_cluster():
    df = create_sample_data()
    cleaned = clean_data(df)
    user_agg = get_user_aggregation(cleaned)
    result, kmeans, scaler = normalize_and_cluster(user_agg, k=2)
    assert 'engagement_cluster' in result.columns

def test_get_experience_metrics():
    df = create_experience_sample()
    experience = get_experience_metrics(df)
    assert isinstance(experience, pd.DataFrame)
    assert 'avg_tcp' in experience.columns
    assert 'avg_rtt' in experience.columns
    assert 'avg_throughput' in experience.columns

def test_experience_unique_users():
    df = create_experience_sample()
    experience = get_experience_metrics(df)
    assert len(experience) == 3

def test_cluster_experience():
    df = create_experience_sample()
    experience = get_experience_metrics(df)
    result, kmeans, scaler = cluster_experience(experience, k=2)
    assert 'experience_cluster' in result.columns

def test_compute_satisfaction_score():
    user_agg = pd.DataFrame({
        'MSISDN/Number': [111, 222, 333],
        'engagement_score': [0.5, 0.8, 0.3],
    })
    experience = pd.DataFrame({
        'MSISDN/Number': [111, 222, 333],
        'experience_score': [0.6, 0.7, 0.4],
    })
    merged = compute_satisfaction_score(user_agg, experience)
    assert 'satisfaction_score' in merged.columns
    assert len(merged) == 3

def test_satisfaction_score_is_average():
    user_agg = pd.DataFrame({
        'MSISDN/Number': [111],
        'engagement_score': [0.4],
    })
    experience = pd.DataFrame({
        'MSISDN/Number': [111],
        'experience_score': [0.6],
    })
    merged = compute_satisfaction_score(user_agg, experience)
    assert merged['satisfaction_score'].values[0] == 0.5

def test_cluster_satisfaction():
    merged = pd.DataFrame({
        'MSISDN/Number': [111, 222, 333, 444],
        'engagement_score': [0.5, 0.8, 0.3, 0.6],
        'experience_score': [0.6, 0.7, 0.4, 0.5],
        'satisfaction_score': [0.55, 0.75, 0.35, 0.55],
    })
    result = cluster_satisfaction(merged, k=2)
    assert 'satisfaction_cluster' in result.columns
