import pandas as pd
import os

def save_features(df, filename):
    """Save features to CSV file"""
    path = f"data/{filename}.csv"
    df.to_csv(path, index=False)
    print(f"Features saved to {path}")

def load_features(filename):
    """Load features from CSV file"""
    path = f"data/{filename}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"Features loaded from {path}")
        return df
    else:
        print(f"File {path} not found!")
        return None