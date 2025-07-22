from flask import Flask, request
import os
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Setup credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "/etc/secrets/credentials.json"  # Path used by Render

SPREADSHEET_ID = "1XXUKcnOUttzd4VlwjEP7PCnF3Eh0YxEuElJDFBQ4o_M"
SHEET_NAME = "gmass"

# Authenticate and open worksheet
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
gc = gspread.authorize(creds)
worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.route('/notify', methods=['GET', 'POST'])
def notify():
    if request.method == 'POST':
        data = request.form or request.json or {}
    else:
        data = request.args

    email = data.get('EmailAddress', '')
    campaign = data.get('CampaignID', '')
    useragent = data.get('UserAgent', '')
    timestamp = data.get('TimeStamp', '')

    # Determine if the open is likely human
    useragent_lower = useragent.lower()
    if any(client in useragent_lower for client in ['outlook', 'thunderbird', 'foxmail', 'windows nt', 'macintosh']):
        likely_human = 'Yes'
    else:
        likely_human = 'No'

    # Append to spreadsheet
    worksheet.append_row([email, campaign, useragent, timestamp, likely_human])
    print(f"Logged to sheet: {email}, {campaign}, {useragent}, {timestamp}, Likely Human: {likely_human}")

    return "Logged to Google Sheet!"

@app.route('/')
def health():
    return "Render Webhook is live!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
