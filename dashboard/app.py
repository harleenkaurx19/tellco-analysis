import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import load_data, clean_data, get_user_aggregation

# Page config
st.set_page_config(
    page_title="TellCo Analysis Dashboard",
    page_icon="📱",
    layout="wide"
)

# Load data once
@st.cache_data
def get_data():
    df = load_data('data/telecom_data.xlsx')
    df = clean_data(df)
    return df

@st.cache_data
def get_aggregated_data():
    df = get_data()
    user_agg = get_user_aggregation(df)
    return user_agg

# Sidebar navigation
st.sidebar.title("📱 TellCo Analysis")
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["🏠 Home",
     "📊 User Overview",
     "🔥 User Engagement",
     "📡 User Experience",
     "😊 User Satisfaction"]
)

# ============================================
# HOME PAGE
# ============================================
if page == "🏠 Home":
    st.title("📱 TellCo Telecom Analytics Dashboard")
    st.markdown("### Welcome to the TellCo User Analytics Report")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    df = get_data()

    with col1:
        st.metric("Total Sessions", f"{len(df):,}")
    with col2:
        st.metric("Unique Users", f"{df['MSISDN/Number'].nunique():,}")
    with col3:
        st.metric("Handset Types", f"{df['Handset Type'].nunique():,}")
    with col4:
        st.metric("Manufacturers", f"{df['Handset Manufacturer'].nunique():,}")

    st.markdown("---")
    st.markdown("### 📌 Project Overview")
    st.info("""
    This dashboard presents a complete analysis of TellCo telecom data including:
    - **Task 1:** User Overview Analysis
    - **Task 2:** User Engagement Analysis
    - **Task 3:** User Experience Analysis
    - **Task 4:** User Satisfaction Analysis
    """)

    st.markdown("### 💡 Key Recommendation")
    st.success("""
    Based on our analysis, TellCo shows strong growth potential!
    - High user engagement on Social Media and Gaming
    - Apple and Samsung dominate the handset market
    - Clear user segments identified for targeted marketing
    """)

# ============================================
# USER OVERVIEW PAGE
# ============================================
elif page == "📊 User Overview":
    st.title("📊 User Overview Analysis")
    st.markdown("---")

    df = get_data()

    # Top 10 handsets
    st.subheader("🔝 Top 10 Handsets")
    top10_handsets = df['Handset Type'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top10_handsets.values, y=top10_handsets.index,
                palette='viridis', ax=ax)
    ax.set_title('Top 10 Handsets Used by Customers')
    ax.set_xlabel('Number of Users')
    st.pyplot(fig)

    st.markdown("---")

    # Top 3 manufacturers
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏭 Top 3 Manufacturers")
        top3_mfr = df['Handset Manufacturer'].value_counts().head(3)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top3_mfr.values, y=top3_mfr.index,
                    palette='coolwarm', ax=ax)
        ax.set_title('Top 3 Manufacturers')
        st.pyplot(fig)

    with col2:
        st.subheader("📋 Manufacturer Stats")
        st.dataframe(top3_mfr.reset_index().rename(
            columns={'Handset Manufacturer': 'Manufacturer',
                     'count': 'Users'}
        ))

    st.markdown("---")

    # Top 5 per manufacturer
    st.subheader("📱 Top 5 Handsets per Manufacturer")
    top3_names = df['Handset Manufacturer'].value_counts().head(3).index

    for mfr in top3_names:
        st.markdown(f"**{mfr}**")
        filtered = df[df['Handset Manufacturer'] == mfr]
        top5 = filtered['Handset Type'].value_counts().head(5)
        st.dataframe(top5.reset_index().rename(
            columns={'Handset Type': 'Handset', 'count': 'Users'}
        ))

# ============================================
# USER ENGAGEMENT PAGE
# ============================================
elif page == "🔥 User Engagement":
    st.title("🔥 User Engagement Analysis")
    st.markdown("---")

    user_agg = get_aggregated_data()

    # Top 10 per metric
    st.subheader("🏆 Top 10 Users by Sessions")
    st.dataframe(user_agg.nlargest(10, 'sessions')[
        ['MSISDN/Number', 'sessions', 'total_duration', 'total_traffic']
    ])

    st.markdown("---")

    # App usage chart
    st.subheader("📱 Application Usage")
    app_totals = {
        'Social Media': user_agg['social_media'].sum(),
        'YouTube': user_agg['youtube'].sum(),
        'Netflix': user_agg['netflix'].sum(),
        'Google': user_agg['google'].sum(),
        'Email': user_agg['email'].sum(),
        'Gaming': user_agg['gaming'].sum(),
        'Other': user_agg['other'].sum(),
    }
    app_df = pd.Series(app_totals).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=app_df.index, y=app_df.values, palette='viridis', ax=ax)
    ax.set_title('Total Data Usage per Application')
    ax.set_xlabel('Application')
    ax.set_ylabel('Total Data (Bytes)')
    st.pyplot(fig)

    st.markdown("---")

    # Elbow curve
    st.subheader("📈 Elbow Method Chart")
    st.image('data/elbow_curve.png')

# ============================================
# USER EXPERIENCE PAGE
# ============================================
elif page == "📡 User Experience":
    st.title("📡 User Experience Analysis")
    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📶 Throughput per Handset")
        st.image('data/throughput_per_handset.png')

    with col2:
        st.subheader("🔄 TCP Retransmission per Handset")
        st.image('data/tcp_per_handset.png')

    st.markdown("---")

    # Experience features
    st.subheader("📊 Experience Metrics Summary")
    experience = pd.read_csv('data/experience_features.csv')
    st.dataframe(experience[[
        'MSISDN/Number', 'avg_tcp', 'avg_rtt',
        'avg_throughput', 'experience_cluster'
    ]].head(20))

# ============================================
# USER SATISFACTION PAGE
# ============================================
elif page == "😊 User Satisfaction":
    st.title("😊 User Satisfaction Analysis")
    st.markdown("---")

    satisfaction = pd.read_csv('data/satisfaction_scores.csv')

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Satisfaction Score",
                  f"{satisfaction['satisfaction_score'].mean():.4f}")
    with col2:
        st.metric("Avg Engagement Score",
                  f"{satisfaction['engagement_score'].mean():.4f}")
    with col3:
        st.metric("Avg Experience Score",
                  f"{satisfaction['experience_score'].mean():.4f}")

    st.markdown("---")

    # Top 10 satisfied users
    st.subheader("🏆 Top 10 Most Satisfied Customers")
    st.dataframe(satisfaction.nlargest(10, 'satisfaction_score')[
        ['MSISDN/Number', 'engagement_score',
         'experience_score', 'satisfaction_score']
    ])

    st.markdown("---")

    # Satisfaction distribution
    st.subheader("📊 Satisfaction Score Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(satisfaction['satisfaction_score'],
                 bins=50, kde=True, color='purple', ax=ax)
    ax.set_title('Distribution of Satisfaction Scores')
    ax.set_xlabel('Satisfaction Score')
    st.pyplot(fig)

    st.markdown("---")

    # Cluster summary
    st.subheader("🎯 Satisfaction Clusters")
    cluster_summary = satisfaction.groupby('satisfaction_cluster').agg(
        avg_satisfaction=('satisfaction_score', 'mean'),
        avg_experience=('experience_score', 'mean'),
        avg_engagement=('engagement_score', 'mean'),
        count=('MSISDN/Number', 'count')
    ).reset_index()
    st.dataframe(cluster_summary)