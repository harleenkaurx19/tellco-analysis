import pandas as pd
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PostgreSQL connection
DB_USER = "postgres"
DB_PASSWORD = "rohi7411"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "tellco_db"

# Create connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def export_to_db():
    """Export all scores to PostgreSQL database"""
    
    # Load satisfaction scores
    print("Loading satisfaction scores...")
    satisfaction = pd.read_csv('data/satisfaction_scores.csv')
    
    # Export to PostgreSQL
    print("Exporting to PostgreSQL...")
    satisfaction.to_sql(
        'user_scores',
        engine,
        if_exists='replace',
        index=False
    )
    print(f"Exported {len(satisfaction)} rows to user_scores table!")
    
    # Verify export
    print("\nVerifying export...")
    result = pd.read_sql("SELECT * FROM user_scores LIMIT 10", engine)
    print(result)
    print("\nExport successful!")

if __name__ == "__main__":
    export_to_db()
