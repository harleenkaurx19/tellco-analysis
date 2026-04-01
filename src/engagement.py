import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def get_top10_per_metric(user_agg):
    """Get top 10 customers per engagement metric"""
    
    print("Top 10 by Sessions:")
    print(user_agg.nlargest(10, 'sessions')[['MSISDN/Number', 'sessions']])
    
    print("\nTop 10 by Duration:")
    print(user_agg.nlargest(10, 'total_duration')[['MSISDN/Number', 'total_duration']])
    
    print("\nTop 10 by Total Traffic:")
    print(user_agg.nlargest(10, 'total_traffic')[['MSISDN/Number', 'total_traffic']])

def normalize_and_cluster(user_agg, k=3):
    """Normalize metrics and run KMeans clustering"""
    
    # Select engagement metrics
    metrics = user_agg[['sessions', 'total_duration', 'total_traffic']].copy()
    
    # Normalize
    scaler = MinMaxScaler()
    metrics_normalized = scaler.fit_transform(metrics)
    
    # KMeans clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    user_agg['engagement_cluster'] = kmeans.fit_predict(metrics_normalized)
    
    print("\nCluster Summary:")
    cluster_summary = user_agg.groupby('engagement_cluster').agg(
        min_sessions=('sessions', 'min'),
        max_sessions=('sessions', 'max'),
        avg_sessions=('sessions', 'mean'),
        total_sessions=('sessions', 'sum'),
        min_duration=('total_duration', 'min'),
        max_duration=('total_duration', 'max'),
        avg_duration=('total_duration', 'mean'),
        min_traffic=('total_traffic', 'min'),
        max_traffic=('total_traffic', 'max'),
        avg_traffic=('total_traffic', 'mean'),
    )
    print(cluster_summary)
    
    return user_agg, kmeans, scaler

def plot_top3_apps(user_agg):
    """Plot top 3 most used applications"""
    
    app_totals = {
        'Social Media': user_agg['social_media'].sum(),
        'YouTube': user_agg['youtube'].sum(),
        'Netflix': user_agg['netflix'].sum(),
        'Google': user_agg['google'].sum(),
        'Email': user_agg['email'].sum(),
        'Gaming': user_agg['gaming'].sum(),
        'Other': user_agg['other'].sum(),
    }
    
    # Sort and get top 3
    app_df = pd.Series(app_totals).sort_values(ascending=False)
    top3 = app_df.head(3)
    
    # Plot
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top3.index, y=top3.values, palette='viridis')
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Data (Bytes)')
    plt.tight_layout()
    plt.savefig('data/top3_apps.png')
    plt.show()
    print("Chart saved!")

def elbow_method(user_agg):
    """Find optimal k using elbow method"""
    
    metrics = user_agg[['sessions', 'total_duration', 'total_traffic']].copy()
    scaler = MinMaxScaler()
    metrics_normalized = scaler.fit_transform(metrics)
    
    inertias = []
    k_range = range(1, 11)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(metrics_normalized)
        inertias.append(kmeans.inertia_)
    
    # Plot elbow curve
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, inertias, 'bo-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method - Finding Optimal k')
    plt.tight_layout()
    plt.savefig('data/elbow_curve.png')
    plt.show()
    print("Elbow curve saved!")