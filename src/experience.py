import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def get_experience_metrics(df):
    """Aggregate experience metrics per user"""
    experience = df.groupby('MSISDN/Number').agg(
        avg_tcp_dl=('TCP DL Retrans. Vol (Bytes)', 'mean'),
        avg_tcp_ul=('TCP UL Retrans. Vol (Bytes)', 'mean'),
        avg_rtt_dl=('Avg RTT DL (ms)', 'mean'),
        avg_rtt_ul=('Avg RTT UL (ms)', 'mean'),
        avg_tp_dl=('Avg Bearer TP DL (kbps)', 'mean'),
        avg_tp_ul=('Avg Bearer TP UL (kbps)', 'mean'),
        handset_type=('Handset Type', lambda x: x.mode()[0]),
    ).reset_index()
    experience['avg_tcp'] = (experience['avg_tcp_dl'] + experience['avg_tcp_ul']) / 2
    experience['avg_rtt'] = (experience['avg_rtt_dl'] + experience['avg_rtt_ul']) / 2
    experience['avg_throughput'] = (experience['avg_tp_dl'] + experience['avg_tp_ul']) / 2
    print(f"Experience metrics done! {len(experience)} users")
    return experience

def get_top_bottom_frequent(experience):
    """Get top, bottom and most frequent values"""
    for metric in ['avg_tcp', 'avg_rtt', 'avg_throughput']:
        print(f"\n--- {metric} ---")
        print(f"Top 10:\n{experience.nlargest(10, metric)[metric].values}")
        print(f"Bottom 10:\n{experience.nsmallest(10, metric)[metric].values}")
        print(f"Most Frequent:\n{experience[metric].value_counts().head(10)}")

def plot_throughput_per_handset(experience):
    """Plot average throughput per handset type"""
    handset_tp = experience.groupby('handset_type')['avg_throughput'].mean()
    handset_tp = handset_tp.sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=handset_tp.values, y=handset_tp.index, palette='coolwarm')
    plt.title('Average Throughput per Handset Type (Top 10)')
    plt.xlabel('Average Throughput (kbps)')
    plt.ylabel('Handset Type')
    plt.tight_layout()
    plt.savefig('data/throughput_per_handset.png')
    plt.show()
    print("Chart saved!")

def plot_tcp_per_handset(experience):
    """Plot average TCP retransmission per handset type"""
    handset_tcp = experience.groupby('handset_type')['avg_tcp'].mean()
    handset_tcp = handset_tcp.sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=handset_tcp.values, y=handset_tcp.index, palette='Reds')
    plt.title('Average TCP Retransmission per Handset Type (Top 10)')
    plt.xlabel('Average TCP Retransmission (Bytes)')
    plt.ylabel('Handset Type')
    plt.tight_layout()
    plt.savefig('data/tcp_per_handset.png')
    plt.show()
    print("Chart saved!")

def cluster_experience(experience, k=3):
    """KMeans clustering on experience metrics"""
    features = experience[['avg_tcp', 'avg_rtt', 'avg_throughput']].copy()
    scaler = MinMaxScaler()
    features_normalized = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=k, random_state=42)
    experience['experience_cluster'] = kmeans.fit_predict(features_normalized)
    print("\nExperience Cluster Summary:")
    summary = experience.groupby('experience_cluster').agg(
        avg_tcp=('avg_tcp', 'mean'),
        avg_rtt=('avg_rtt', 'mean'),
        avg_throughput=('avg_throughput', 'mean'),
        count=('MSISDN/Number', 'count')
    )
    print(summary)
    return experience, kmeans, scaler
