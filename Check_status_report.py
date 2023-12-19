from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from write_sheet_values import update_values


# If modifying these scopes, delete the file token.json. 
# https://developers.google.com/identity/protocols/oauth2/scopes#sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # for editing, reading en deleting spreadsheets
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly'] # for reading spreadsheet only

# writing the values to the URL overview
# https://developers.google.com/sheets/api/guides/values#python_2 Explaining how to do write values 

# CF_spreadsheet = '1aW4vJzyWp6Nak00ivH20REHlT1bD92m3NhYqw6MEUd4'
CF_timestamp_pos = 'Formulierreacties!A2' # time stamp position row 2
CF_name_stamp_pos = 'Formulierreacties!D2' # name stamp position
CF_timestamp_pos_row3 = 'Formulierreacties!A3' # time stamp position row 3
CF_row2 = 'Formulierreacties!A2:BN2' # all data from row 2
CF_row3 = 'Formulierreacties!A3:BN3' # all data from row 3


def copy_row2_to_row3(CF_spreadsheet, sheet):
    """Copies row 2 to row 3, this is needed because of a bug in the Google test form
    Doesn't work yet...
    An error occurred: <HttpError 400 when requesting https://sheets.googleapis.com/v4/spreadsheets/1K-O-3C9hScCKeTBL5L6QudnYZVKQb0CVLt-851dS4e0/values/Formulierreacties%21A3%3ABN3?valueInputOption=USER_ENTERED&alt=json returned "Invalid values[2][0]: struct_value {
    Solution: https://stackoverflow.com/questions/72190255/updating-cols-in-google-sheets ???
    """

    row2 = sheet.values().get(spreadsheetId=CF_spreadsheet,
                                    range=CF_row2).execute()
    # print(row2)
    update_values(CF_spreadsheet,
            CF_row3, "USER_ENTERED", row2)


def get_CF_timestamp(CF_spreadsheet, terminalmessage:bool = True):
    """1) Get timestamp information (and name candidate)
    """
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
                                    range=CF_timestamp_pos).execute()
        result_row3 = sheet.values().get(spreadsheetId=CF_spreadsheet,
                                    range=CF_timestamp_pos_row3).execute()
        result_name = sheet.values().get(spreadsheetId=CF_spreadsheet,
                                    range=CF_name_stamp_pos).execute()
        CF_timestamp = result.get('values', [])
        CF_timestamp_row3 = result_row3.get('values', [])
        CF_name_stamp = result_name.get('values', [])

        if not CF_timestamp: # Check if a list is empty by its type flexibility
            if terminalmessage: print('No data found.')
            return(None, None)
        # Because of a bug in the test form we need to copy row_2 to row_3
        if CF_timestamp != CF_timestamp_row3: 
            # call copy function
            print('çopy this')   
            copy_row2_to_row3(CF_spreadsheet, sheet)     
        return(CF_timestamp, CF_name_stamp) # return answers on open question as well update (incorporating text_analyses in automation)

    except HttpError as err:
        if terminalmessage: print(err)


if __name__ == '__main__':

    # print(get_CF_timestamp('1uro0PYsSdUPyZN594a72-00HHtik1tFjHlmmw-sb1FU')) # YS empty form

    # print(get_CF_timestamp('1Amgbr2HxUw-lrF0tR9I-0rrCt7MMK23MJf4ywhTGL1c')) # YS hand typed the date-time

    # print(get_CF_timestamp('1Oz1kG9Z_uTqvHLNmh5EpFdXybwu_qCxbbW7YnZkxJ74')) # XJ empty form

    print(get_CF_timestamp('1cy3k_5b4-ages0SS5MWVhToFuVcalI27-PlUigI2dqg')) # DD ingevuld door form


    


    

    