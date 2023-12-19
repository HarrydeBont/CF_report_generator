import json

def get_document_id(CF_report_number):
    """
    Read and edit the client test link dictionary from the file client_test_link_dict
    Ask user for inpot when needed
    """
    with open('client_test_link_dict.json', 'r') as file:
        client_test_link_dict = json.load(file)

    client_key = CF_report_number[:2]  # Get the first two characters

