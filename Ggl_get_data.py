import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# CF_spreadsheet = '1aW4vJzyWp6Nak00ivH20REHlT1bD92m3NhYqw6MEUd4'
# _sheet_range = 'Uitslag!B6:J10'
# candidate_info = 'Uitslag!A17:B23'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # for editing, reading en deleting spreadsheets

def get_Ggl_data(_spreadsheet, _sheet_range ):
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=_spreadsheet,
                                    range=_sheet_range).execute()
        score = result.get('values', [])

        if not score: # Check if a list is empty by its type flexibility
            print('No data found.')
            return
        else: 
            return(score)
    
    except HttpError as err:
        print(err)
