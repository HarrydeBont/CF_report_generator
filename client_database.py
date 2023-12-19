import json

client_database = 'client_test_link_dict.json'

def key_in_client_database(CF_report_number):
    with open(client_database, 'r') as file:
        client_test_link_dict = json.load(file)

    client_key = CF_report_number[:2]  # Get the first two characters

    # Check if client_key exists in the dictionary
    found_key = client_key in client_test_link_dict
    return found_key
    

def get_document_id(CF_report_number):
    """
    Read and edit the client test link dictionary from the file client_test_link_dict
    Ask user for inpot when needed
    """
    with open(client_database, 'r') as file:
        client_test_link_dict = json.load(file)

    client_key = CF_report_number[:2]  # Get the first two characters

     # Check if client_key exists in the dictionary
    while client_key not in client_test_link_dict:
        print('Invalid CF_report_number. Could not find a matching Document_ID.')
        return
    # When client_key does exists in the dictionary
    return client_test_link_dict[client_key]

def get_client_name(CF_report_number):
    """This function (untested) reads the JSON file, extracts the client key from the CF_report_number, and then looks up the corresponding comment in the JSON.
    It then splits the comment to extract the client name and returns it. If the client key is not found in the JSON, it raises a ValueError.
    """
    client_key = CF_report_number[:2] # get the first two characters

    # Open the JSON file containing the client information
    with open(client_database, 'r') as file:
        client_test_link_dict = json.load(file)

    # Construct the comment key to retrieve the client name
    comment_key = "comment_" + client_key

    # Check if the comment key exists in the dictionary
    if comment_key in client_test_link_dict:
        # Extract the client name from the comment
        client_name = client_test_link_dict[comment_key].split(": ")[1]
        return client_name
    else:
        raise ValueError('Invalid CF_report_number. Could not find a matching client name.')

def add_to_client_database(client_key, client_name, document_link):
    # Define the filename
    filename = 'client_test_link_dict.json'

    # Read the existing data from the JSON file
    with open(filename, 'r') as file:
        client_test_link_dict = json.load(file)

    # Add the new client key and document link
    client_test_link_dict[client_key] = document_link

    # Add the comment with the client name
    comment_key = f'comment_{client_key}'
    client_test_link_dict[comment_key] = f'Client name: {client_name}'

    # Write the updated data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(client_test_link_dict, file)

    print(f'Added {client_name} with key {client_key} to the database.')
