from Ggl_get_data import get_Ggl_data
from get_doc_id import search_id, open_URL_doc
from Check_status_report import get_CF_timestamp
from write_sheet_values import update_values
from test_code_to_URL_overview import convert_test_code_to_URL

terminalmessage = True
client_code = input('Which overview do you want to process? Expro [XJ], s [YS], Individual [IP], Deep-Dive[DD], Test Case [TX]: ')
URL_overview, Formulier = convert_test_code_to_URL(client_code, True)

URL_overview_data = get_Ggl_data(URL_overview, Formulier)
print(len(URL_overview_data))
start = int(input('Start row? : '))
stop = int(input('Until row? : '))
start = start - 2
stop = stop - 1
for i, (doc, url) in enumerate(URL_overview_data[start:stop], start=start): # Loop through url list
    print('row: ',i+start+2, end = ' ')
    print(doc, url, end = ' -> ')
    Ggl_url = search_id(doc, URL_overview_data, True)                      # return url in Google format
    # print(Ggl_url)
    # print(Ggl_url, end = ' ')
    _timestamp, timestamp_r3 = get_CF_timestamp(Ggl_url, False)
    URL_overview_row = 'C'+str(i+2) # 'C999'
    # print(URL_overview_row, sep = '', end = ' Test-form: ' )
    if  _timestamp == None: # empty form
        update_values(URL_overview,
            URL_overview_row, "USER_ENTERED", 'Nog niet ingevuld')
        print('No data yet..')
    else:
        update_values(URL_overview,
            URL_overview_row, "USER_ENTERED", str(_timestamp[0][0]))
        print(_timestamp, str(timestamp_r3[0][0])) # second timestamp copied?
        # call_for_field_copy