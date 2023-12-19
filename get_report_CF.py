""" The get_report_CF retreives info from the Google cloud
1) Get information from Courage and Fear test results from the Google Cloud.
2) Return scores and candidate's specifics

"""
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # for editing, reading en deleting spreadsheets

# The ID and range of a sample spreadsheet.
# Use 'XJ-084 Vragenlijst Expro (Respons)'Google sheet as test case

# CF_spreadsheet = '1aW4vJzyWp6Nak00ivH20REHlT1bD92m3NhYqw6MEUd4'
CF_scores = 'Uitslag!B6:J10'
candidate_info = 'Uitslag!A17:B23'

def get_CF_data(CF_spreadsheet):
    
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
        result = sheet.values().get(spreadsheetId=CF_spreadsheet,
                                    range=CF_scores).execute()
        score = result.get('values', [])

        if not score: # Check if a list is empty by its type flexibility
            print('No data found.')
            return

        # print('Angst, Moed:')
        # for row in score:
        #     # Print columns A and E, which correspond to indices 0 and 1.
        #     print('%s, %s' % (row[0], row[1]))
        
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=CF_spreadsheet,
                                    range=candidate_info).execute()
        CF_report_item = result.get('values', [])

        if not CF_report_item: # Check if a list is empty by its type flexibility
            print('No data found.')
            return

        # print('Item, Description:')
        # for row in CF_report_item:
        #     Print columns A and B, which correspond to indices 0 and 1.
        #     print('%s, %s' % (row[0], row[1]))
        
        return(score, CF_report_item) # return answers on open question as well update (incorporating text_analyses in automation)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    print(get_CF_data('1uro0PYsSdUPyZN594a72-00HHtik1tFjHlmmw-sb1FU'))