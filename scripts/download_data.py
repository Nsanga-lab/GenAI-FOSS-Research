import os
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')

# Create directory if it doesn't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def download_google_form_data():
    """
    Downloads the latest responses from Google Forms and saves as CSV
    """
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            os.path.join(PROJECT_ROOT, 'credentials.json'),
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Connect to Google Sheets
        gc = gspread.authorize(creds)

        # YOUR GOOGLE SHEET URL - Replace with your actual sheet URL
        sheet_url = 'https://docs.google.com/spreadsheets/d/1iDa0Psp2vtgOCmBKn8VFc4BG1KqH9U8702rEolqUquQ/edit'
        
        # Open the sheet
        sheet = gc.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)  # First worksheet

        # Get all data as a list of lists
        data = worksheet.get_all_values()

        # Convert to DataFrame
        if data and len(data) > 1:  # Check if there's data beyond headers
            headers = data[0]  # First row is headers
            rows = data[1:]    # Remaining rows are data
            df = pd.DataFrame(rows, columns=headers)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"survey_responses_{timestamp}.csv"
            filepath = os.path.join(RAW_DATA_DIR, filename)

            # Save as CSV
            df.to_csv(filepath, index=False)
            print(f"✅ Data downloaded successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Total responses: {len(df)}")
            print(f"📋 Columns: {len(headers)} columns found")
            
            # Also save a version without timestamp as "latest"
            latest_path = os.path.join(RAW_DATA_DIR, "survey_responses_latest.csv")
            df.to_csv(latest_path, index=False)
            print(f"📁 Latest version saved as: survey_responses_latest.csv")
            
            return df
        else:
            print("⚠️ No data found in the sheet or sheet is empty")
            print("   Make sure you have submitted at least one test response")
            return None
            
    except FileNotFoundError as e:
        print(f"❌ Error: credentials.json file not found")
        print("   Make sure credentials.json is in the project root folder")
        print(f"   {e}")
        return None
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None

def load_latest_data():
    """
    Load the most recently saved data
    """
    latest_path = os.path.join(RAW_DATA_DIR, "survey_responses_latest.csv")
    if os.path.exists(latest_path):
        return pd.read_csv(latest_path)
    else:
        print("⚠️ No latest data found. Run download_google_form_data() first.")
        return None

if __name__ == "__main__":
    # Run the download function
    df = download_google_form_data()
    
    # If data was downloaded, show a preview
    if df is not None:
        print("\n📝 Preview of first 5 responses:")
        print(df.head())
        
        print("\n📊 Column names:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
