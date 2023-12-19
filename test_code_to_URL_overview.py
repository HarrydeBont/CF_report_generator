def convert_test_code_to_URL(client_code:str, terminalmessage:bool = False):
    """convert_test_code_to_URL converts a two character text-string which is part of a code attached to a test form. e.g. 'XJ'
        It returns the Google URL reference to the Google doc containing all the tests that are issued (manually made).
    """
    client_code = client_code[:2] # A user could enter a whole test-ID eg. 'YS-001'
    match(client_code):
        case 'XJ':
            URL_overview = '1b3cgbMxYvkNQLryPJRm36pRBPpvI98AWn0qx_xStfrI' # URL overview Expro
            Formulier = 'doc_id!A2:B122'
            if terminalmessage: print('Client is Expro Engineering B.V.')
        case 'YS':
            URL_overview = '1ukk6kWB0sQHc_uU6j78rGLPS91WETMhrb-hrRC4Up_c' # URL overview Your Professional
            Formulier = 'doc_id!A2:B122'
            if terminalmessage: print('Client is Your Professionals B.V.')
        case 'IP':
            URL_overview = '1b3cgbMxYvkNQLryPJRm36pRBPpvI98AWn0qx_xStfrI' # URL overview Individual or self paying Professional
            Formulier = 'doc_id!A2:B122'
            if terminalmessage: print('Client is an Individual')
        case 'DD':
            URL_overview = '1GxAqXE6NArhyeYQmVHsM6ckA_KhCma_d27jKDKFNPFo' # URL overview Individual or self paying Professional
            Formulier = 'doc_id!A2:B122'
            if terminalmessage: print('Client a Deep-Dive participant')
        case 'TX':
            URL_overview = '1lmgVs9b6Q21KE7g24Y7c6aYbnB9pWykDLQc9IvYqb9o' # TX for testing puposes
            Formulier = 'doc_id!A2:B122'
            if terminalmessage: print('Testing the waters')
        case _:
            if terminalmessage: print('Client code unknown. Halting Program.')
            URL_overview = 'Invalid'
            Formulier = 'Invalid'
            exit()
    return(URL_overview, Formulier)

