import pandas as pd
from src.data_loader import load_data, clean_data, get_user_aggregation
from src.feature_store import save_features, load_features
from src.engagement import (get_top10_per_metric, normalize_and_cluster,
                             plot_top3_apps, elbow_method)
from src.experience import (get_experience_metrics, get_top_bottom_frequent,
                             plot_throughput_per_handset, plot_tcp_per_handset,
                             cluster_experience)
from src.satisfaction import (compute_engagement_score, compute_experience_score,
                               compute_satisfaction_score, build_regression_model,
                               cluster_satisfaction)

# ============================================
# LOAD AND CLEAN DATA
# ============================================
print("="*50)
print("STEP 1 - Loading and Cleaning Data")
print("="*50)
df = load_data('data/telecom_data.xlsx')
df = clean_data(df)

# ============================================
# TASK 1 - USER OVERVIEW
# ============================================
print("\n" + "="*50)
print("TASK 1 - User Overview Analysis")
print("="*50)

# Top 10 handsets
print("\nTop 10 Handsets:")
print(df['Handset Type'].value_counts().head(10))

# Top 3 manufacturers
print("\nTop 3 Manufacturers:")
print(df['Handset Manufacturer'].value_counts().head(3))

# Top 5 handsets per top 3 manufacturers
top3_manufacturers = df['Handset Manufacturer'].value_counts().head(3).index
for manufacturer in top3_manufacturers:
    print(f"\nTop 5 Handsets for {manufacturer}:")
    filtered = df[df['Handset Manufacturer'] == manufacturer]
    print(filtered['Handset Type'].value_counts().head(5))

# User aggregation
user_agg = get_user_aggregation(df)
save_features(user_agg, 'user_aggregation')

# ============================================
# TASK 2 - USER ENGAGEMENT
# ============================================
print("\n" + "="*50)
print("TASK 2 - User Engagement Analysis")
print("="*50)

get_top10_per_metric(user_agg)
user_agg, kmeans_engagement, scaler_engagement = normalize_and_cluster(user_agg, k=3)
plot_top3_apps(user_agg)
elbow_method(user_agg)
save_features(user_agg, 'engagement_features')

# ============================================
# TASK 3 - USER EXPERIENCE
# ============================================
print("\n" + "="*50)
print("TASK 3 - User Experience Analysis")
print("="*50)

experience = get_experience_metrics(df)
get_top_bottom_frequent(experience)
plot_throughput_per_handset(experience)
plot_tcp_per_handset(experience)
experience, kmeans_experience, scaler_experience = cluster_experience(experience, k=3)
save_features(experience, 'experience_features')

# ============================================
# TASK 4 - USER SATISFACTION
# ============================================
print("\n" + "="*50)
print("TASK 4 - User Satisfaction Analysis")
print("="*50)

user_agg = compute_engagement_score(user_agg, kmeans_engagement, scaler_engagement)
experience = compute_experience_score(experience, kmeans_experience, scaler_experience)
merged = compute_satisfaction_score(user_agg, experience)
model = build_regression_model(merged)
merged = cluster_satisfaction(merged, k=2)
save_features(merged, 'satisfaction_scores')

print("\n" + "="*50)
print("ALL TASKS COMPLETED SUCCESSFULLY!")
print("="*50)