import gspread
from google.oauth2.service_account import Credentials

# Define the scope
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Load credentials
creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)

# Authorize the client
client = gspread.authorize(creds)

# YOUR SHEET ID - Replace this with your actual Sheet ID
sheet_id = '1iDa0Psp2vtgOCmBKn8VFc4BG1KqH9U8702rEolqUquQ'

try:
    # Open the sheet by ID
    sheet = client.open_by_key(sheet_id)
    
    # Get the first worksheet (responses)
    worksheet = sheet.sheet1
    
    # Get all data
    records = worksheet.get_all_records()
    
    print("✅ Connected to Google Sheets successfully!")
    print(f"📊 Found {len(records)} rows of data")
    
    if records:
        print(f"📋 Columns: {list(records[0].keys())}")
        print("\n📝 First row of data:")
        for key, value in records[0].items():
            print(f"   {key}: {value}")
    else:
        print("ℹ️ No data found in the sheet (you may need to submit a test response)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔍 Troubleshooting Tips:")
    print("1. Make sure you've shared the sheet with your service account email")
    print("2. Check that the Sheet ID is correct")
    print("3. Ensure Google Sheets API is enabled in your Google Cloud project")
