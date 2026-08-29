import pandas as pd
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
CLEAN_DIR = os.path.join(PROJECT_ROOT, 'data', 'clean')
os.makedirs(CLEAN_DIR, exist_ok=True)

def clean_survey_data():
    """Placeholder cleaning function"""
    raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv') and 'latest' not in f]
    if not raw_files:
        print("⚠️ No raw data files found.")
        return
    
    latest_file = sorted(raw_files)[-1]
    df = pd.read_csv(os.path.join(RAW_DIR, latest_file))
    
    # Basic cleaning: remove empty rows
    df_clean = df.dropna(how='all')
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    clean_path = os.path.join(CLEAN_DIR, f'cleaned_data_{timestamp}.csv')
    df_clean.to_csv(clean_path, index=False)
    
    print(f"✅ Cleaned {len(df_clean)} rows. Saved to {clean_path}")

if __name__ == "__main__":
    clean_survey_data()
