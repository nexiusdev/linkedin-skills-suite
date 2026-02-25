"""
Sync ICP prospects from icp-prospects.md to Google Sheets.
Reads the markdown table directly (no CSV intermediary).
Auto-runs as part of linkedin-daily-planner Evening Block.

Prerequisites:
- pip install gspread google-auth
- Service account JSON key at SERVICE_ACCOUNT_FILE path
- Spreadsheet shared with: claude-sheets@gen-lang-client-0759962377.iam.gserviceaccount.com (Editor)
- Google Drive API + Google Sheets API enabled on project gen-lang-client-0759962377

Trigger: "sync to googlesheet" or auto-run in Evening Block
"""
import gspread
from google.oauth2.service_account import Credentials
import re
import sys
import csv
import os
from datetime import datetime

# --- Configuration ---
SERVICE_ACCOUNT_FILE = r"{{CLIENT_WORKSPACE_ROOT}}\gen-lang-client-0759962377-207882157ce2.json"
PROSPECTS_FILE = r"{{CLIENT_WORKSPACE_ROOT}}\shared\logs\icp-prospects.md"
SPREADSHEET_ID = "1-3Ua8O6vwqHtuUe17VepNpWPWPeT0eeL8jXfN40lfKc"
DRIVE_FOLDER_ID = "1PAvNtv07W2wsLkAgIr93xxPCeoINjAnX"
SERVICE_ACCOUNT_EMAIL = "claude-sheets@gen-lang-client-0759962377.iam.gserviceaccount.com"
CSV_BACKUP_DIR = r"{{CLIENT_WORKSPACE_ROOT}}\shared\logs\backups"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def parse_markdown_table(filepath):
    """Parse the prospects markdown table into headers + rows."""
    rows = []
    headers = None
    in_table = False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                if in_table and headers:
                    break
                continue

            cells = [c.strip() for c in line.split("|")]
            cells = cells[1:-1]

            if not headers:
                headers = cells
                in_table = True
                continue

            if all(re.match(r'^-+$', c) for c in cells):
                continue

            rows.append(cells)

    return headers, rows


def save_csv_backup(headers, rows):
    """Save versioned CSV backup to backups folder."""
    os.makedirs(CSV_BACKUP_DIR, exist_ok=True)

    # Format: icp-prospects_YYYYMMDDHHMM.csv
    version = datetime.now().strftime('%Y%m%d%H%M')
    csv_filename = f"icp-prospects_{version}.csv"
    csv_path = os.path.join(CSV_BACKUP_DIR, csv_filename)

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return csv_path


def main():
    timestamp = datetime.now().strftime('%H:%M')

    try:
        print(f"[{timestamp}] Parsing icp-prospects.md...")
        headers, rows = parse_markdown_table(PROSPECTS_FILE)
        print(f"[{timestamp}] Found {len(rows)} prospects with {len(headers)} columns")

        # Save CSV backup (always, even if Sheets sync fails)
        csv_path = save_csv_backup(headers, rows)
        print(f"[{timestamp}] CSV backup saved: {csv_path}")

        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)

        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.sheet1
        worksheet.clear()

        all_data = [headers] + rows
        worksheet.update(all_data, value_input_option="RAW")

        # Format header row (blue bg, white bold text, frozen)
        worksheet.format("1:1", {
            "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.7},
            "textFormat": {"bold": True, "foregroundColorStyle": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}},
        })
        worksheet.freeze(rows=1)
        worksheet.update_title("Prospects")

        timestamp = datetime.now().strftime('%H:%M')
        print(f"[{timestamp}] Synced {len(rows)} prospects to Google Sheets")
        print(f"[{timestamp}] Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        sys.exit(0)

    except Exception as e:
        timestamp = datetime.now().strftime('%H:%M')
        print(f"[{timestamp}] ERROR syncing prospects: {str(e)}")
        print(f"[{timestamp}] CSV backup available at: {csv_path if 'csv_path' in locals() else 'N/A'}")
        sys.exit(1)


if __name__ == "__main__":
    main()
