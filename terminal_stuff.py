"""Ternminal stuff deals with all the input from the user via the terminal.
This allows for an upgrade in the future when we want a graphical input.
"""


import time
import os
import json

def clear_screen(timer=0.7):
    """Pause to get the user pay attention. 
        Clear the terminal  to keep it tight and clean.
    """
    time.sleep(timer)  # pause for 0.5 seconds
    os.system('cls' if os.name == 'nt' else 'clear')

def tprint(msg, time=2):
    """Print a message to the terminal and erase after timer expires (default = 2).
        Designed to replace print statements, keeping a clear code base, for future UI upgrades
        Enter time > 9 for no cls of the terminal.
    """
    print(msg)
    
    if time < 9:
        clear_screen(time)

def reminder_CF_Web():
    """
    Remind the user to get data from the web first, before generating a report
    """
    print("Reminder. Did you get new data from the web?")
    forgot = input("Your choice [Y/N]: ").lower()
    if forgot == 'n':
        print('Please run [CF_from_web.py] first, to retreive new data.')
        quit()
    else:
        print('Continuing with latest-web-retreived data.')

def select_data_source():
    """select whether the data for the CF test is to be retreived from a seperate test file [single_data_source] or from a test file that accumulates test_results [returning_client_data]
    """
    while True:
        # check to see what the user wants: either address a single test document
        # or a returning client form (Your Professional and Expro)
        # User instructions
        print("Please select your data source:")
        print("[s] Single Test Form")
        print("[r] Returning Clients Form")

        # Repeat until the user gives a valid input
        # User input
        data_source = input("Your choice: ").lower()
        
        if data_source == 's':
            single_data_source = True
            returning_client_data = False
            print("Single Test Form selected")
            clear_screen()
            return(single_data_source,returning_client_data)  # The input is valid, return status
        
        elif data_source == 'r':
            single_data_source = False
            returning_client_data = True
            print("Returning Clients Form selected")
            return(single_data_source,returning_client_data)  # The input is valid, return status
        else: 
            print('Invalid entry. Please enter "s" for Single Test Form or "r" for Returning Clients Form.')
            clear_screen(1)

import re # Regular expression

def get_document_code()->str:
    """Start an infinite loop to keep asking for input until a valid code, in the format "AB-999", is provided
    """
    while True:
        clear_screen(0)
        CF_report_number = input('Provide document code (format AB-999): ').upper()

        # Regular expression pattern to match the desired format
        pattern = r'^[A-Z]{2}-\d{3,}$'

        # ^        : Start of the line
        # [A-Z]{2} : Exactly two uppercase letters (A-Z)
        # -        : A dash
        # \d{3,}   : At least three digits (0-9)
        # $        : End of the line

        if re.match(pattern, CF_report_number):
            # If the input matches the pattern, exit the loop
            break
        else:
            # If the input does not match the pattern, print an error message
            print("Invalid format! Please enter the document code in the format AB-999.")
            clear_screen(2)
    print("Document code:", CF_report_number)
    clear_screen()
    return CF_report_number

def get_gender()->bool:
    # Start an infinite loop to keep asking for input until a valid one is provided
    while True:
        gender = input('What is the gender? [M|F] (Leave blank for M): ').strip().upper()

        # Check if the input is 'M', 'F', or an empty string
        if gender == 'M' or gender == 'F' or gender == '':
            if gender == '' or gender == 'M':
                gender_descr = 'Male'
            else:
                gender_descr = 'Female'
            print('the chosen gender is : ', gender_descr)
            clear_screen(2)
            break
        else:
            # If the input is not valid, print an error message
            print("Invalid input! Please enter 'M' for male, 'F' for female, or leave blank for male.")
            clear_screen(3)

    # Set the female_gender variable based on the input
    female_gender = gender == 'F'

    return female_gender

def capitalize_first_letter(input_string):
    return input_string.capitalize()

def ask_client_name():
    """Ask for the name of the client to be printed on the report.
        The first character is always capatilized.
    """
    name = input('Geef de naam van de opdrachtgever in: ')
    print("Converted name:", name)
    clear_screen(2)
    return name[0].upper() + name[1:]

def get_document_id(CF_report_number):
    """
    Read and edit the client test link dictionary from the file client_test_link_dict
    Ask user for inpot when needed
    """
    with open('client_test_link_dict.json', 'r') as file:
        client_test_link_dict = json.load(file)

    client_key = CF_report_number[:2]  # Get the first two characters

    # Check if client_key exists in the dictionary
    while client_key not in client_test_link_dict:
        print('Invalid CF_report_number. Could not find a matching Document_ID.')
        retry = input('Do you want to add a new document_ID? [Y/N]: ').upper()
        if retry == 'N':
            CF_report_number = input('Provide document code: ')
            client_key = CF_report_number[:2]
        else:
            client_name = ask_client_name()
            new_client_key = input('Enter a new client code (two characters): ')
            while len(new_client_key) != 2:
                print('Client code must be two characters.')
                new_client_key = input('Enter a new client code (two characters): ')
            new_client_link = input(f'Enter the link to the test file for {client_name}: ')
            client_test_link_dict[new_client_key] = new_client_link
            # Add a comment to clarify the client name
            client_test_link_dict[f'comment_{new_client_key}'] = f'Client name: {client_name}'
            with open('client_test_link_dict.json', 'w') as file:
                json.dump(client_test_link_dict, file)
            print('New client added.')
            return new_client_link
    # When client_key does exists in the dictionary
    return client_test_link_dict[client_key]

def get_int_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input == '':
            return 0
        try:
            print('')
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a whole number.")