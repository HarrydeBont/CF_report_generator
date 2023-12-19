""" get_doc_id returns  the reference to the Google doc the 'doc_id'
1)  Extracts the client_code from the test_code (e.g. 'XJ-001') -> client code (e.g. 'XJ') to reference to an URL-overview.
2)  Each client has a specific URL-overview an unique URL for every test
3)  Each overview has URL references to test documents
4)  Return the reference to the Google doc 'doc_id' (e.g. '1b3cgbMxYvkNQLryPJRm36pRBPpvI98AWn0qx_xStfrI')
"""
import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from test_code_to_URL_overview import convert_test_code_to_URL
from Check_status_report import get_CF_timestamp
from write_sheet_values import update_values
    
# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # for editing, reading en deleting spreadsheets

# The ID and range of a sample spreadsheet.
# Document id is a string in the format 'AB-999', A-indicating company, B indicating client and 999 indicating the sequential number

def open_URL_doc(doc_id : str = 'XJ-083', terminalmessage:bool = True):
    """ - determine which client.
        - Get information from google doc: 'HTTPS-URL overview CF report'.
    """
    client_code = doc_id[:2] # Use first two characters as client code
    URL_overview, Formulier = convert_test_code_to_URL(client_code, True)
  
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
        # print('service is: ', service)
        # Call the Sheets API
        sheet = service.spreadsheets()
        # print('sheet is: ', sheet)
        result = sheet.values().get(spreadsheetId=URL_overview,
                                    range=Formulier).execute()
        # print('result is: ', result)
        url_reference = result.get('values', [])
        if not terminalmessage:
            print(url_reference)

        if not url_reference:
            if terminalmessage: print('No data found.')
            return
       
        # print('From get_doc_id, document url is: ', url_reference)
        return(url_reference)

    except HttpError as err:
        if terminalmessage: print(err)


def search_id(zoek_code, url_reference, terminalmessage:bool = True):
    # print(zoek_code, url_reference)
    try:
        test = dict(url_reference) # Try to open the spreadsheet as a dictionary, if not spreadsheet empty
            
        string_search_error = ' '
        try:
            string_search_error = "string '/d/' not found"
            start_str = test[zoek_code].index('/d/')

            # print(start_str)
            string_search_error = "string '/edit' not found"
            stop_str = test[zoek_code].index('/edit')
            Ggl_url = test[zoek_code][start_str+3:stop_str]
            # print(stop_str)
            return(Ggl_url)
        except:
            if terminalmessage: print('Document ID not found! During search in string got error code: ', string_search_error)
            sys.exit()
    except:
        return('Empty spreadsheet.')
