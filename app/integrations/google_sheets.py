import os
from datetime import datetime
from typing import Dict

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ----------------------------------------
# CONFIG
# ----------------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")

SHEET_NAME = "Leads"  # change if needed

# ----------------------------------------
# AUTH
# ----------------------------------------
def get_sheets_service():
    if not SERVICE_ACCOUNT_FILE or not SPREADSHEET_ID:
        raise RuntimeError("Google Sheets env variables missing")

    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("sheets", "v4", credentials=creds)
    return service

# ----------------------------------------
# APPEND LEAD
# ----------------------------------------
def append_lead_to_sheet(lead: Dict):
    """
    lead dict must contain:
    - session_id
    - name
    - email
    - phone
    - intent_summary
    """

    service = get_sheets_service()
    sheet = service.spreadsheets()

    values = [[
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        lead.get("session_id"),
        lead.get("name"),
        lead.get("email"),
        lead.get("phone"),
        lead.get("intent_summary"),
    ]]

    body = {"values": values}

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
