import pandas as pd
import numpy as np

def load_data(filepath):
    """Load the telecom dataset"""
    df = pd.read_excel(filepath)
    print(f"Data loaded! Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    return df

def clean_data(df):
    """Clean missing values and outliers"""
    print("Cleaning data...")
    for col in df.select_dtypes(include='number').columns:
        df[col].fillna(df[col].mean(), inplace=True)
    for col in df.select_dtypes(include='object').columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    for col in df.select_dtypes(include='number').columns:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = df[col].clip(mean - 3*std, mean + 3*std)
    print("Data cleaned!")
    return df

def get_user_aggregation(df):
    """Aggregate data per user"""
    user_agg = df.groupby('MSISDN/Number').agg(
        sessions=('Bearer Id', 'count'),
        total_duration=('Dur. (ms)', 'sum'),
        total_dl=('Total DL (Bytes)', 'sum'),
        total_ul=('Total UL (Bytes)', 'sum'),
        social_media_dl=('Social Media DL (Bytes)', 'sum'),
        social_media_ul=('Social Media UL (Bytes)', 'sum'),
        youtube_dl=('Youtube DL (Bytes)', 'sum'),
        youtube_ul=('Youtube UL (Bytes)', 'sum'),
        netflix_dl=('Netflix DL (Bytes)', 'sum'),
        netflix_ul=('Netflix UL (Bytes)', 'sum'),
        google_dl=('Google DL (Bytes)', 'sum'),
        google_ul=('Google UL (Bytes)', 'sum'),
        email_dl=('Email DL (Bytes)', 'sum'),
        email_ul=('Email UL (Bytes)', 'sum'),
        gaming_dl=('Gaming DL (Bytes)', 'sum'),
        gaming_ul=('Gaming UL (Bytes)', 'sum'),
        other_dl=('Other DL (Bytes)', 'sum'),
        other_ul=('Other UL (Bytes)', 'sum'),
    ).reset_index()

    user_agg['total_traffic'] = user_agg['total_dl'] + user_agg['total_ul']
    user_agg['social_media'] = user_agg['social_media_dl'] + user_agg['social_media_ul']
    user_agg['youtube'] = user_agg['youtube_dl'] + user_agg['youtube_ul']
    user_agg['netflix'] = user_agg['netflix_dl'] + user_agg['netflix_ul']
    user_agg['google'] = user_agg['google_dl'] + user_agg['google_ul']
    user_agg['email'] = user_agg['email_dl'] + user_agg['email_ul']
    user_agg['gaming'] = user_agg['gaming_dl'] + user_agg['gaming_ul']
    user_agg['other'] = user_agg['other_dl'] + user_agg['other_ul']

    print(f"User aggregation done! {len(user_agg)} unique users found")
    return user_agg
