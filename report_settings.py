"""report_setting is to obtain the specifics (e.g. destination language) for the reports..
"""
def set_report_document_code(_document_code):
    """set_report_document_code sets the document code of the report being generated (eg. 'AB-123')
    """
    global report_code
    report_code =_document_code

def get_report_document_code():
    """get_report_document_code gets the document code of the report being generated (eg. 'AB-123')
    """
    return(report_code)

def set_report_language(_dest_language):
    """set_report_language sets the destination language as a global variable (e.g. 'en')
    """
    global report_lang
    report_lang =_dest_language

def get_report_language(terminalmessage:bool = False):
    """set_report_language gets the destination language
    """
    if type(report_lang) == str:
        if terminalmessage: print('From get_report_language / report_settings, retreiving report language, it is : ', report_lang)
    else:
        print("Something went wrong retreiving the destination language, it's not a string")
        raise(TypeError)
        
    return(report_lang)

def set_report_candidate_name(_name):
    """set_report_candidate_name sets the name of the candidate as a global variable (e.g. 'Henk de Bruijn')
    """
    global candidate_name
    candidate_name = _name

def get_report_candidate_name():
    """get_report_candidate_name gets the name of the candidate
    """
    return(candidate_name)

def get_config_file_name():
    """get_config_file_name generates and returns the file name of the CF report documents configuration file.
    (e.g. 'Henk Moos_AB-123_config')
    """
    _config_name = candidate_name + '_' + report_code + '_config'
    return(_config_name)