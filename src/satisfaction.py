import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import mlflow
import mlflow.sklearn

def compute_engagement_score(user_agg, kmeans_engagement, scaler_engagement):
    """Compute engagement score using Euclidean distance"""
    metrics = user_agg[['sessions', 'total_duration', 'total_traffic']].copy()
    metrics_normalized = scaler_engagement.transform(metrics)
    least_engaged_idx = np.argmin([
        kmeans_engagement.cluster_centers_[i].sum()
        for i in range(kmeans_engagement.n_clusters)
    ])
    least_engaged_centroid = kmeans_engagement.cluster_centers_[least_engaged_idx]
    user_agg['engagement_score'] = [
        np.linalg.norm(row - least_engaged_centroid)
        for row in metrics_normalized
    ]
    print("Engagement scores computed!")
    return user_agg

def compute_experience_score(experience, kmeans_experience, scaler_experience):
    """Compute experience score using Euclidean distance"""
    features = experience[['avg_tcp', 'avg_rtt', 'avg_throughput']].copy()
    features_normalized = scaler_experience.transform(features)
    worst_exp_idx = np.argmax([
        kmeans_experience.cluster_centers_[i].sum()
        for i in range(kmeans_experience.n_clusters)
    ])
    worst_exp_centroid = kmeans_experience.cluster_centers_[worst_exp_idx]
    experience['experience_score'] = [
        np.linalg.norm(row - worst_exp_centroid)
        for row in features_normalized
    ]
    print("Experience scores computed!")
    return experience

def compute_satisfaction_score(user_agg, experience):
    """Compute satisfaction score"""
    merged = user_agg[['MSISDN/Number', 'engagement_score']].merge(
        experience[['MSISDN/Number', 'experience_score']],
        on='MSISDN/Number',
        how='inner'
    )
    merged['satisfaction_score'] = (
        merged['engagement_score'] + merged['experience_score']
    ) / 2
    print("\nTop 10 Satisfied Customers:")
    print(merged.nlargest(10, 'satisfaction_score')[
        ['MSISDN/Number', 'engagement_score',
         'experience_score', 'satisfaction_score']
    ])
    return merged

def build_regression_model(merged):
    """Build regression model to predict satisfaction score"""
    X = merged[['engagement_score', 'experience_score']]
    y = merged['satisfaction_score']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2_score", r2)
        mlflow.sklearn.log_model(model, "satisfaction_model")
        print(f"\nModel Results:")
        print(f"MSE: {mse:.4f}")
        print(f"R2 Score: {r2:.4f}")
    return model

def cluster_satisfaction(merged, k=2):
    """Run KMeans on engagement and experience scores"""
    features = merged[['engagement_score', 'experience_score']]
    scaler = MinMaxScaler()
    features_normalized = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=k, random_state=42)
    merged['satisfaction_cluster'] = kmeans.fit_predict(features_normalized)
    print("\nSatisfaction Cluster Summary:")
    summary = merged.groupby('satisfaction_cluster').agg(
        avg_satisfaction=('satisfaction_score', 'mean'),
        avg_experience=('experience_score', 'mean'),
        avg_engagement=('engagement_score', 'mean'),
        count=('MSISDN/Number', 'count')
    )
    print(summary)
    return merged
