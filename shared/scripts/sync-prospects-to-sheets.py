"""
Sync ICP prospects from local CSV to Google Sheets
Auto-runs as part of linkedin-daily-planner Evening Block
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import sys
from datetime import datetime

# Setup the credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r'C:\Users\melve\Downloads\gen-lang-client-0759962377-02a98892e599.json',
    scope
)

# Authorize and open the spreadsheet
client = gspread.authorize(creds)
SPREADSHEET_ID = '1-3Ua8O6vwqHtuUe17VepNpWPWPeT0eeL8jXfN40lfKc'

try:
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.sheet1

    # Read the CSV file
    csv_file = r'C:\Users\melve\.claude\skills\icp-prospects.csv'
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Clear existing data and update with new data
    sheet.clear()
    sheet.update(data, 'A1')

    # Success output
    timestamp = datetime.now().strftime('%H:%M')
    print(f"[{timestamp}] Synced {len(data)-1} prospects to Google Sheets")
    print(f"[{timestamp}] Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    sys.exit(0)

except Exception as e:
    timestamp = datetime.now().strftime('%H:%M')
    print(f"[{timestamp}] ERROR syncing prospects: {str(e)}")
    sys.exit(1)
