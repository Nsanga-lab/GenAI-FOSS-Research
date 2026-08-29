import pandas as pd
import os
from pathlib import Path

def explore_data():
    """Explore the downloaded survey data"""
    
    # Find the latest data file
    raw_dir = Path('data/raw')
    latest_file = raw_dir / 'survey_responses_latest.csv'
    
    if not latest_file.exists():
        print("❌ No data found! Run download_data.py first.")
        return
    
    # Load the data
    df = pd.read_csv(latest_file)
    
    print("=" * 60)
    print("📊 SURVEY DATA EXPLORER")
    print("=" * 60)
    
    print(f"\n📁 File: {latest_file}")
    print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\n📋 Column Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print("\n📊 Basic Statistics:")
    print(f"   - Missing values: {df.isnull().sum().sum()}")
    print(f"   - Complete rows: {df.dropna().shape[0]}")
    
    print("\n📝 First 3 rows:")
    print(df.head(3))
    
    print("\n📝 Data Types:")
    print(df.dtypes)
    
    # Check for open-ended questions
    open_ended = [col for col in df.columns if 'F' in col and len(col) <= 5]
    print(f"\n💡 Found {len(open_ended)} open-ended questions (starting with 'F')")
    
    return df

if __name__ == "__main__":
    df = explore_data()
